import decimal

from wtforms import Form, StringField, DateField, TimeField, TextAreaField, SelectField, DecimalField, validators

class CreateParticipantActivityForm(Form):
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


class ReplyParticipantEnquiryForm(CreateEnquiryForm):
    # Class-level field definition (required by WTForms)
    reply_text = TextAreaField('Staff Reply', [
        validators.Length(min=1, max=1000),
        validators.DataRequired()
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Modify existing fields
        self.name.render_kw = {'readonly': True}
        self.subject.render_kw = {'readonly': True}
        self.message.render_kw = {'readonly': True}

class CreateProductForm(Form):
    product = StringField('Product Name',[
        validators.length(min=1, max=20),
        validators.DataRequired()])
    description = TextAreaField('Description', [
        validators.Length(min=1, max=50),
    ])
    price = DecimalField('Price',
        places=2,
        rounding=decimal.ROUND_UP,
        validators=[validators.DataRequired()])
    image_url = StringField('Image URL', [
        validators.DataRequired()
    ])

# class CreateTransactionForm(Form):
