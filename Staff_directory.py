from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateActivityForm, ReplyParticipantEnquiryForm
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
    return render_template('Staff/create_participant_activity.html', form=create_participant_activity_form)

@app.route('/update-participant-activity/<int:id>/', methods=['GET', 'POST'])
def update_participant_activity(id):
    update_participant_activity_form = CreateActivityForm(request.form)
    if request.method == 'POST' and update_participant_activity_form.validate():
        activities_dict = {}
        db = shelve.open('participant_activity_storage.db', 'w')
        activities_dict = db['Activities']

        activity = activities_dict.get(id)
        activity.set_name(update_participant_activity_form.name.data)
        activity.set_description(update_participant_activity_form.description.data)
        activity.set_venue(update_participant_activity_form.venue.data)
        activity.set_date(update_participant_activity_form.date.data)
        activity.set_start_time(update_participant_activity_form.start_time.data)
        activity.set_end_time(update_participant_activity_form.end_time.data)

        db['Activities'] = activities_dict
        db.close()
        return redirect(url_for('activity_participants'))
    else:
        participants_activities_dict = {}
        db = shelve.open('participant_activity_storage.db', 'r')
        participants_activities_dict = db['Activities']
        db.close()

        activity = participants_activities_dict.get(id)
        update_participant_activity_form.name.data = activity.get_name()
        update_participant_activity_form.description.data = activity.get_description()
        update_participant_activity_form.venue.data = activity.get_venue()
        update_participant_activity_form.date.data = activity.get_date()
        update_participant_activity_form.start_time.data = activity.get_start_time()
        update_participant_activity_form.end_time.data = activity.get_end_time()

        return render_template('Staff/update_participant_activity.html',
                               form = update_participant_activity_form)

@app.route('/delete-participant-activity/<int:id>', methods=['POST'])
def delete_participant_activity(id):
    activities_dict = {}
    db = shelve.open('participant_activity_storage.db', 'w')
    activities_dict = db['Activities']

    activities_dict.pop(id)

    db['Activities'] = activities_dict
    db.close()

    return redirect(url_for('activity_participants'))

@app.route('/activity-management/public')
def activity_public():
    return render_template('Staff/activity_public.html', current_page='activity_public')

@app.route('/enquiry-management')
def manage_enquries():
    return render_template('Staff/enquiry_management.html', current_page='manage_enquires')


@app.route('/enquiry-management/participants')
def enquiry_participants():
    # Handle filter parameters
    selected_subject = request.args.get('subject', '')
    selected_status = request.args.get('status', '')

    # Initialize variables
    enquiries = []
    all_enquiries = []

    try:
        # Open the shelve database in read-only mode
        with shelve.open('participant_enquiries_storage.db', 'r') as db:
            # Retrieve all enquiries from the database
            all_enquiries = list(db.get('Participant_Enquiries', {}).values())

            # Apply filters if any
            for enquiry in all_enquiries:
                subject_match = not selected_subject or enquiry.get_subject() == selected_subject
                status_match = not selected_status or enquiry.get_status() == selected_status
                if subject_match and status_match:
                    enquiries.append(enquiry)

            # Sort enquiries by ID
            enquiries.sort(key=lambda x: x.get_enquiry_id())

    except Exception as e:
        print(f"Error loading enquiries: {str(e)}")

    # Define subject and status options (same as in participant_help)
    subjects = ['Activity', 'Technical Issues', 'Account Issues',
                'General Feedback / Concerns', 'Navigation Issues', 'Others']
    statuses = ['Pending', 'Replied']

    return render_template('Staff/enquiry_participants.html',
                           current_page='enquiry_participants',
                           enquiries=enquiries,
                           count=len(all_enquiries),
                           selected_subject=selected_subject,
                           selected_status=selected_status,
                           subjects=subjects,
                           statuses=statuses)


@app.route('/reply-participant-enquiry/<int:id>/', methods=['GET', 'POST'])
def participant_enquiry_reply(id):
    form = ReplyParticipantEnquiryForm(request.form)

    if request.method == 'POST' and form.validate():
        db = shelve.open('participant_enquiries_storage.db', 'w')
        enquiries_dict = db['Participant_Enquiries']
        enquiry = enquiries_dict.get(id)

        # Save reply and update status
        enquiry.set_reply(form.reply_text.data)
        enquiry.set_status("Replied")

        db['Participant_Enquiries'] = enquiries_dict
        db.close()

        # Redirect back to enquiries list with success
        return redirect(url_for('enquiry_participants'))

    # GET request - load existing enquiry
    db = shelve.open('participant_enquiries_storage.db', 'r')
    enquiry = db['Participant_Enquiries'].get(id)
    db.close()

    # Pre-fill form data
    form.name.data = enquiry.get_name()
    form.subject.data = enquiry.get_subject()
    form.message.data = enquiry.get_message()

    return render_template('Staff/participant_enquiry_reply.html', form=form)
@app.route('/enquiry-management/public')
def enquiry_public():
    return render_template('Staff/enquiry_public.html', current_page='enquiry_public')

if __name__ == '__main__':
    app.run(debug=True)

