from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


case_entities = db.Table(
    "case_entities",
    db.Column("case_id", db.Integer, db.ForeignKey("case.id"), primary_key=True),
    db.Column("entity_id", db.Integer, db.ForeignKey("entity.id"), primary_key=True),
)


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class Case(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.String(48), unique=True, nullable=False, index=True)
    fir_number = db.Column(db.String(80), nullable=False, index=True)
    complaint_date = db.Column(db.Date, nullable=False)
    fraud_type = db.Column(db.String(120), nullable=False, index=True)
    investigating_officer = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="Active", index=True)
    victim_name = db.Column(db.String(120), nullable=False)
    victim_contact = db.Column(db.String(40), nullable=False)
    investigation_notes = db.Column(db.Text, default="")

    entities = db.relationship(
        "Entity",
        secondary=case_entities,
        back_populates="cases",
        lazy="selectin",
    )
    notes = db.relationship("InvestigationNote", back_populates="case", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Case {self.case_id}>"


class Entity(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(32), nullable=False, index=True)
    value = db.Column(db.String(255), nullable=False, index=True)
    label = db.Column(db.String(120), default="")
    metadata_text = db.Column("metadata", db.Text, default="")

    cases = db.relationship(
        "Case",
        secondary=case_entities,
        back_populates="entities",
        lazy="selectin",
    )

    __table_args__ = (db.UniqueConstraint("entity_type", "value", name="uq_entity_type_value"),)

    @property
    def type_label(self):
        return ENTITY_TYPES.get(self.entity_type, self.entity_type)

    def __repr__(self):
        return f"<Entity {self.entity_type}:{self.value}>"


class InvestigationNote(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("case.id"), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)

    case = db.relationship("Case", back_populates="notes")


ENTITY_TYPES = {
    # Cyber Fraud (5) - EXISTING
    "phone": "Phone Number",
    "upi": "UPI ID",
    "bank": "Bank Account",
    "email": "Email Address",
    "ip": "IP Address",
    
    # Vehicle/Property (3) - NEW
    "license_plate": "Vehicle Registration Number",
    "vin": "Vehicle Identification Number (VIN)",
    "address": "Physical Address",
    
    # Identity (4) - NEW
    "aadhaar": "Aadhaar / National ID",
    "passport": "Passport Number",
    "name": "Suspect / Person Name",
    "alias": "Alias / Nickname",
    
    # Physical Evidence (4) - NEW
    "weapon": "Weapon",
    "device": "Mobile Device / Gadget",
    "document": "Document / File",
    "serial_number": "Serial Number",
    
    # Witness (1) - NEW
    "witness": "Witness Information",
}


CASE_STATUSES = ("Active", "Under Review", "Closed")
