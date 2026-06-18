from datetime import date

from app import create_app
from app.models import Case, Entity, InvestigationNote, db


DEMO_CASES = [
    {
        "case_id": "CASE-001",
        "fir_number": "FIR/001/2026",
        "complaint_date": date(2026, 6, 1),
        "fraud_type": "UPI refund fraud",
        "investigating_officer": "Inspector A. Verma",
        "status": "Active",
        "victim_name": "Demo Victim 1",
        "victim_contact": "+91-90000-10001",
        "investigation_notes": "Victim received a fake refund support call and was asked to approve a UPI collect request.",
        "entities": [
            ("phone", "+91-88220-44119", "Caller number", "Used by fake refund support agent"),
            ("upi", "refunddesk@upi", "Collection UPI", "UPI ID used to receive first payment"),
            ("bank", "ACCT-DEMO-3921", "Receiver account", "Account where funds were moved"),
            ("email", "support.refund@mail.example", "Fake support email", "Used in SMS/email follow-up"),
        ],
        "notes": [
            "Start demo here: CASE-001 is the first victim complaint.",
            "Shared phone number links this case to CASE-002.",
            "Shared bank account links this case to CASE-003.",
        ],
    },
    {
        "case_id": "CASE-002",
        "fir_number": "FIR/002/2026",
        "complaint_date": date(2026, 6, 2),
        "fraud_type": "Instant loan app fraud",
        "investigating_officer": "SI N. Khan",
        "status": "Under Review",
        "victim_name": "Demo Victim 2",
        "victim_contact": "+91-90000-10002",
        "investigation_notes": "Victim paid loan processing fees after receiving calls from a fake loan verification desk.",
        "entities": [
            ("phone", "+91-88220-44119", "Shared caller number", "Same phone as CASE-001"),
            ("upi", "loanverify@upi", "Loan fee UPI", "Used for processing fee collection"),
            ("email", "kycdesk.secure@mail.example", "KYC email", "Sent fake approval letter"),
            ("ip", "103.88.44.21", "Login IP", "Used for loan portal login"),
        ],
        "notes": [
            "CASE-002 proves the same number is being reused for another fraud type.",
            "The IP address links forward to CASE-003 and CASE-010.",
        ],
    },
    {
        "case_id": "CASE-003",
        "fir_number": "FIR/003/2026",
        "complaint_date": date(2026, 6, 3),
        "fraud_type": "Marketplace advance payment fraud",
        "investigating_officer": "Inspector A. Verma",
        "status": "Active",
        "victim_name": "Demo Victim 3",
        "victim_contact": "+91-90000-10003",
        "investigation_notes": "Victim paid advance for a vehicle listed online. Seller disappeared after payment.",
        "entities": [
            ("upi", "loanverify@upi", "Shared UPI", "Same UPI as CASE-002"),
            ("bank", "ACCT-DEMO-3921", "Shared receiver account", "Same bank account as CASE-001"),
            ("ip", "103.88.44.21", "Shared login IP", "Same IP as CASE-002"),
            ("license_plate", "MH-12-DE-9090", "Vehicle listing plate", "Plate displayed in marketplace listing"),
            ("vin", "VINDEMO2026MARKET01", "Vehicle VIN", "VIN shared in forged sale document"),
        ],
        "notes": [
            "CASE-003 is a bridge: it connects cyber payments to a vehicle listing.",
            "Use this case to explain how one case can join two investigation clusters.",
        ],
    },
    {
        "case_id": "CASE-004",
        "fir_number": "FIR/004/2026",
        "complaint_date": date(2026, 6, 4),
        "fraud_type": "Vehicle theft and resale",
        "investigating_officer": "PI S. Rao",
        "status": "Active",
        "victim_name": "Demo Victim 4",
        "victim_contact": "+91-90000-10004",
        "investigation_notes": "Stolen vehicle was found advertised using changed ownership documents.",
        "entities": [
            ("license_plate", "MH-12-DE-9090", "Shared vehicle plate", "Same plate seen in CASE-003"),
            ("vin", "VINDEMO2026MARKET01", "Shared VIN", "Same VIN seen in CASE-003"),
            ("name", "Rakesh Sharma", "Suspect name", "Name on forged sale form"),
            ("alias", "Raka", "Suspect alias", "Alias used by vehicle broker"),
            ("address", "Warehouse 17, Ring Road Industrial Area", "Storage address", "Location where vehicle was stored"),
        ],
        "notes": [
            "CASE-004 shows the vehicle evidence from CASE-003 was not isolated.",
            "The suspect alias connects this case to organized crime activity in CASE-007 and CASE-010.",
        ],
    },
    {
        "case_id": "CASE-005",
        "fir_number": "FIR/005/2026",
        "complaint_date": date(2026, 6, 5),
        "fraud_type": "Property rental deposit fraud",
        "investigating_officer": "SI M. Iyer",
        "status": "Under Review",
        "victim_name": "Demo Victim 5",
        "victim_contact": "+91-90000-10005",
        "investigation_notes": "Victim paid deposit for a fake rental property listing.",
        "entities": [
            ("address", "Warehouse 17, Ring Road Industrial Area", "Shared address", "Same address as CASE-004"),
            ("phone", "+91-77770-55001", "Rental listing phone", "Number used in property listing"),
            ("name", "Rakesh Sharma", "Shared suspect name", "Same name as CASE-004"),
            ("document", "RENT-AGREEMENT-DEMO-77", "Fake rental agreement", "Document shared with victim"),
        ],
        "notes": [
            "CASE-005 demonstrates address reuse across vehicle and property crime.",
            "The suspect name makes the link easy to explain to non-technical viewers.",
        ],
    },
    {
        "case_id": "CASE-006",
        "fir_number": "FIR/006/2026",
        "complaint_date": date(2026, 6, 6),
        "fraud_type": "Identity misuse in bank account opening",
        "investigating_officer": "Inspector P. Singh",
        "status": "Active",
        "victim_name": "Demo Victim 6",
        "victim_contact": "+91-90000-10006",
        "investigation_notes": "Victim identity documents were used to open mule accounts.",
        "entities": [
            ("aadhaar", "AADHAAR-DEMO-4455", "National ID", "Identity number used in account opening"),
            ("passport", "P-DEMO-778899", "Passport", "Passport scan found in document bundle"),
            ("name", "Meera Nair", "Identity holder", "Name used on account opening form"),
            ("bank", "ACCT-DEMO-8890", "Mule account", "New account opened with stolen identity"),
            ("document", "KYC-BUNDLE-DEMO-06", "KYC file", "Bundle of identity documents"),
        ],
        "notes": [
            "CASE-006 introduces identity evidence: Aadhaar, passport, KYC document, and mule bank account.",
            "The document bundle links to CASE-008.",
        ],
    },
    {
        "case_id": "CASE-007",
        "fir_number": "FIR/007/2026",
        "complaint_date": date(2026, 6, 7),
        "fraud_type": "Weapon seizure linked to extortion",
        "investigating_officer": "PI S. Rao",
        "status": "Active",
        "victim_name": "Demo Victim 7",
        "victim_contact": "+91-90000-10007",
        "investigation_notes": "Weapon and mobile devices were recovered during an extortion inquiry.",
        "entities": [
            ("weapon", "9mm pistol DEMO-WPN-19", "Recovered weapon", "Weapon seized during search"),
            ("serial_number", "SN-DEMO-556677", "Weapon serial", "Serial number on recovered weapon"),
            ("device", "IMEI-DEMO-990011223344", "Recovered phone", "Device recovered with suspect"),
            ("alias", "Raka", "Shared alias", "Same alias as CASE-004"),
            ("phone", "+91-77770-55001", "Shared contact number", "Same phone as CASE-005"),
        ],
        "notes": [
            "CASE-007 adds physical evidence and shows the same alias from vehicle theft.",
            "The recovered device links to CASE-009 and CASE-010.",
        ],
    },
    {
        "case_id": "CASE-008",
        "fir_number": "FIR/008/2026",
        "complaint_date": date(2026, 6, 8),
        "fraud_type": "Document forgery racket",
        "investigating_officer": "Inspector P. Singh",
        "status": "Under Review",
        "victim_name": "Demo Victim 8",
        "victim_contact": "+91-90000-10008",
        "investigation_notes": "Forged identity documents were found in multiple account opening packets.",
        "entities": [
            ("document", "KYC-BUNDLE-DEMO-06", "Shared KYC file", "Same bundle as CASE-006"),
            ("aadhaar", "AADHAAR-DEMO-4455", "Shared Aadhaar", "Same identity as CASE-006"),
            ("passport", "P-DEMO-778899", "Shared passport", "Same passport as CASE-006"),
            ("serial_number", "SN-DOC-PRINTER-2026", "Printer serial", "Serial number of printer used for forged IDs"),
            ("email", "kycdesk.secure@mail.example", "Shared KYC email", "Same email as CASE-002"),
        ],
        "notes": [
            "CASE-008 links identity misuse back to the loan fraud KYC email.",
            "This is useful for explaining indirect links across different crime categories.",
        ],
    },
    {
        "case_id": "CASE-009",
        "fir_number": "FIR/009/2026",
        "complaint_date": date(2026, 6, 9),
        "fraud_type": "Witness statement in missing person inquiry",
        "investigating_officer": "SI M. Iyer",
        "status": "Active",
        "victim_name": "Demo Victim 9",
        "victim_contact": "+91-90000-10009",
        "investigation_notes": "Witness reported seeing suspects near the warehouse address with a mobile device.",
        "entities": [
            ("witness", "Witness DEMO-WIT-09", "Primary witness", "Statement recorded under demo file"),
            ("address", "Warehouse 17, Ring Road Industrial Area", "Shared address", "Same location as CASE-004 and CASE-005"),
            ("device", "IMEI-DEMO-990011223344", "Shared device", "Same device as CASE-007"),
            ("name", "Meera Nair", "Person name", "Name mentioned in witness statement"),
        ],
        "notes": [
            "CASE-009 shows how witness information can connect physical location and device evidence.",
            "It also links the identity name from CASE-006 into the wider network.",
        ],
    },
    {
        "case_id": "CASE-010",
        "fir_number": "FIR/010/2026",
        "complaint_date": date(2026, 6, 10),
        "fraud_type": "Organized crime coordination",
        "investigating_officer": "DCP Demo Cell",
        "status": "Active",
        "victim_name": "Demo Victim 10",
        "victim_contact": "+91-90000-10010",
        "investigation_notes": "Analysis suggests one group is coordinating cyber fraud, vehicle resale, document forgery, and extortion.",
        "entities": [
            ("alias", "Raka", "Network alias", "Alias appears in CASE-004 and CASE-007"),
            ("ip", "103.88.44.21", "Shared IP", "Same IP as CASE-002 and CASE-003"),
            ("device", "IMEI-DEMO-990011223344", "Shared device", "Same device as CASE-007 and CASE-009"),
            ("phone", "+91-88220-44119", "Shared caller number", "Same number as CASE-001 and CASE-002"),
            ("bank", "ACCT-DEMO-8890", "Shared mule account", "Same account as CASE-006"),
        ],
        "notes": [
            "Use CASE-010 as the final reveal: it ties multiple evidence clusters into one organized network.",
            "Open the Network page after loading this data to show the connected graph.",
        ],
    },
]


