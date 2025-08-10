from flask import Flask, render_template, request, redirect, url_for, session, flash
import shelve, os, Participant_Enquiry, Public_Enquiry, Participant_Activity_Sign_Up
from datetime import date, datetime, timedelta

from Transaction import Transaction
from Forms import CreateParticipantEnquiryForm, CreatePublicEnquiryForm, CreateParticipantSignUpForm, CreateTransactionForm
from math import ceil
from functools import wraps

app = Flask(__name__)
app.secret_key = 'fb814d13-2f3e-48b1-937b-ef33a4d35c18'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)  # 10 minutes inactivity before timeout

# PWID users details:
# Amy: password
# Julie: "password123
# mary: mary123
# Karl: karl123


def login_required(f):
    @wraps(f)                                       # Prevent access if not logged in
    def custom_login(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return custom_login

# <-------- Sync ID Routes -------->
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

def sync_transaction_id():
    try:
        with shelve.open('storage/storage_transactions.db', 'r') as db:
            transactions_dict = db.get('transaction', {})
            max_id = max((transaction.get_transaction_id() for transaction in transactions_dict.values()), default=0)
            Transaction.count_id = max_id
            print(f"Synced transaction count_id: {Transaction.count_id}")
    except Exception as e:
        print("Error syncing transaction ID:", e)
        Transaction.count_id = 0

# ========================
# Public Routes (main site)
# ========================
@app.route('/')
def public_home():
    return render_template('Public/home.html', current_page='public_home')

@app.route('/about')
def public_about():
    return render_template('Public/about.html', current_page='public_about')

@app.route('/activities', methods=['GET', 'POST'])
def public_activities():
    # Get filter parameters
    selected_activity = request.args.get('activity', '')
    selected_venue = request.args.get('venue', '')
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Items per page

    # Open database
    db = shelve.open('storage/storage_activities.db', 'r')
    activities_dict = db.get('Activities', {})
    db.close()

    # Get all unique venues and activity names for dropdowns
    all_activities = list(activities_dict.values())
    venues = sorted({activity.get_activity_venue() for activity in all_activities})
    activity_names = sorted({activity.get_activity_name() for activity in all_activities})

    # Apply filters
    filtered_activities = []
    for activity in all_activities:
        activity_match = not selected_activity or activity.get_activity_name() == selected_activity
        venue_match = not selected_venue or activity.get_activity_venue() == selected_venue

        if activity_match and venue_match:
            filtered_activities.append(activity)

    # Sort by date (newest first)
    filtered_activities.sort(key=lambda x: x.get_activity_start_datetime(), reverse=True)

    # Pagination
    total = len(filtered_activities)
    pages = ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_activities = filtered_activities[start:end]

    return render_template(
        'Public/activities.html',
        current_page='public_activities',
        count=total,
        activities=paginated_activities,
        page=page,
        pages=pages,
        selected_activity=selected_activity,
        selected_venue=selected_venue,
        venues=venues,
        activity_names=activity_names
    )

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

# ========================
# Sample SG Enable Outlets Data for Public and Participants locations Route
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
# Get list of outlets
@app.route('/contact/locations')
def public_locations():
    return render_template('Public/contact_locations.html',
                           outlets=outlets,
                           current_page='public_locations')

# See Map based on the respective outlet address
@app.route('/contact/locations/<int:outlet_id>')
def public_contact_outlet_map(outlet_id):
    # Retrieve specific outlet by ID
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

@app.route('/donations/transaction_payment', methods=['GET', 'POST'])
def create_transaction():
    form = CreateTransactionForm(request.form)

    if request.method == 'POST' and form.validate():
        sync_transaction_id()
        Transaction.count_id += 1
        shared_transaction_id = Transaction.count_id

        cart = session.get('cart', {})
        if not cart:
            return "Cart is empty", 400

        with shelve.open('storage/storage_transactions.db', 'c') as db:
            transactions_dict = db.get('transaction', {})

            for pid, item in cart.items():
                new_transaction = Transaction(
                    product_id=pid,
                    product_name=item["name"],
                    quantity=item["quantity"],
                    price=item["price"],
                    customer_name=form.customer_name.data,
                    payment_type=form.payment_type.data,
                    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                # Set all transactions to share the same transaction id
                new_transaction._Transaction__transaction_id = shared_transaction_id
                transactions_dict[f"{shared_transaction_id}-{pid}"] = new_transaction

            db['transaction'] = transactions_dict
        return redirect(url_for('transaction_complete'))

    # For GET requests or invalid form, render the payment page
    return render_template('Public/transaction_payment.html', form=form)


@app.route('/donations/transaction_cart/transaction_complete')
def transaction_complete():
    session['cart'] = {}
    return render_template('Public/transaction_completion.html')

# ========================
# Transaction Cart Routes
# ========================
@app.route('/donations/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {
            'name': request.form['name'],
            'price': float(request.form['price']),
            'quantity': 1
        }

    session['cart'] = cart
    return redirect(request.referrer)

@app.route('/donations/transaction_cart')
def transaction_cart():
    cart = session.get('cart', {})
    print(cart)
    return render_template('Public/transaction_cart.html', cart=cart)

@app.route('/donations/transaction_cart/update_quantity/<product_id>/<action>', methods=['POST'])
def update_quantity(product_id, action):
    cart = session.get('cart', {})
    pid = str(product_id)  # Make sure to use string keys

    if pid in cart:
        if action == 'increase':
            cart[pid]['quantity'] += 1
        elif action == 'decrease':
            cart[pid]['quantity'] -= 1
            if cart[pid]['quantity'] <= 0:
                del cart[pid]

        session['cart'] = cart

    return redirect(url_for('transaction_cart'))


@app.route('/donations/transaction_cart/remove_item/<product_id>', methods=['POST'])
def remove_item(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
    session['cart'] = cart
    return redirect(url_for('transaction_cart'))

# ========================
# Participants Routes
# ========================

@app.route('/participants/home')
@login_required
def participant_home():
    activities_dict = {}
    db = shelve.open('storage/participant_activity_storage.db', 'r')
    activities_dict = db['Activities']
    db.close()

    today = date.today()
    upcoming_activities = []

    for key in activities_dict:
        activity = activities_dict.get(key)
        if activity.get_date() >= today:
            upcoming_activities.append(activity)

    upcoming_activities.sort(key=lambda x: x.get_date())
    upcoming_activities = upcoming_activities[:3]

    return render_template(
        'PWIDS/home.html',
        current_page='participant_home',
        upcoming_activities=upcoming_activities
    )

@app.route('/participant_activities')
def participant_activities():
    try:
        # Get filter parameters from URL
        activity_name_filter = request.args.get('activity_name', '')
        location_filter = request.args.get('location', '')

        # Open activities database
        activities_db = shelve.open('storage/participant_activity_storage.db', 'r')
        activities_dict = activities_db['Activities']
        activities_db.close()

        # Open signups database
        signups_db = shelve.open('storage/activity_signups.db', 'r')
        signups_dict = signups_db['Activity_Signups']
        signups_db.close()

        # Get current user
        username = session.get('user')

        # Find which activities user has registered for
        registered_ids = set()
        for signup in signups_dict.values():
            if signup.get_name() == username:
                registered_ids.add(signup.get_activity_id())

        # Categorize activities
        today = date.today()
        upcoming = []
        registered = []

        for activity in activities_dict.values():
            # Skip if doesn't match filters
            if (activity_name_filter and activity.get_name() != activity_name_filter) or \
                    (location_filter and activity.get_venue() != location_filter):
                continue

            if activity.get_activity_id() in registered_ids:
                registered.append(activity)
            elif activity.get_date() >= today:
                upcoming.append(activity)

        # Sort by date
        upcoming.sort(key=lambda x: x.get_date())
        registered.sort(key=lambda x: x.get_date())

        # Get unique values for filters
        activity_names = sorted({a.get_name() for a in activities_dict.values()})
        venues = sorted({a.get_venue() for a in activities_dict.values()})

        return render_template(
            'PWIDS/my_activities.html',
            current_page='participant_activities',
            upcoming_activities=upcoming,
            registered_activities=registered,
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
    activity = None
    activity_db = shelve.open('storage/participant_activity_storage.db', 'r')
    try:
        activities_dict = activity_db['Activities']
        activity = activities_dict.get(activity_id)
    except:
        print("Error accessing activity data")
    finally:
        activity_db.close()

    if not activity:
        return redirect(url_for('participant_activities'))

    # Prefill name from logged-in user if GET request
    if request.method == 'GET':
        username = session.get('user', '')
        user_db = shelve.open('storage/user_storage.db', 'r')
        try:
            users_dict = user_db['Users']
            signup_form.name.data = username
        except:
            print("Error accessing user data")
        finally:
            user_db.close()

    # Handle form submission
    if request.method == 'POST' and signup_form.validate():
        signups_dict = {}
        signup_db = shelve.open('storage/activity_signups.db', 'c')

        try:
            signups_dict = signup_db['Activity_Signups']

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
            signup_db['Activity_Signups'] = signups_dict

            return redirect(url_for('participant_activities'))
        except:
            print("Error saving signup")
            return render_template('PWIDS/activity_signup.html',
                                   form=signup_form,
                                   activity=activity,
                                   error="Failed to save signup",
                                   current_page='activity_signup')
        finally:
            signup_db.close()

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
    # Sync ID and initialize form
    sync_participant_enquiry_id()
    create_enquiry_form = CreateParticipantEnquiryForm(request.form)
    username = session.get('user', '') #Get current logged in user

    # Prefill name for GET requests
    if request.method == 'GET':
        create_enquiry_form.name.data = username

    # Handle form submission (CREATE)
    if request.method == 'POST' and create_enquiry_form.validate():
        enquiries_dict = {}
        db = shelve.open('storage/participant_enquiries_storage.db', 'c')

        try:
            enquiries_dict = db['Participant_Enquiries']
        except:
            print("Error in retrieving Participant_Enquiries from shelve.")

        new_enquiry = Participant_Enquiry.ParticipantEnquiry(
            name=create_enquiry_form.name.data,
            subject=create_enquiry_form.subject.data,
            message=create_enquiry_form.message.data,
            status="Pending" # Default status after submitting enquiry
        )

        enquiries_dict[new_enquiry.get_enquiry_id()] = new_enquiry
        db['Participant_Enquiries'] = enquiries_dict
        db.close()
        return redirect(url_for('participant_help', show_enquiries=1))

    # Handle retrieving enquiries (READ)
    # Get filter parameters from URL
    selected_subject = request.args.get('subject', '') # Filter by subject
    selected_status = request.args.get('status', '') # Filter by status
    show_enquiries = request.args.get('show_enquiries', default=0, type=int) # Toggle display

    enquiries_dict = {}
    db = shelve.open('storage/participant_enquiries_storage.db', 'r')
    enquiries_dict = db['Participant_Enquiries']
    db.close()

    # Filtered Enquiries
    enquiries = []
    for key in enquiries_dict:
        enquiry = enquiries_dict.get(key)
        if enquiry.get_name() == username: # Only show current user's enquiries
            # Check if selected field matches
            subject_match = not selected_subject or enquiry.get_subject() == selected_subject
            status_match = not selected_status or enquiry.get_status() == selected_status
            if subject_match and status_match:
                enquiries.append(enquiry)

    # Sort enquiries by ID (chronological order)
    enquiries.sort(key=lambda x: x.get_enquiry_id())

    # Defined filter options
    subjects = ['Activity', 'Technical Issues', 'Account Issues',
                'General Feedback / Concerns', 'Navigation Issues', 'Others']
    statuses = ['Pending', 'Replied']

    return render_template('PWIDS/help.html',
                           form=create_enquiry_form,
                           enquiries=enquiries,
                           count=len(enquiries),
                           selected_subject=selected_subject,
                           selected_status=selected_status,
                           show_enquiries=show_enquiries,
                           subjects=subjects,
                           statuses=statuses,
                           current_page='participant_help')

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

@app.route('/participants/profile')
@login_required
def profile():
    return render_template('PWIDS/profile.html', current_page='profile')

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
            session.permanent = True  # Start inactivity tracking
            session['user'] = username
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

@app.route('/participants/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    username = session['user']

    if request.method == 'POST':
        current_pw = request.form['current_password']
        new_pw = request.form['new_password']
        confirm_pw = request.form['confirm_password']

        # Open database with writeback=True for proper saving
        db = shelve.open('storage/user_storage.db', writeback=True)
        users = db.get('Users', {})

        if username not in users:
            flash("User not found", "error")
        elif users[username] != current_pw:
            flash("Current password is incorrect.", "error")
        elif new_pw != confirm_pw:
            flash("New passwords do not match.", "error")
        else:
            # Update password and save to database
            users[username] = new_pw
            db['Users'] = users  # Explicitly save changes
            flash("Password updated successfully!", "success")
            db.close()  # Close database
            return redirect(url_for('participant_home'))

        db.close()  # Close database in all cases

    return render_template('PWIDS/change_password.html', current_page='change_password')

if __name__ == '__main__':
    app.run(debug=True)
