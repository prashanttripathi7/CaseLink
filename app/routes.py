from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, send_file, url_for

from .forms import CaseForm, DeleteForm, EntityForm, NoteForm
from .models import CASE_STATUSES, Case, Entity, InvestigationNote, db
from .services.analysis import (
    case_relationships,
    dashboard_metrics,
    entity_type_options,
    global_search,
    investigation_insights,
    repeat_entities,
)
from .services.reports import build_case_report
from .services.visualization import generate_network_html

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def dashboard():
    metrics = dashboard_metrics()
    recent_cases = Case.query.order_by(Case.created_at.desc()).limit(6).all()
    recent_notes = InvestigationNote.query.order_by(InvestigationNote.created_at.desc()).limit(6).all()
    alerts = repeat_entities(limit=6)
    insights = investigation_insights()
    return render_template(
        "dashboard.html",
        metrics=metrics,
        recent_cases=recent_cases,
        recent_notes=recent_notes,
        alerts=alerts,
        insights=insights,
    )


@main_bp.route("/workflow")
def workflow():
    return render_template("workflow.html")


@main_bp.route("/cases")
def case_list():
    status = request.args.get("status", "")
    query = Case.query
    if status:
        query = query.filter_by(status=status)
    cases = query.order_by(Case.updated_at.desc()).all()
    return render_template(
        "cases/list.html",
        cases=cases,
        status=status,
        status_options=CASE_STATUSES,
        delete_form=DeleteForm(),
    )


@main_bp.route("/cases/new", methods=["GET", "POST"])
def case_new():
    form = CaseForm()
    if form.validate_on_submit():
        case = Case()
        form.populate_obj(case)
        db.session.add(case)
        db.session.commit()
        flash("Investigation created.", "success")
        return redirect(url_for("main.case_detail", case_id=case.id))
    return render_template("cases/form.html", form=form, title="Create Investigation")


@main_bp.route("/cases/<int:case_id>")
def case_detail(case_id):
    case = Case.query.get_or_404(case_id)
    entity_form = EntityForm()
    note_form = NoteForm()
    delete_form = DeleteForm()
    relationships = case_relationships(case)
    return render_template(
        "cases/detail.html",
        case=case,
        entity_form=entity_form,
        note_form=note_form,
        delete_form=delete_form,
        relationships=relationships,
    )


@main_bp.route("/cases/<int:case_id>/edit", methods=["GET", "POST"])
def case_edit(case_id):
    case = Case.query.get_or_404(case_id)
    form = CaseForm(obj=case)
    if form.validate_on_submit():
        form.populate_obj(case)
        db.session.commit()
        flash("Investigation updated.", "success")
        return redirect(url_for("main.case_detail", case_id=case.id))
    return render_template("cases/form.html", form=form, title=f"Edit {case.case_id}")


@main_bp.route("/cases/<int:case_id>/delete", methods=["POST"])
def case_delete(case_id):
    case = Case.query.get_or_404(case_id)
    form = DeleteForm()
    if not form.validate_on_submit():
        flash("Unable to delete investigation. Please try again.", "danger")
        return redirect(url_for("main.case_detail", case_id=case.id))

    case_label = case.case_id
    linked_entities = list(case.entities)
    case.entities.clear()
    db.session.delete(case)
    db.session.flush()

    for entity in linked_entities:
        if not entity.cases:
            db.session.delete(entity)

    db.session.commit()
    flash(f"Investigation {case_label} deleted.", "success")
    return redirect(url_for("main.case_list"))


@main_bp.route("/cases/<int:case_id>/entities", methods=["POST"])
def case_add_entity(case_id):
    case = Case.query.get_or_404(case_id)
    form = EntityForm()
    if form.validate_on_submit():
        value = form.value.data.strip()
        entity = Entity.query.filter_by(entity_type=form.entity_type.data, value=value).first()
        if not entity:
            entity = Entity(entity_type=form.entity_type.data, value=value)
            db.session.add(entity)
        entity.label = form.label.data or entity.label
        entity.metadata_text = form.metadata_text.data or entity.metadata_text
        if entity not in case.entities:
            case.entities.append(entity)
        db.session.commit()
        flash("Evidence linked to investigation.", "success")
    else:
        flash("Unable to add entity. Check required fields.", "danger")
    return redirect(url_for("main.case_detail", case_id=case.id))


@main_bp.route("/cases/<int:case_id>/entities/<int:entity_id>/remove", methods=["POST"])
def case_remove_entity(case_id, entity_id):
    case = Case.query.get_or_404(case_id)
    entity = Entity.query.get_or_404(entity_id)
    if entity in case.entities:
        case.entities.remove(entity)
        db.session.commit()
        flash("Evidence removed from investigation.", "success")
    return redirect(url_for("main.case_detail", case_id=case.id))


@main_bp.route("/entities/<int:entity_id>/edit", methods=["GET", "POST"])
def entity_edit(entity_id):
    entity = Entity.query.get_or_404(entity_id)
    form = EntityForm(obj=entity)
    if form.validate_on_submit():
        entity.entity_type = form.entity_type.data
        entity.value = form.value.data.strip()
        entity.label = form.label.data or ""
        entity.metadata_text = form.metadata_text.data or ""
        db.session.commit()
        flash("Entity updated.", "success")
        if entity.cases:
            return redirect(url_for("main.case_detail", case_id=entity.cases[0].id))
        return redirect(url_for("main.case_list"))
    return render_template("entity_form.html", form=form, entity=entity)


@main_bp.route("/cases/<int:case_id>/notes", methods=["POST"])
def case_add_note(case_id):
    case = Case.query.get_or_404(case_id)
    form = NoteForm()
    if form.validate_on_submit():
        db.session.add(InvestigationNote(case=case, author=form.author.data, body=form.body.data))
        db.session.commit()
        flash("Investigation note added.", "success")
    else:
        flash("Note requires officer and body.", "danger")
    return redirect(url_for("main.case_detail", case_id=case.id))


@main_bp.route("/search")
def search():
    term = request.args.get("q", "").strip()
    results = global_search(term)
    return render_template("search.html", term=term, results=results)


@main_bp.route("/network")
def network():
    selected_types = request.args.getlist("type")
    graph_file = Path(current_app.instance_path) / "network.html"
    generate_network_html(graph_file, entity_types=selected_types or None)
    has_network_data = bool(repeat_entities(limit=1))
    return render_template(
        "network.html",
        graph_file=graph_file.name,
        entity_types=entity_type_options(),
        selected_types=selected_types,
        has_network_data=has_network_data,
    )


@main_bp.route("/network/frame")
def network_frame():
    graph_file = Path(current_app.instance_path) / "network.html"
    if not graph_file.exists():
        generate_network_html(graph_file)
    return send_file(graph_file)


@main_bp.route("/cases/<int:case_id>/report")
def case_report(case_id):
    case = Case.query.get_or_404(case_id)
    path = build_case_report(case, current_app.config["REPORT_DIR"])
    return send_file(path, as_attachment=True, download_name=path.name)
