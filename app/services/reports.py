from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.services.analysis import case_relationships


def build_case_report(case, report_dir):
    report_dir = Path(report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{case.case_id}_investigation_report.pdf"

    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=14 * mm,
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Muted", parent=styles["Normal"], textColor=colors.HexColor("#4b5563")))
    story = [
        Paragraph("LinkSutra Investigation Report", styles["Title"]),
        Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}", styles["Muted"]),
        Spacer(1, 8),
    ]

    metadata = [
        ["Case ID", case.case_id],
        ["FIR Number", case.fir_number],
        ["Complaint Date", case.complaint_date.strftime("%d %b %Y")],
        ["Fraud Type", case.fraud_type],
        ["Investigating Officer", case.investigating_officer],
        ["Status", case.status],
        ["Victim", f"{case.victim_name} ({case.victim_contact})"],
    ]
    story += [Paragraph("Case Metadata", styles["Heading2"]), _table(metadata), Spacer(1, 8)]

    entity_rows = [[entity.type_label, entity.value, str(len(entity.cases))] for entity in case.entities]
    story += [Paragraph("Associated Entities", styles["Heading2"])]
    story.append(_table([["Type", "Value", "Linked Cases"]] + entity_rows) if entity_rows else Paragraph("No entities recorded.", styles["Normal"]))
    story.append(Spacer(1, 8))

    relationships = case_relationships(case)
    story += [Paragraph("Relationship Findings", styles["Heading2"])]
    if relationships["alerts"]:
        for alert in relationships["alerts"]:
            story.append(Paragraph(f"- {alert}", styles["Normal"]))
    else:
        story.append(Paragraph("No repeat entities or linked investigations detected for this case.", styles["Normal"]))

    if relationships["direct"]:
        rows = [["Entity", "Linked Cases"]]
        for item in relationships["direct"]:
            rows.append([item["entity"].value, ", ".join(c.case_id for c in item["cases"])])
        story += [Spacer(1, 6), Paragraph("Direct Links", styles["Heading3"]), _table(rows)]

    if relationships["indirect"]:
        story += [Spacer(1, 6), Paragraph("Indirect Network Paths", styles["Heading3"])]
        for item in relationships["indirect"]:
            story.append(Paragraph(item["path"], styles["Normal"]))

    story += [Spacer(1, 8), Paragraph("Investigation Notes", styles["Heading2"])]
    story.append(Paragraph(case.investigation_notes or "No investigation notes recorded.", styles["Normal"]))
    for note in sorted(case.notes, key=lambda n: n.created_at):
        story.append(Paragraph(f"{note.created_at.strftime('%d %b %Y')} - {note.author}: {note.body}", styles["Normal"]))

    doc.build(story)
    return path


def _table(rows):
    table = Table(rows, hAlign="LEFT", colWidths=[45 * mm, 95 * mm, 32 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table