def upsert_entity(entity_type, value, label="", metadata_text=""):
    entity = Entity.query.filter_by(entity_type=entity_type, value=value).first()
    if not entity:
        entity = Entity(entity_type=entity_type, value=value)
        db.session.add(entity)
    entity.label = label or entity.label
    entity.metadata_text = metadata_text or entity.metadata_text
    return entity


def remove_existing_demo_cases():
    demo_ids = [item["case_id"] for item in DEMO_CASES]
    for case in Case.query.filter(Case.case_id.in_(demo_ids)).all():
        linked_entities = list(case.entities)
        case.entities.clear()
        db.session.delete(case)
        db.session.flush()
        for entity in linked_entities:
            if not entity.cases:
                db.session.delete(entity)


def seed_demo_cases():
    app = create_app()
    with app.app_context():
        remove_existing_demo_cases()

        for item in DEMO_CASES:
            entity_specs = item["entities"]
            note_bodies = item["notes"]
            case = Case(
                case_id=item["case_id"],
                fir_number=item["fir_number"],
                complaint_date=item["complaint_date"],
                fraud_type=item["fraud_type"],
                investigating_officer=item["investigating_officer"],
                status=item["status"],
                victim_name=item["victim_name"],
                victim_contact=item["victim_contact"],
                investigation_notes=item["investigation_notes"],
            )
            db.session.add(case)

            for entity_type, value, label, metadata_text in entity_specs:
                case.entities.append(upsert_entity(entity_type, value, label, metadata_text))

            for body in note_bodies:
                db.session.add(InvestigationNote(case=case, author=item["investigating_officer"], body=body))

        db.session.commit()
        print("Loaded police demo cases CASE-001 to CASE-010.")
        print("Open http://127.0.0.1:5000/cases and http://127.0.0.1:5000/network")


if __name__ == "__main__":
    seed_demo_cases()
