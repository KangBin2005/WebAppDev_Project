from wtforms import Form, StringField, DateField, TimeField, TextAreaField, validators

class CreateActivityForm(Form):
    name = StringField('Activity Name', [
        validators.Length(min=1, max=150),
        validators.DataRequired()
    ])
    description = TextAreaField('Description', [
        validators.Length(min=1, max=500),
        validators.DataRequired()
    ])
    venue = StringField('Venue', [
        validators.Length(min=1, max=150),
        validators.DataRequired()
    ])
    date = DateField('Date', format='%Y-%m-%d', validators=[validators.DataRequired()])
    start_time = TimeField('Start Time', validators=[validators.DataRequired()])
    end_time = TimeField('End Time', validators=[validators.DataRequired()])