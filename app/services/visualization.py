from pathlib import Path

from pyvis.network import Network

from app.models import ENTITY_TYPES
from app.services.analysis import build_case_entity_graph


ENTITY_COLORS = {
    "phone": "#58a6ff",
    "upi": "#7ee787",
    "bank": "#f2cc60",
    "email": "#ff9b85",
    "ip": "#c9a5ff",
}


def generate_network_html(output_path, entity_types=None):
    graph = build_case_entity_graph(entity_types=entity_types)
    network = Network(
        height="720px",
        width="100%",
        bgcolor="#0b0f14",
        font_color="#d8dee9",
        notebook=False,
        cdn_resources="in_line",
    )
    network.force_atlas_2based(gravity=-58, central_gravity=0.012, spring_length=160, spring_strength=0.08)

    for node_id, data in graph.nodes(data=True):
        if data["kind"] == "case":
            network.add_node(
                node_id,
                label=data["label"],
                title=data["title"],
                shape="box",
                color={"background": "#1f6feb", "border": "#8b949e"},
                font={"size": 18, "face": "Inter"},
                margin=12,
            )
        else:
            entity_type = data.get("entity_type")
            network.add_node(
                node_id,
                label=data["label"],
                title=data["title"],
                shape="dot",
                size=18,
                color=ENTITY_COLORS.get(entity_type, "#8b949e"),
                group=ENTITY_TYPES.get(entity_type, entity_type),
                font={"size": 14, "face": "Inter"},
            )

    for source, target, data in graph.edges(data=True):
        network.add_edge(source, target, title=data.get("label"), label=data.get("label"), color="#30363d")

    network.set_options(
        """
        {
          "interaction": {"hover": true, "navigationButtons": true, "keyboard": true},
          "nodes": {"borderWidth": 1},
          "edges": {
            "font": {"size": 10, "color": "#8b949e", "strokeWidth": 0},
            "smooth": {"type": "continuous"}
          },
          "physics": {
            "stabilization": {"iterations": 160},
            "minVelocity": 0.75
          }
        }
        """
    )
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    network.write_html(str(output_path), open_browser=False)
    return output_path
