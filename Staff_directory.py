from flask import Flask, render_template, request, redirect, url_for, flash, session
from Forms import CreateParticipantActivityForm, ReplyParticipantEnquiryForm, CreateProductForm
from Form_activity_public import CreateActivityForm
from Form_admin_accounts import CreateAccountForm
import shelve, Participant_Activity, Account, Activity_public, Product

from math import ceil
from datetime import timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = '8f5b21e9-9a55-4879-9218-57c9e81c01e1'           # Random UUIDv4 value
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)  # 10 minutes inactivity before timeout


users = {
    "Bob": "password",      # Example Staff
    "Mary": "password123"
}


# <-------- Misc management -------->

def login_required(f):
    @wraps(f)                                       # Prevent access if not logged in
    def custom_login(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return custom_login



def sync_account_id():
    try:
        db = shelve.open('storage_accounts.db', 'r')
        accounts_dict = db['Accounts']
        max_id = max(account.get_user_id() for account in accounts_dict.values())
        Account.Account.count_id = max_id
        db.close()
    except KeyError:
        # 'Accounts' key doesn't exist in the shelve yet / No accounts exist
        Account.Account.count_id = 0
    except Exception as e:
        print("Error syncing account ID:", e)



def sync_public_activity_id():
    try:
        db = shelve.open('storage_activities.db', 'r')
        activities_dict = db['Activities']
        max_id = max(activity.get_activity_id() for activity in activities_dict.values())
        Activity_public.ActivityPublic.count_id = max_id
        db.close()
    except KeyError:
        # 'Activities' key doesn't exist in the shelve yet / No activities exist
        Activity_public.ActivityPublic.count_id = 0
    except Exception as e:
        print("Error syncing activity ID:", e)


def sync_participant_activity_id():
    try:
        db = shelve.open('participant_activity_storage.db', 'r')
        participants_activities_dict = db['Activities']
        max_id = max(activity.get_activity_id() for activity in participants_activities_dict.values())
        Participant_Activity.ParticipantActivity.count_id = max_id
        db.close()
    except KeyError:
        # 'Activities' key doesn't exist in the shelve yet / No activities exist
        Participant_Activity.ParticipantActivity.count_id = 0
    except Exception as e:
        print("Error syncing activity ID:", e)


# <-------- Routes -------->


@app.route('/')
@login_required
def dashboard():
    return render_template('Staff/dashboard.html',
                           current_page='dashboard')


@app.route('/account-management', methods=['GET', 'POST'])
@login_required
def manage_accounts():
    search_query = request.args.get('search', '').lower()
    page = request.args.get('page', 1, type=int)
    per_page = 10


    db = shelve.open('storage_accounts.db', 'r')
    accounts_dict = db.get('Accounts', {})
    db.close()

    accounts_list = list(accounts_dict.values())

    if search_query:
        accounts_list = [
            account for account in accounts_list
            if search_query in account.get_first_name().lower() or search_query in account.get_last_name().lower()
        ]


    total = len(accounts_list)
    pages = ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_activities = accounts_list[start:end]
    return render_template('Staff/account_management.html',
                           current_page='account_management',
                           count=total,
                           page=page,
                           pages=pages,
                           accounts_list=paginated_activities,
                           search_query=search_query)


@app.route('/account-management/create', methods=['GET', 'POST'])
@login_required
def create_account():
    sync_account_id()

    create_account_form = CreateAccountForm(request.form)
    if request.method == 'POST' and create_account_form.validate():
        accounts_dict = {}
        db = shelve.open('storage_accounts.db', 'c')

        try:
            accounts_dict = db['Accounts']
        except Exception as e:
            print("Error in retrieving Users from storage_accounts.db.:", e)

        account = Account.Account(create_account_form.first_name.data,
                         create_account_form.last_name.data,
                         create_account_form.gender.data,
                         create_account_form.role.data,
                         create_account_form.email.data)
        accounts_dict[account.get_user_id()] = account
        db['Accounts'] = accounts_dict

        db.close()

        return redirect(url_for('manage_accounts'))
    return render_template('/Staff/account_create.html',
                           form=create_account_form,
                           current_page='account_create')


@app.route('/account-management/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_account(id):
    update_account_form = CreateAccountForm(request.form)
    if request.method == 'POST' and update_account_form.validate():
        accounts_dict = {}
        db = shelve.open('storage_accounts.db', 'w')
        accounts_dict = db['Accounts']

        account = accounts_dict.get(id)
        account.set_first_name(update_account_form.first_name.data)
        account.set_last_name(update_account_form.last_name.data)
        account.set_gender(update_account_form.gender.data)
        account.set_role(update_account_form.role.data)
        account.set_email(update_account_form.email.data)

        db['Accounts'] = accounts_dict
        db.close()

        return redirect(url_for('manage_accounts'))
    else:
        accounts_dict = {}
        db = shelve.open('storage_accounts.db', 'r')
        accounts_dict = db['Accounts']
        db.close()

        account = accounts_dict.get(id)
        update_account_form.first_name.data = account.get_first_name()
        update_account_form.last_name.data = account.get_last_name()
        update_account_form.gender.data = account.get_gender()
        update_account_form.role.data = account.get_role()
        update_account_form.email.data = account.get_email()

        return render_template('/Staff/account_update.html',
                               form=update_account_form,
                               current_page='account_update')


@app.route('/account-management/delete/<int:id>/', methods=['POST'])
@login_required
def delete_account(id):
    accounts_dict = {}
    db = shelve.open('storage_accounts.db', 'w')
    accounts_dict = db['Accounts']

    accounts_dict.pop(id)

    db['Accounts'] = accounts_dict
    db.close()
    return redirect(url_for('manage_accounts'))


@app.route('/activity-management/public', methods=['GET', 'POST'])
@login_required
def activity_public():
    search_query = request.args.get('search', '').lower()
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of activities per page

    db = shelve.open('storage_activities.db', 'r')
    activities_dict = db.get('Activities', {})
    db.close()

    activities_list = list(activities_dict.values())

    if search_query:                # for search filtering
        activities_list = [
            activity for activity in activities_list
            if search_query in activity.get_activity_name().lower()
        ]

    total = len(activities_list)
    pages = ceil(total / per_page) # round up to nearest integer
    start = (page - 1) * per_page
    end = start + per_page
    paginated_activities = activities_list[start:end]

    return render_template(
        'Staff/activity_public.html',
        current_page='activity_public',
        count=total,
        activities=paginated_activities,
        page=page,
        pages=pages,
        search_query=search_query)


@app.route('/activity-management/public/create', methods=['GET','POST'])
@login_required
def activity_public_create():
    sync_public_activity_id()

    create_activity_form = CreateActivityForm(request.form)
    if request.method == 'POST' and create_activity_form.validate():
        activities_dict = {}
        db = shelve.open('storage_activities.db', 'c')

        try:
            activities_dict = db['Activities']
        except Exception as e:
            print("Error in retrieving Users from storage_activities.db.:", e)

        activity = Activity_public.ActivityPublic(create_activity_form.activity_name.data,
                                                  create_activity_form.activity_details.data,
                                                  create_activity_form.activity_start_datetime.data,
                                                  create_activity_form.activity_end_datetime.data)

        activities_dict[activity.get_activity_id()] = activity
        db['Activities'] = activities_dict

        db.close()

        return redirect(url_for('activity_public'))
    return render_template('/Staff/activity_public_create.html',
                           form=create_activity_form,
                           current_page='activity_public_create')


@app.route('/activity-management/public/<int:id>/', methods=['GET', 'POST'])
@login_required
def activity_public_update(id):
    activity_form = CreateActivityForm(request.form)

    if request.method == 'POST' and activity_form.validate():
        db = shelve.open('storage_activities.db', 'w')
        activities_dict = db.get('Activities', {})

        activity = activities_dict.get(id)
        activity.set_activity_name(activity_form.activity_name.data)
        activity.set_activity_details(activity_form.activity_details.data)
        activity.set_activity_start_datetime(activity_form.activity_start_datetime.data)
        activity.set_activity_end_datetime(activity_form.activity_end_datetime.data)

        db['Activities'] = activities_dict
        db.close()

        return redirect(url_for('activity_public'))  # Change to your actual display function name

    else:
        db = shelve.open('storage_activities.db', 'r')
        activities_dict = db.get('Activities', {})
        db.close()

        activity = activities_dict.get(id)
        # if not activity:
        #     return "Activity not found", 404

        activity_form.activity_name.data = activity.get_activity_name()
        activity_form.activity_details.data = activity.get_activity_details()
        activity_form.activity_start_datetime.data = activity.get_activity_start_datetime()
        activity_form.activity_end_datetime.data = activity.get_activity_end_datetime()

        return render_template('/Staff/activity_public_update.html',
                               form=activity_form,
                               current_page='activity_public_update')


@app.route('/activity-management/delete/<int:id>/', methods=['POST'])
@login_required
def activity_public_delete(id):
    activities_dict = {}
    db = shelve.open('storage_activities.db', 'w')
    activities_dict = db['Activities']

    activities_dict.pop(id)

    db['Activities'] = activities_dict
    db.close()
    return redirect(url_for('activity_public'))


@app.route('/profile')
@login_required
def profile():
    return render_template('Staff/profile.html', current_page='profile')



# <-------- Staff (Participants) Done by Kang Bin -------->

@app.route('/activity-management/participants')
@login_required
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
   current_page='activity_participants',
                           count = len(activities_list),
                           activities_list = activities_list)


@app.route('/create-participant-activity', methods=['GET', 'POST'])
@login_required
def create_participant_activity():
    sync_participant_activity_id()
    create_participant_activity_form = CreateParticipantActivityForm(request.form)
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
    return render_template('Staff/create_participant_activity.html',
                           form=create_participant_activity_form,
                           current_page='create_participant_activity')


@app.route('/update-participant-activity/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_participant_activity(id):
    update_participant_activity_form = CreateParticipantActivityForm(request.form)
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
                               form = update_participant_activity_form,
                               current_page='update_participant_activity')


@app.route('/delete-participant-activity/<int:id>', methods=['POST'])
@login_required
def delete_participant_activity(id):
    activities_dict = {}
    db = shelve.open('participant_activity_storage.db', 'w')
    activities_dict = db['Activities']

    activities_dict.pop(id)

    db['Activities'] = activities_dict
    db.close()

    return redirect(url_for('activity_participants'))


# Retrieving Participants Enquiries as Staff
@app.route('/enquiry-management/participants')
@login_required
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
            # Retrieve all non-deleted enquiries
            all_enquiries = [
                e for e in db.get('Participant_Enquiries', {}).values()
                if not e.get_deleted_for_staff()
            ]

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

    # Define subject and status options
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
@login_required
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


@app.route('/staff-delete-enquiry/<int:id>', methods=['POST'])
@login_required
def staff_delete_participant_enquiry(id):
    try:
        with shelve.open('participant_enquiries_storage.db', 'w') as db:
            enquiries_dict = db.get('Participant_Enquiries', {})
            if id in enquiries_dict:
                enquiries_dict[id].set_deleted_for_staff(True)
                db['Participant_Enquiries'] = enquiries_dict
    except Exception as e:
        print(f"Error deleting enquiry: {str(e)}")

    return redirect(url_for('enquiry_participants'))

@app.route('/product/management')
@login_required
def manage_product():
    products_dict = {}
    productdb = shelve.open('storage_products.db', 'r')
    products_dict = productdb['product']
    productdb.close()

    product_list = []
    for product in products_dict:
        product = products_dict.get(product)
        product_list.append(product)
    return render_template('Staff/product_management.html',
                           current_page='store_management',
                           count = len(products_dict),
                           product_list = product_list)


@app.route('/store_management/product_management/create-product', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        # Save form data to shelf if successful
        product_dict = {}
        productdb = shelve.open('storage_products.db', 'c')
        try:
            product_dict = productdb['product']
        except:
            print("Error in retrieving products from storage_products.db.")
        new_product = Product.Product(
            create_product_form.product.data,
            create_product_form.description.data,
            create_product_form.price.data,
            create_product_form.image_url.data)
        product_dict[new_product.get_product_id()] = new_product
        productdb['product'] = product_dict

        productdb.close()
        print("Product created successfully")
        # Return user to management page
        return redirect(url_for('manage_product'))
    # If form unsuccessful / unfinished return user to form page
    return render_template('Staff/product_create.html', form=create_product_form)

@app.route('/enquiry-management')
def manage_enquiries():
    return render_template('Staff/enquiry_management.html', current_page='manage_enquiries')


@app.route('/enquiry-management/public')
def enquiry_public():
    return render_template('Staff/enquiry_public.html', current_page='enquiry_public')


@app.route('/store_management')
@login_required
def manage_store():
    return render_template('Staff/store_management.html', current_page='store_management')

# <-------- Login Routes -------->

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']         # Login details submitted to server
        password = request.form['password']

        if username in users and users[username] == password:
            session.permanent = True    # Start inactivity tracking
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('Login_SignUp/staff_login.html', current_page='login')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    username = session['user']

    if request.method == 'POST':
        current_pw = request.form['current_password']       # Retrieve form inputs
        new_pw = request.form['new_password']
        confirm_pw = request.form['confirm_password']

        if users[username] != current_pw:
            flash("Current password is incorrect.", "error")
        elif new_pw != confirm_pw:
            flash("New passwords do not match.", "error")
        else:
            users[username] = new_pw                        # updated password
            flash("Password updated successfully!", "success")
            return redirect(url_for('dashboard'))
    return render_template('Staff/change_password.html', current_page='change_password')


if __name__ == '__main__':
    app.run(debug=True)
