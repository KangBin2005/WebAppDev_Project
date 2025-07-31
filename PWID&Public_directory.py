from flask import Flask, render_template, request, redirect, url_for
import shelve
from datetime import date
app = Flask(__name__)

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
