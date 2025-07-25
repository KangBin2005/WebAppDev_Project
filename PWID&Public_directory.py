from flask import Flask, render_template

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
    return render_template('PWIDS/home.html', current_page='participant_home')

@app.route('/participants/my-activities')
def participant_activities():
    return render_template('PWIDS/my_activities.html', current_page='participant_activities')

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
