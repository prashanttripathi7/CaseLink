from datetime import date

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from .models import CASE_STATUSES, ENTITY_TYPES


class CaseForm(FlaskForm):
    case_id = StringField("Case ID", validators=[DataRequired(), Length(max=48)])
    fir_number = StringField("FIR Number", validators=[DataRequired(), Length(max=80)])
    complaint_date = DateField("Complaint Date", default=date.today, validators=[DataRequired()])
    fraud_type = StringField("Fraud Type", validators=[DataRequired(), Length(max=120)])
    investigating_officer = StringField("Investigating Officer", validators=[DataRequired(), Length(max=120)])
    status = SelectField("Status", choices=[(s, s) for s in CASE_STATUSES], validators=[DataRequired()])
    victim_name = StringField("Victim Name", validators=[DataRequired(), Length(max=120)])
    victim_contact = StringField("Victim Contact", validators=[DataRequired(), Length(max=40)])
    investigation_notes = TextAreaField("Investigation Notes", validators=[Optional()])
    submit = SubmitField("Save Investigation")


class EntityForm(FlaskForm):
    entity_type = SelectField("Evidence Type", choices=list(ENTITY_TYPES.items()), validators=[DataRequired()])
    value = StringField("Evidence Value", validators=[DataRequired(), Length(max=255)])
    label = StringField("Label (Optional)", validators=[Optional(), Length(max=120)])
    metadata_text = TextAreaField("Additional Metadata", validators=[Optional()])
    submit = SubmitField("Link Evidence")


class NoteForm(FlaskForm):
    author = StringField("Officer", validators=[DataRequired(), Length(max=120)])
    body = TextAreaField("Investigation Note", validators=[DataRequired()])
    submit = SubmitField("Add Note")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
