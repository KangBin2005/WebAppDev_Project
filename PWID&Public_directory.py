from flask import Flask, render_template, request, redirect, url_for, session, flash
import shelve, os, Participant_Enquiry, Public_Enquiry, Participant_Activity_Sign_Up
from datetime import date
from Forms import CreateParticipantEnquiryForm, CreatePublicEnquiryForm, CreateParticipantSignUpForm
from functools import wraps

app = Flask(__name__)
app.secret_key = 'fb814d13-2f3e-48b1-937b-ef33a4d35c18'

# PWID users:
# Amy: password
# Julie: password123
# mary: mary123

def login_required(f):
    @wraps(f)                                       # Prevent access if not logged in
    def custom_login(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return custom_login


# ========================
# Sample SG Enable Outlets Data
# ========================
outlets = {
    1: {
        'name': 'SG Enable Headquarters',
        'address': '20 Lengkok Bahru (Enabling Village), #01-01, Singapore 159053',
        'phone': '+65 6479 3700',
        'hours': 'Mon-Fri: 9am to 5.30pm',
        'wheelchair_accessible': True,
        'lat': '1.2875454',
        'lng': '103.8149975',
        'map_zoom': '17',
        'map_version': '1716905890037',
        'map_url': 'https://www.google.com/maps/place/SG+Enable/@1.2875508,103.8124226,17z/data=!3m1!4b1!4m6!3m5!1s0x31da19792f952f6d:0xb7db38a7c6c26ba1!8m2!3d1.2875454!4d103.8149975!16s%2Fg%2F1vg_9cwl?entry=ttu',
        'embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.669318672029!2d103.8124226!3d1.2875508!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31da19792f952f6d%3A0xb7db38a7c6c26ba1!2sSG%20Enable!5e0!3m2!1sen!2ssg!4v1716905890037!5m2!1sen!2ssg'
    },
    2: {
        'name': 'Toa Payoh Enable Hub',
        'address': '190 Lorong 6 Toa Payoh, #02-510, Singapore 310190',
        'phone': '+65 6123 4567',
        'hours': 'Mon-Fri: 9am-6pm',
        'wheelchair_accessible': True,
        'lat': '1.3345',
        'lng': '103.8568',
        'map_zoom': '7977.322862803088',
        'map_version': '1716905890037',
        'map_url': 'https://www.google.com/maps/place/190+Lor+6+Toa+Payoh,+%2302-510,+Singapore+310190',
        'embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.73834704838!2d103.854225!3d1.3345!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMcKwMjAnMDQuMiJOIDEwM8KwNTEnMjQuNSJF!5e0!3m2!1sen!2ssg!4v1716905890037!5m2!1sen!2ssg'
    },
    3: {
        'name': 'Bishan Enable Support Centre',
        'address': '51 Bishan Street 13, #01-01, Singapore 579799',
        'phone': '+65 6234 5678',
        'hours': 'Mon-Sat: 8am-7pm',
        'wheelchair_accessible': True,
        'lat': '1.3506',
        'lng': '103.8484',
        'map_zoom': '7977.322862803088',
        'map_version': '1716905890037',
        'map_url': 'https://www.google.com/maps/place/51+Bishan+St+13,+%2301-01,+Singapore+579799',
        'embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.584402768847!2d103.846212!3d1.3506!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMcKwMjEnMDIuMiJOIDEwM8KwNTAnNTQuMiJF!5e0!3m2!1sen!2ssg!4v1716905890037!5m2!1sen!2ssg'
    },
    4: {
        'name': 'Yishun Enable Care Centre',
        'address': '101 Yishun Ave 5, #03-01, Singapore 760101',
        'phone': '+65 6345 6789',
        'hours': 'Mon-Fri: 8:30am-5:30pm',
        'wheelchair_accessible': True,
        'lat': '1.4295',
        'lng': '103.8350',
        'map_zoom': '7977.322862803088',
        'map_version': '1716905890037',
        'map_url': 'https://www.google.com/maps/place/101+Yishun+Ave+5,+%2303-01,+Singapore+760101',
        'embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.263601270874!2d103.832812!3d1.4295!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMcKwMjUnNDYuMiJOIDEwM8KwNTAnMDYuMCJF!5e0!3m2!1sen!2ssg!4v1716905890037!5m2!1sen!2ssg'
    },
    5: {
        'name': 'Tampines Enable Hub',
        'address': '5 Tampines Central 6, #04-10, Singapore 529482',
        'phone': '+65 6456 7890',
        'hours': 'Mon-Sat: 9am-6pm',
        'wheelchair_accessible': True,
        'lat': '1.3536',
        'lng': '103.9386',
        'map_zoom': '7977.322862803088',
        'map_version': '1716905890037',
        'map_url': 'https://www.google.com/maps/place/5+Tampines+Central+6,+%2304-10,+Singapore+529482',
        'embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.678350727765!2d103.936412!3d1.3536!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMcKwMjEnMTMuMCJOIDEwM8KwNTYnMTkuMCJF!5e0!3m2!1sen!2ssg!4v1716905890037!5m2!1sen!2ssg'
    },
    6: {
        'name': 'Jurong East Enable Centre',
        'address': '135 Jurong Gateway Rd, #02-317, Singapore 600135',
        'phone': '+65 6567 8901',
        'hours': 'Mon-Fri: 8am-5pm',
        'wheelchair_accessible': True,
        'lat': '1.3333',
        'lng': '103.7426',
        'map_zoom': '7977.322862803088',
        'map_version': '1716905890037',
        'map_url': 'https://www.google.com/maps/place/135+Jurong+Gateway+Rd,+%2302-317,+Singapore+600135',
        'embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.917197049249!2d103.740412!3d1.3333!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMcKwMTknNTkuOSJOIDEwM8KwNDQnMzMuNCJF!5e0!3m2!1sen!2ssg!4v1716905890037!5m2!1sen!2ssg'
    }
}
def sync_public_enquiry_id():
    try:
        db = shelve.open('storage/public_enquiries_storage.db', 'r')
        enquiries_dict = db['Public_Enquiries']
        max_id = max(enquiry.get_enquiry_id() for enquiry in enquiries_dict.values())
        Public_Enquiry.PublicEnquiry.count_id = max_id
        db.close()
    except KeyError:
        # 'Participant_Enquiries' key doesn't exist in the shelve yet / No enquiries exist
        Participant_Enquiry.ParticipantEnquiry.count_id = 0
    except Exception as e:
        print("Error syncing enquiry ID:", e)

def sync_participant_activity_signup_id():
    try:
        db = shelve.open('storage/activity_signups.db', 'r')
        signups_dict = db['Activity_Signups']
        max_id = max(signup.get_signup_id() for signup in signups_dict.values())
        Participant_Activity_Sign_Up.ParticipantActivitySignUp.count_id = max_id
        db.close()
    except KeyError:
        # 'Activity_Signups' key doesn't exist in the shelve yet / No sign ups exist
        Participant_Activity_Sign_Up.ParticipantActivitySignUp.count_id = 0
    except Exception as e:
        print("Error syncing enquiry ID:", e)

def sync_participant_enquiry_id():
    try:
        db = shelve.open('storage/participant_enquiries_storage.db', 'r')
        enquiries_dict = db['Participant_Enquiries']
        max_id = max(enquiry.get_enquiry_id() for enquiry in enquiries_dict.values())
        Participant_Enquiry.ParticipantEnquiry.count_id = max_id
        db.close()
    except KeyError:
        # 'Participant_Enquiries' key doesn't exist in the shelve yet / No enquiries exist
        Participant_Enquiry.ParticipantEnquiry.count_id = 0
    except Exception as e:
        print("Error syncing enquiry ID:", e)
# ========================
# Public Routes (main site)
# ========================
@app.route('/')
def public_home():
    return render_template('Public/home.html', current_page='public_home')

@app.route('/about')
def public_about():
    return render_template('Public/about.html', current_page='public_about')

@app.route('/activities')
def public_activities():
    return render_template('Public/activities.html', current_page='public_activities')

@app.route('/contact')
def public_contact():
    return render_template('Public/contact_us.html', current_page='public_contact')

@app.route('/contact/enquiries', methods=['GET', 'POST'])
def public_enquiries():
    sync_public_enquiry_id()
    create_enquiry_form = CreatePublicEnquiryForm(request.form)

    # Handle form submission
    if request.method == 'POST' and create_enquiry_form.validate():
        enquiries_dict = {}
        db = shelve.open('storage/public_enquiries_storage.db', 'c')
        try:
            enquiries_dict = db['Public_Enquiries']
        except:
            print("Error in retrieving Participant_Enquiries from shelve.")

        new_enquiry = Public_Enquiry.PublicEnquiry(
            name=create_enquiry_form.name.data,
            email=create_enquiry_form.email.data,
            subject=create_enquiry_form.subject.data,
            message=create_enquiry_form.message.data,
            status="Pending"
        )

        enquiries_dict[new_enquiry.get_enquiry_id()] = new_enquiry
        db['Public_Enquiries'] = enquiries_dict
        db.close()
        return redirect(url_for('public_enquiries'))
    return render_template('Public/contact_enquries.html',
                           current_page='public_enquiries',
                           form=create_enquiry_form)

@app.route('/contact/locations')
def public_locations():
    return render_template('Public/contact_locations.html',
                           outlets=outlets,
                           current_page='public_locations')

@app.route('/contact/locations/<int:outlet_id>')
def public_contact_outlet_map(outlet_id):
    outlet = outlets.get(outlet_id)
    if not outlet:
        return redirect(url_for('public_locations'))


    return render_template('Public/contact_location_map.html',
                           outlet=outlet,
                           current_page='public_contact_outlet_map')

@app.route('/contact/faq')
def public_faq():
    return render_template('Public/contact_faq.html', current_page='public_faq')

@app.route('/donations')
def public_donations():
    product_list = []
    try:
        if os.path.exists('storage/storage_products.db'):  # Check if .db actually exists
            with shelve.open('storage/storage_products.db', flag='r') as productdb:
                products_dict = productdb.get('product', {})
                product_list = list(products_dict.values())


    except Exception as e:
        print(f"Error reading product database: {e}")
        # You can also log this error or flash a message

    return render_template('Public/donations.html', current_page='public_donations',product_list=product_list)

# ========================
# Participant Routes (under /participants/)
# ========================
@app.route('/participants/home')
@login_required
def participant_home():
    try:
        # Get today's date
        today = date.today()

        # Open the shelve database
        with shelve.open('storage/participant_activity_storage.db', 'r') as db:
            activities_dict = db.get('Activities', {})

            # Filter upcoming activities (today or future)
            upcoming = [
                a for a in activities_dict.values()
                if a.get_date() >= today
            ]

            # Sort by date (earliest first) and take first 3
            upcoming_activities = sorted(
                upcoming,
                key=lambda x: x.get_date()
            )[:3]

            return render_template(
                'PWIDS/home.html',
                current_page='participant_home',
                upcoming_activities=upcoming_activities
            )

    except Exception as e:
        print(f"Error accessing activity database: {str(e)}")
        return render_template(
            'PWIDS/home.html',
            current_page='participant_home',
            upcoming_activities=[]
        )

@app.route('/participants/my-activities', methods=['GET'])
@login_required
def participant_activities():
    try:
        # Get filter parameters
        activity_name_filter = request.args.get('activity_name', '')
        location_filter = request.args.get('location', '')

        with shelve.open('storage/participant_activity_storage.db', 'r') as db:
            activities_dict = db.get('Activities', {})
            all_activities = list(activities_dict.values())

            # Get user's registered activities
            username = session.get('user')
            registered_activity_ids = set()
            with shelve.open('storage/activity_signups.db', 'r') as signups_db:
                signups_dict = signups_db.get('Activity_Signups', {})
                for signup in signups_dict.values():
                    if signup.get_name() == username:
                        registered_activity_ids.add(signup.get_activity_id())

            # Split activities into upcoming and registered
            upcoming_activities = []
            registered_activities = []

            today = date.today()

            for activity in all_activities:
                # Apply filters
                if (activity_name_filter and activity.get_name() != activity_name_filter) or \
                        (location_filter and activity.get_venue() != location_filter):
                    continue

                # Registered activities (regardless of date)
                if activity.get_activity_id() in registered_activity_ids:
                    registered_activities.append(activity)
                # Upcoming activities (future only + not registered)
                elif activity.get_date() >= today:
                    upcoming_activities.append(activity)

            # Sort activities by date
            upcoming_activities.sort(key=lambda x: x.get_date())
            registered_activities.sort(key=lambda x: x.get_date())

            # Get all unique activity names and venues for filters
            activity_names = sorted({a.get_name() for a in all_activities})
            venues = sorted({a.get_venue() for a in all_activities})

            return render_template(
                'PWIDS/my_activities.html',
                current_page='participant_activities',
                upcoming_activities=upcoming_activities,
                registered_activities=registered_activities,
                activity_names=activity_names,
                venues=venues,
                selected_activity=activity_name_filter,
                selected_location=location_filter
            )

    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template(
            'PWIDS/my_activities.html',
            current_page='participant_activities',
            upcoming_activities=[],
            registered_activities=[],
            activity_names=[],
            venues=[],
            selected_activity='',
            selected_location=''
        )


@app.route('/activity/<int:activity_id>/signup', methods=['GET', 'POST'])
@login_required
def activity_signup(activity_id):
    # Sync ID counter
    sync_participant_activity_signup_id()

    # Initialize form
    signup_form = CreateParticipantSignUpForm(request.form)

    # Get activity
    try:
        with shelve.open('storage/participant_activity_storage.db', 'r') as db:
            activities_dict = db.get('Activities', {})
            activity = activities_dict.get(activity_id)
            if not activity:
                return redirect(url_for('participant_activities'))  # Silent redirect if activity not found
    except Exception as e:
        print(f"Error accessing activity data: {str(e)}")
        return redirect(url_for('participant_activities'))

    # Prefill name from logged-in user's session if GET request
    if request.method == 'GET':
        # Get username from session
        username = session.get('user', '')
        # Open user storage to get user details
        try:
            with shelve.open('storage/user_storage.db', 'r') as db:
                users_dict = db.get('Users', {})
                # Here you would need to modify to store more user details
                # Currently only stores username:password pairs
                # For now, we'll just use the username as the name
                signup_form.name.data = username
        except Exception as e:
            print(f"Error accessing user data: {str(e)}")
            # Continue without prefilling if there's an error

    if request.method == 'POST' and signup_form.validate():
        try:
            with shelve.open('storage/activity_signups.db', 'c') as db:
                signups_dict = db.get('Activity_Signups', {})

                new_signup = Participant_Activity_Sign_Up.ParticipantActivitySignUp(
                    name=signup_form.name.data,
                    phone=signup_form.phone.data,
                    email=signup_form.email.data,
                    accessibility_needs=signup_form.accessibility_needs.data,
                    emergency_contact_name=signup_form.emergency_contact_name.data,
                    emergency_phone=signup_form.emergency_phone.data,
                    activity_id=activity_id
                )

                signups_dict[new_signup.get_signup_id()] = new_signup
                db['Activity_Signups'] = signups_dict

                return redirect(url_for('participant_activities'))
        except Exception as e:
            print(f"Error saving signup: {str(e)}")
            # You could pass an error message to template if needed
            return render_template('PWIDS/activity_signup.html',
                                   form=signup_form,
                                   activity=activity,
                                   error="Failed to save signup",
                                   current_page='activity_signup')

    return render_template('PWIDS/activity_signup.html',
                           form=signup_form,
                           activity=activity,
                           current_page='activity_signup')

@app.route('/withdraw-participant-activity/<int:activity_id>', methods=['POST'])
@login_required
def withdraw_activity(activity_id):
    db = shelve.open('storage/activity_signups.db', 'w')
    signups_dict = db.get('Activity_Signups', {})

    username = session.get('user')

    # Find and remove the signup(s) for this user and activity
    signup_ids_to_remove = [
        signup_id for signup_id, signup in signups_dict.items()
        if signup.get_name() == username and signup.get_activity_id() == activity_id
    ]

    for signup_id in signup_ids_to_remove:
        signups_dict.pop(signup_id)

    db['Activity_Signups'] = signups_dict
    db.close()

    return redirect(url_for('participant_activities'))


@app.route('/participants/outlets')
@login_required
def participant_locations():
    return render_template('PWIDS/outlets.html',
                         outlets=outlets,
                         current_page='our_outlets')

@app.route('/participants/outlet/<int:outlet_id>')
@login_required
def outlet_map(outlet_id):
    outlet = outlets.get(outlet_id)
    if not outlet:
        return redirect(url_for('participant_locations'))


    return render_template('PWIDS/outlet_map.html',
                           outlet=outlet,
                           current_page='outlet_map')

@app.route('/participants/help', methods=['GET', 'POST'])
@login_required
def participant_help():
    sync_participant_enquiry_id()
    create_enquiry_form = CreateParticipantEnquiryForm(request.form)

    # Handle form submission
    if request.method == 'POST' and create_enquiry_form.validate():
        enquiries_dict = {}
        db = shelve.open('storage/participant_enquiries_storage.db', 'c')
        try:
            enquiries_dict = db.get('Participant_Enquiries', {})
        except:
            print("Error in retrieving Participant_Enquiries from shelve.")

        new_enquiry = Participant_Enquiry.ParticipantEnquiry(
            name=create_enquiry_form.name.data,
            subject=create_enquiry_form.subject.data,
            message=create_enquiry_form.message.data,
            status="Pending"
        )

        enquiries_dict[new_enquiry.get_enquiry_id()] = new_enquiry
        db['Participant_Enquiries'] = enquiries_dict
        db.close()
        return redirect(url_for('participant_help', show_enquiries=1))

    # Handle GET requests
    selected_subject = request.args.get('subject', '')
    selected_status = request.args.get('status', '')
    show_enquiries = request.args.get('show_enquiries', default=0, type=int)

    enquiries = []
    try:
        with shelve.open('storage/participant_enquiries_storage.db', 'r') as db:
            all_enquiries = list(db.get('Participant_Enquiries', {}).values())

            for enquiry in all_enquiries:
                subject_match = not selected_subject or enquiry.get_subject() == selected_subject
                status_match = not selected_status or enquiry.get_status() == selected_status
                if subject_match and status_match:
                    enquiries.append(enquiry)

            enquiries.sort(key=lambda x: x.get_enquiry_id())
    except Exception as e:
        print(f"Error loading enquiries: {str(e)}")

    # Defined subject and status field data
    subjects = ['Activity', 'Technical Issues', 'Account Issues',
                'General Feedback / Concerns', 'Navigation Issues', 'Others']
    statuses = ['Pending', 'Replied']

    return render_template('PWIDS/help.html',
                           form=create_enquiry_form,
                           enquiries=enquiries,
                           count=len(all_enquiries),
                           selected_subject=selected_subject,
                           selected_status=selected_status,
                           show_enquiries=show_enquiries,
                           subjects=subjects,
                           statuses=statuses,
                           current_page='participant_help'
                           )

@app.route('/update_participant_enquiry/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_participant_enquiry(id):
    update_participant_enquiry_form = CreateParticipantEnquiryForm(request.form)
    if request.method == "POST" and update_participant_enquiry_form.validate():
        db = shelve.open('storage/participant_enquiries_storage.db', 'w')
        enquiries_dict = db['Participant_Enquiries']

        enquiry = enquiries_dict.get(id)
        enquiry.set_name(update_participant_enquiry_form.name.data)
        enquiry.set_subject(update_participant_enquiry_form.subject.data)
        enquiry.set_message(update_participant_enquiry_form.message.data)

        db['Participant_Enquiries'] = enquiries_dict
        db.close()
        return redirect(url_for('participant_help', show_enquiries=1))
    else:
        db = shelve.open('storage/participant_enquiries_storage.db', 'r')
        enquiries_dict = db['Participant_Enquiries']
        db.close()

        enquiry = enquiries_dict.get(id)
        update_participant_enquiry_form.name.data = enquiry.get_name()
        update_participant_enquiry_form.subject.data = enquiry.get_subject()
        update_participant_enquiry_form.message.data = enquiry.get_message()
        return render_template('PWIDS/update_enquiry.html', form=update_participant_enquiry_form)

@app.route('/delete_participant_enquiry/<int:id>', methods=['POST'])
@login_required
def delete_participant_enquiry(id):
    enquiries_dict = {}
    db = shelve.open('storage/participant_enquiries_storage.db', 'w')
    enquiries_dict = db['Participant_Enquiries']

    enquiries_dict.pop(id)
    db['Participant_Enquiries'] = enquiries_dict
    db.close()
    return redirect(url_for('participant_help', show_enquiries=1))

# ========================
# Login_Sign Up Routes
# ========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = shelve.open('storage/user_storage.db', 'c')
        users = db.get('Users', {})
        db.close()

        if username in users and users[username] == password:
            session['user'] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for('participant_home'))
        else:
            flash("Invalid username or password", "error")
    return render_template('Login_SignUp/login.html', current_page='login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_pw = request.form['confirm_password']


        db = shelve.open('storage/user_storage.db', writeback=True)
        users = db.get('Users', {})

        if username in users:
            flash('Username already taken.', 'error')
        elif password != confirm_pw:
            flash('Passwords do not match.', 'error')
        else:
            users[username] = password
            db['Users'] = users
            db.close()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))

        db.close()
    return render_template('Login_SignUp/signup.html', current_page='signup')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('public_home'))

if __name__ == '__main__':
    app.run(debug=True)
