from datetime import date

from app import create_app
from app.models import Case, Entity, InvestigationNote, db


CASES = [
    {
        "case_id": "CASE-001",
        "fir_number": "FIR/142/2026",
        "complaint_date": date(2026, 5, 18),
        "fraud_type": "UPI refund fraud",
        "investigating_officer": "Inspector A. Verma",
        "status": "Active",
        "victim_name": "Redacted Victim A",
        "victim_contact": "+91-90000-11001",
        "investigation_notes": "Complainant reported payment redirection after receiving a refund support call.",
        "entities": [("phone", "+91-88220-44119"), ("upi", "supportdesk@upi"), ("bank", "ACCT-XX3921")],
    },
    {
        "case_id": "CASE-002",
        "fir_number": "FIR/151/2026",
        "complaint_date": date(2026, 5, 26),
        "fraud_type": "Loan application fraud",
        "investigating_officer": "SI N. Khan",
        "status": "Under Review",
        "victim_name": "Redacted Victim B",
        "victim_contact": "+91-90000-11002",
        "investigation_notes": "Victim was asked to pay processing fees through UPI collect requests.",
        "entities": [("phone", "+91-88220-44119"), ("upi", "loanverify@upi"), ("email", "kycdesk.secure@mail.example")],
    },
    {
        "case_id": "CASE-003",
        "fir_number": "FIR/166/2026",
        "complaint_date": date(2026, 6, 4),
        "fraud_type": "Marketplace advance payment fraud",
        "investigating_officer": "Inspector A. Verma",
        "status": "Active",
        "victim_name": "Redacted Victim C",
        "victim_contact": "+91-90000-11003",
        "investigation_notes": "Seller profile disappeared after advance payment confirmation.",
        "entities": [("upi", "loanverify@upi"), ("bank", "ACCT-XX3921"), ("ip", "103.88.44.21")],
    },
]


def seed():
    app = create_app()
    with app.app_context():
        if Case.query.count():
            print("Database already contains cases. Seed skipped.")
            return
        for item in CASES:
            entity_specs = item.pop("entities")
            case = Case(**item)
            db.session.add(case)
            for entity_type, value in entity_specs:
                entity = Entity.query.filter_by(entity_type=entity_type, value=value).first()
                if not entity:
                    entity = Entity(entity_type=entity_type, value=value)
                    db.session.add(entity)
                case.entities.append(entity)
            db.session.add(InvestigationNote(case=case, author=item["investigating_officer"], body="Initial entity correlation completed."))
        db.session.commit()
        print("Seeded LinkSutra investigation data.")


if __name__ == "__main__":
    seed()
