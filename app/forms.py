from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, DateTimeField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Optional, Email, NumberRange
from datetime import datetime

class TeamMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact = StringField('Contact (email/phone)', validators=[Optional()])
    role = StringField('Role', validators=[Optional()])

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Short Description', validators=[Optional()])
    date = DateTimeField('Date & Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()], default=datetime.now)
    location = StringField('Location', validators=[Optional()])
    organizer = StringField('Organizer', validators=[Optional()])
    budget = FloatField('Budget (USD)', validators=[Optional(), NumberRange(min=0)])
    details = TextAreaField('Event Details (full description)', validators=[Optional()])
    
    # Team members – at least one entry but can add more
    team_members = FieldList(FormField(TeamMemberForm), min_entries=0)
    
    submit = SubmitField('Save')