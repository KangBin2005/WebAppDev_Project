from wtforms import Form, StringField, DateField, TimeField, TextAreaField, SelectField, validators

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


class CreateEnquiryForm(Form):
    name = StringField('Your Name', [
        validators.Length(min=1, max=100),
        validators.DataRequired()
    ])

    subject = SelectField('Subject', choices=[
        ('', 'Select a subject'),  # Default empty option
        ('Activity', 'Activity'),
        ('Technical Issues', 'Technical Issues'),
        ('Account Issues', 'Account Issues'),
        ('General Feedback / Concerns', 'General Feedback / Concerns'),
        ('Navigation Issues', 'Navigation Issues'),
        ('Others', 'Others')
    ], validators=[validators.DataRequired()])
    # ... other fields ...

    message = TextAreaField('Message', [
        validators.Length(min=1, max=1000),
        validators.DataRequired()
    ])