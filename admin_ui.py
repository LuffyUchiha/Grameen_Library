from flask import *
from forms import AdminLoginForm
from get_values import add_panchayat, get_panchayats, get_books_list, get_donor_donations, get_active_volunteers, appreciate_volunteer, assign_volunteer

admin_ui = Blueprint('admin_ui', __name__)


@admin_ui.route("/admin", methods=['GET', 'POST'])
def admin_login_page():
    admin_form = AdminLoginForm()
    if admin_form.validate_on_submit():
        username = admin_form.username.data
        password = admin_form.password.data
        if password == 'pass':
            session['logged_in'] = True
            session['role'] = 'admin'
            return redirect(url_for('admin_ui.admin_page', username=username))

    return render_template('roles/admin/admin_login_page.html', form=admin_form)


@admin_ui.route("/admin/<username>")
def admin_page(username):
    if session['logged_in'] and session['role'] == 'admin':
        return render_template('roles/admin/admin_page.html', username=username)
    else:
        return redirect(url_for('ui.error_page'))


@admin_ui.route("/admin/<username>/manage_donation")
def admin_page_manage_donation(username):
    if session['logged_in'] and session['role'] == 'admin':
        donation_list = get_donor_donations()
        volunteer_list = get_active_volunteers()
        return render_template('roles/admin/admin_page_manage_donation.html', username=username,
                               donation_list=zip(range(donation_list.__len__()), donation_list),
                               volunteer_list=zip(range(volunteer_list.__len__()), volunteer_list))
    else:
        return redirect(url_for('ui.error_page'))


@admin_ui.route("/admin/<username>/collect_books")
def admin_page_collect_books(username):
    if session['logged_in'] and session['role'] == 'admin':
        books_list = get_books_list()
        return render_template('roles/admin/admin_page_manage_collection.html', username=username, books_list=books_list)
    else:
        return redirect(url_for('ui.error_page'))

@admin_ui.route("/admin/<username>/manage_panchayat", methods=['GET', 'POST'])
def admin_page_manage_panchayat(username):
    if session['logged_in'] and session['role'] == 'admin':
        if request.method == 'GET':
            panchayat_list = get_panchayats()
            return render_template('roles/admin/admin_page_manage_panchayat.html', username=username, panchayat_list=panchayat_list)
        if request.method == 'POST':
            village_name = request.form.get('village_name')
            panchayat_name = request.form.get('panchayat_name')
            village_address = request.form.get('village_address')
            poc_name = request.form.get('poc_name')
            poc_number = request.form.get('poc_number')
            poc_mail = request.form.get('poc_mail')
            # print(village_name, panchayat_name, village_address, poc_name, poc_mail,poc_number)
            state = add_panchayat(village_name, panchayat_name, village_address, poc_name, poc_mail,poc_number).get('state')
            if state == 'success':
                return "Success"
            else:
                return "Failed"
    else:
        return redirect(url_for('ui.error_page'))

@admin_ui.route("/admin/assign", methods=["POST"])
def assign():
    donor_details = eval(request.form['donor_details'])
    volunteer_details = eval(request.form['volunteer_details'])
    # print(donor_details, volunteer_details)
    donor_id = donor_details['id']
    volunteer_id = volunteer_details['id']
    donation_date = donor_details['donation_date']
    available_from = donor_details['available_from']
    available_till = donor_details['available_till']
    assign_volunteer(volunteer_id, donor_id, donation_date, available_from, available_till)
    return json.dumps(donor_details)

@admin_ui.route("/admin/appreciate_volunteer", methods=["POST"])
def appreciate():
    appreciation = request.form['appreciation']
    volunteer_id = request.form['volunteer_id']
    admin_name = request.form['admin_name']
    # print(appreciation, volunteer_id, admin_name)
    return appreciate_volunteer(volunteer_id, appreciation, admin_name)

