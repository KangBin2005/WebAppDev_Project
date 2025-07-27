from flask import Flask, render_template, request
import shelve
from datetime import date
app = Flask(__name__)

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

@app.route('/participants/locations')
def participant_locations():
    return render_template('PWIDS/locations.html', current_page='participant_locations')

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
