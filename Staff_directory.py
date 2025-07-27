from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateActivityForm
import shelve, Participant_Activity

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
    participants_activities_dict = {}
    db = shelve.open('participant_activity_storage.db', 'r')
    participants_activities_dict = db['Activities']
    db.close()

    activities_list = []
    for key in participants_activities_dict:
        activity = participants_activities_dict.get(key)
        activities_list.append(activity)
    return render_template('Staff/activity_participants.html',
   current_page='activity_participants', count = len(activities_list), activities_list = activities_list)

@app.route('/create-participant-activity', methods=['GET', 'POST'])
def create_participant_activity():
    create_participant_activity_form = CreateActivityForm(request.form)
    if request.method == 'POST' and create_participant_activity_form.validate():
        participants_activities_dict = {}
        db = shelve.open('participant_activity_storage.db', 'c')
        try:
            participants_activities_dict = db['Activities']
        except:
            print("Error in retrieving Activities from storage.db.")
        activity = Participant_Activity.ParticipantActivity(create_participant_activity_form.name.data,
            create_participant_activity_form.description.data,
            create_participant_activity_form.venue.data,
            create_participant_activity_form.date.data,
            create_participant_activity_form.start_time.data,
            create_participant_activity_form.end_time.data)
        participants_activities_dict[activity.get_activity_id()] = activity
        db['Activities'] = participants_activities_dict
        db.close()
        return redirect(url_for('activity_participants'))
    return render_template('Staff/create_activity_participant.html', form=create_participant_activity_form)

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

