from flask import Flask, render_template, request, redirect, url_for
import shelve
from datetime import date
app = Flask(__name__)

# Sample outlet data (you might want to move this to a database)
outlets = {
    1: {
        'name': 'Evergreen Home',
        'address': '123 Harmony Street<br>Singapore 123456',
        'phone': '+65 6123 4567',
        'hours': 'Mon-Fri: 9am-6pm',
        'map_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.6783916679!2d103.8198!3d1.3521!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMcKwMjEnMDcuNiJOIDEwM8KwNDknMTEuMyJF!5e0!3m2!1sen!2ssg!4v1620000000000!5m2!1sen!2ssg',
        'wheelchair_accessible': True
    },
    2: {
        'name': 'Sunshine Center',
        'address': '456 Bright Avenue<br>Singapore 654321',
        'phone': '+65 6876 5432',
        'hours': 'Mon-Sat: 8am-7pm',
        'map_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.1234567890!2d103.7764!3d1.2966!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMcKwMTcnNDkuOSJOIDEwM8KwNDYnMzUuMSJF!5e0!3m2!1sen!2ssg!4v1620000000000!5m2!1sen!2ssg',
        'wheelchair_accessible': True
    }
}

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

@app.route('/contact/enquiries')
def public_enquiries():
    return render_template('Public/contact_enquries.html', current_page='public_enquiries')

@app.route('/contact/locations')
def public_locations():
    return render_template('Public/contact_locations.html', current_page='public_locations')

@app.route('/contact/faq')
def public_faq():
    return render_template('Public/contact_faq.html', current_page='public_faq')

@app.route('/donations')
def public_donations():
    return render_template('Public/donations.html', current_page='public_donations')

# ========================
# Participant Routes (under /participants/)
# ========================
@app.route('/participants/home')
def participant_home():
    try:
        # Get today's date
        today = date.today()

        # Open the shelve database
        with shelve.open('participant_activity_storage.db', 'r') as db:
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
def participant_activities():
    try:
        # Get filter parameters
        activity_name_filter = request.args.get('activity_name', '')
        location_filter = request.args.get('location', '')

        with shelve.open('participant_activity_storage.db', 'r') as db:
            activities_dict = db.get('Activities', {})

            # Get all unique activity names and venues
            all_activities = list(activities_dict.values())
            activity_names = sorted({a.get_name() for a in all_activities})
            venues = sorted({a.get_venue() for a in all_activities})

            # Filter activities
            filtered_activities = [
                a for a in all_activities
                if (not activity_name_filter or a.get_name() == activity_name_filter) and
                   (not location_filter or a.get_venue() == location_filter)
            ]

            # Sort by date (newest first)
            activities_list = sorted(
                filtered_activities,
                key=lambda x: x.get_date(),
                reverse=True
            )

            return render_template(
                'PWIDS/my_activities.html',
                current_page='participant_activities',
                activities_list=activities_list,
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
            activities_list=[],
            activity_names=[],
            venues=[],
            selected_activity='',
            selected_location=''
        )

@app.route('/participants/outlets')
def participant_locations():  # Renamed to match navbar
    return render_template('PWIDS/outlets.html',
                         outlets=outlets,
                         current_page='our_outlets')  # Keep current_page consistent

@app.route('/participants/outlet/<int:outlet_id>')
def outlet_map(outlet_id):
    outlet = outlets.get(outlet_id)
    if not outlet:
        return redirect(url_for('participant_locations'))
    return render_template('PWIDS/outlet_map.html',
                         outlet=outlet,
                         current_page='outlet_map')

@app.route('/participants/help')
def participant_help():
    return render_template('PWIDS/help.html', current_page='participant_help')

# ========================
# Login_Sign Up Routes
# ========================
@app.route('/login')
def login():
    return render_template('Login_SignUp/login.html', current_page='login')

@app.route('/signup')
def signup():
    return render_template('Login_SignUp/signup.html', current_page='signup')

if __name__ == '__main__':
    app.run(debug=True)
