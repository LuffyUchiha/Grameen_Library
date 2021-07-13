from flask import *
from forms import AdminLoginForm
from get_values import get_donor_donations, get_active_volunteers, appreciate_volunteer, assign_volunteer

admin_ui = Blueprint('admin_ui', __name__)


@admin_ui.route("/admin", methods=['GET', 'POST'])
def admin_login_page():
    admin_form = AdminLoginForm()
    if admin_form.validate_on_submit():
        username = admin_form.username.data
        password = admin_form.password.data
        if password == 'pass':
            return redirect(url_for('admin_ui.admin_page', username=username))

    return render_template('roles/admin/admin_login_page.html', form=admin_form)


@admin_ui.route("/admin/<username>")
def admin_page(username):
    donation_list = get_donor_donations()
    volunteer_list = get_active_volunteers()
    return render_template('roles/admin/admin_page.html', username=username,
                           donation_list=zip(range(donation_list.__len__()), donation_list),
                           volunteer_list=zip(range(volunteer_list.__len__()), volunteer_list))


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

