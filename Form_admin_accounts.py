from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.validators import Email
#  <---    Install wtforms email validation: pip install wtforms[email]    --->

class CreateAccountForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    role = RadioField('Role', choices=[('M', 'Member'), ('P', 'PWID'), ('C', 'Caregiver')], default='M')
    email = TextAreaField('Email (Optional)', [validators.Optional(), Email(message='Invalid email address')])
