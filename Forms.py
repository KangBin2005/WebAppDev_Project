import decimal
from wtforms import Form, StringField, DateField, TimeField, TextAreaField, SelectField, DecimalField, DateTimeLocalField, RadioField, validators
from datetime import datetime, timedelta
from wtforms.validators import Email

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


class CreateParticipantEnquiryForm(Form):
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


class ReplyParticipantEnquiryForm(CreateParticipantEnquiryForm):
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
    image_name = StringField('Image Name', [
        validators.DataRequired()
    ])

class CreateActivityForm(Form):
    activity_name = StringField('Activity Name', [validators.Length(min=1, max=100), validators.DataRequired()])
    activity_details = TextAreaField('Activity Details', [validators.Length(min=1, max=400), validators.DataRequired()])
    activity_venue = StringField('Activity Venue', [validators.Length(min=1, max=100), validators.DataRequired()])
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


#  <---    Install wtforms email validation: pip install wtforms[email]    --->
class CreatePublicEnquiryForm(Form):
    name = StringField('Your Name', [
        validators.Length(min=1, max=100),
        validators.DataRequired()
    ])
    email = StringField('Your Email', [
        validators.Length(min=1, max=100),
        validators.DataRequired(),
        validators.Email(message='Please enter a valid email address')
    ])

    subject = SelectField('Subject', choices=[
        ('', 'Select a subject'),  # Default empty option
        ('Activity', 'Activity'),
        ('Payment Issues', 'Payment Issues'),
        ('Donations Matters', 'Donations Matters'),
        ('General Enquiry', 'General Enquiry'),
        ('Navigation Issues', 'Navigation Issues'),
        ('Others', 'Others')
    ], validators=[validators.DataRequired()])
    # ... other fields ...

    message = TextAreaField('Message', [
        validators.Length(min=1, max=1000),
        validators.DataRequired()
    ])


class CreateParticipantSignUpForm(Form):
    name = StringField('Full Name', [
        validators.length(min=1, max=150),
        validators.DataRequired(message="Full name is required.")
    ])

    phone = StringField('Phone Number', [
        validators.length(min=8, max=15, message="Phone number must be 8-15 digits."),
        validators.DataRequired()
    ])

    email = StringField('Email', [
        validators.Email(message="Invalid email address."),
        validators.Optional()
    ])

    accessibility_needs = TextAreaField('Optional: Accessibility Needs (e.g., wheelchair access)', [
        validators.Length(max=500, message="Cannot exceed 500 characters."),
        validators.Optional()
    ])

    emergency_contact_name = StringField('Emergency Contact Name', [
        validators.Length(min=1, max=150),
        validators.DataRequired(message="Emergency Contact's Full name is required.")
    ])

    emergency_phone = StringField('Emergency Contact Number', [
        validators.Length(min=8, max=15, message="Phone number must be 8-15 digits."),
        validators.DataRequired()
    ])
class CreateAccountForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    role = RadioField('Role', choices=[('M', 'Member'), ('P', 'PWID'), ('C', 'Caregiver')], default='M')
    email = TextAreaField('Email (Optional)', [validators.Optional(), Email(message='Invalid email address')])

class CreateTransactionForm(Form):
    customer_name = StringField('Customer Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    payment_type = SelectField('Payment Type',
        choices=[
        ('Debit Card', 'Debit Card'),
        ('Credit Card', 'Credit Card'),
        ('Apple Pay', 'Apple Pay'),
        ('Google Pay', 'Google Pay')
    ])