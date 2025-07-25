from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('Staff/dashboard.html', current_page='dashboard')

@app.route('/account-management')
def manage_accounts():
    return render_template('Staff/account_management.html', current_page='account_management')

@app.route('/activity-management')
def manage_activities():
    return render_template('Staff/activity_management.html', current_page='manage_activities')

@app.route('/activity-management/participants')
def activity_participants():
    return render_template('Staff/activity_participants.html', current_page='activity_participants')

@app.route('/activity-management/public')
def activity_public():
    return render_template('Staff/activity_public.html', current_page='activity_public')

@app.route('/enquiry-management')
def manage_enquries():
    return render_template('Staff/enquiry_management.html', current_page='manage_enquires')

@app.route('/enquiry-management/participants')
def enquiry_participants():
    return render_template('Staff/enquiry_participants.html', current_page='enquiry_participants')

@app.route('/enquiry-management/public')
def enquiry_public():
    return render_template('Staff/enquiry_public.html', current_page='enquiry_public')

if __name__ == '__main__':
    app.run(debug=True)

