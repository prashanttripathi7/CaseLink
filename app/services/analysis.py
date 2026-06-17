import networkx as nx
from sqlalchemy import func, or_
from sqlalchemy.orm import selectinload

from app.models import Case, Entity, ENTITY_TYPES, db


def build_case_entity_graph(entity_types=None):
    graph = nx.Graph()
    query = Entity.query
    if entity_types:
        query = query.filter(Entity.entity_type.in_(entity_types))

    for case in Case.query.options(selectinload(Case.entities)).all():
        graph.add_node(
            f"case:{case.id}",
            kind="case",
            label=case.case_id,
            title=f"{case.case_id}<br>{case.fraud_type}<br>Status: {case.status}",
            status=case.status,
            fraud_type=case.fraud_type,
        )

    for entity in query.options(selectinload(Entity.cases)).all():
        node_id = f"entity:{entity.id}"
        graph.add_node(
            node_id,
            kind="entity",
            label=entity.value,
            title=f"{entity.type_label}<br>{entity.value}<br>Cases: {len(entity.cases)}",
            entity_type=entity.entity_type,
            type_label=entity.type_label,
        )
        for case in entity.cases:
            graph.add_edge(f"case:{case.id}", node_id, label=entity.type_label)

    return graph


def repeat_entities(limit=10):
    rows = (
        db.session.query(Entity, func.count(Case.id).label("case_count"))
        .join(Entity.cases)
        .group_by(Entity.id)
        .having(func.count(Case.id) > 1)
        .order_by(func.count(Case.id).desc(), Entity.entity_type.asc())
        .limit(limit)
        .all()
    )
    return rows


def investigation_insights(limit=5):
    insights = []
    repeat_rows = repeat_entities(limit=limit)

    for entity, case_count in repeat_rows[:3]:
        cases = sorted(entity.cases, key=lambda case: case.case_id)
        case_ids = [case.case_id for case in cases[:2]]
        if len(case_ids) >= 2:
            text = f"Investigations {case_ids[0]} and {case_ids[1]} share {entity.type_label} {entity.value}."
        else:
            text = f"{entity.type_label} {entity.value} appears in {case_count} separate investigations."
        insights.append({"text": text, "action": "search", "query": entity.value})

    graph = build_case_entity_graph()
    linked_components = []
    for component in nx.connected_components(graph):
        case_nodes = [node for node in component if node.startswith("case:")]
        entity_nodes = [node for node in component if node.startswith("entity:")]
        if len(case_nodes) > 1 and entity_nodes:
            linked_components.append((case_nodes, entity_nodes))

    linked_components.sort(key=lambda item: len(item[0]), reverse=True)
    if linked_components and len(insights) < limit:
        case_count = len(linked_components[0][0])
        insights.append(
            {
                "text": f"A linked fraud network involving {case_count} investigations has been detected.",
                "action": "network",
            }
        )

    if repeat_rows and len(insights) < limit:
        repeat_count = len(repeat_entities(limit=1000))
        noun = "entity" if repeat_count == 1 else "entities"
        insights.append(
            {
                "text": f"{repeat_count} repeat {noun} require analyst review.",
                "action": "network",
            }
        )

    if not insights:
        insights.append(
            {
                "text": "No cross-investigation correlations detected yet. Add digital evidence to begin link analysis.",
                "action": "create",
            }
        )

    return insights[:limit]


def linked_network_count():
    graph = build_case_entity_graph()
    return sum(1 for component in nx.connected_components(graph) if len(component) > 2)


def case_relationships(case):
    graph = build_case_entity_graph()
    source = f"case:{case.id}"
    if source not in graph:
        return {"direct": [], "indirect": [], "alerts": [], "paths": []}

    direct = []
    alerts = []
    for entity in case.entities:
        related = [c for c in entity.cases if c.id != case.id]
        if related:
            direct.append({"entity": entity, "cases": related})
            alerts.append(f"{entity.type_label} {entity.value} appears in {len(entity.cases)} investigations.")

    indirect = []
    paths = []
    for other in Case.query.filter(Case.id != case.id).all():
        target = f"case:{other.id}"
        if target not in graph or not nx.has_path(graph, source, target):
            continue
        path = nx.shortest_path(graph, source, target)
        if len(path) > 3:
            indirect.append({"case": other, "distance": (len(path) - 1) // 2, "path": _describe_path(graph, path)})
            paths.append(path)

    return {"direct": direct, "indirect": indirect, "alerts": alerts, "paths": paths}


def global_search(term):
    if not term:
        return {"cases": [], "entities": [], "alerts": []}

    like = f"%{term.strip()}%"
    cases = (
        Case.query.filter(
            or_(
                Case.case_id.ilike(like),
                Case.fir_number.ilike(like),
                Case.fraud_type.ilike(like),
                Case.victim_name.ilike(like),
            )
        )
        .order_by(Case.updated_at.desc())
        .all()
    )
    entities = Entity.query.filter(Entity.value.ilike(like)).order_by(Entity.entity_type.asc()).all()
    alerts = [
        f"{entity.type_label} {entity.value} links {len(entity.cases)} investigations."
        for entity in entities
        if len(entity.cases) > 1
    ]
    return {"cases": cases, "entities": entities, "alerts": alerts}


def dashboard_metrics():
    total_cases = Case.query.count()
    closed = Case.query.filter_by(status="Closed").count()
    active = Case.query.filter(Case.status != "Closed").count()
    unique_entities = Entity.query.count()
    repeats = len(repeat_entities(limit=1000))
    return {
        "total_cases": total_cases,
        "active": active,
        "closed": closed,
        "unique_entities": unique_entities,
        "linked_networks": linked_network_count(),
        "repeat_entities": repeats,
    }


def _describe_path(graph, path):
    labels = []
    for node in path:
        data = graph.nodes[node]
        labels.append(data.get("label", node))
    return " -> ".join(labels)


def entity_type_options():
    return ENTITY_TYPES.items()
