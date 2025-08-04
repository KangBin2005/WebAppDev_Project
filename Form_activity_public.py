from wtforms import Form, StringField, TextAreaField, validators
from wtforms.fields import DateTimeLocalField
from datetime import datetime, timedelta

class CreateActivityForm(Form):
    activity_name = StringField('Activity Name', [validators.Length(min=1, max=100), validators.DataRequired()])
    activity_details = TextAreaField('Activity Details', [validators.Length(min=1, max=400), validators.DataRequired()])
    activity_start_datetime = DateTimeLocalField(
        'Activity Start',
        format='%Y-%m-%dT%H:%M',
        default=datetime.now,
        validators=[validators.DataRequired()]
    )
    activity_end_datetime = DateTimeLocalField(
        'Activity End',
        format='%Y-%m-%dT%H:%M',
        default=lambda: datetime.now() + timedelta(hours=1),    # <--- Adds 1 hour to current system time --->
        validators=[validators.DataRequired()]
    )