from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from flask import *
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
from time import sleep
import requests
import datetime
from mpldatacursor import datacursor

from forms import *
from get_values import *

site_name = "http://localhost:5000"

ui = Blueprint('ui', __name__)

plt.style.use('ggplot')





# Adresses to the static pages

@ui.route("/about_grameen_library")
def about_page():
    return render_template('text_only/about_page.html')


@ui.route("/about_donation")
def donation_info_page():
    return render_template('text_only/donation_info.html')


@ui.route("/about_how_to_use")
def library_info_page():
    return render_template('text_only/library_info.html')


@ui.route("/", methods=['GET', 'POST'])
@ui.route("/landing_page", methods=['GET', 'POST'])
def landing_page():
    login_form = LandingPageLoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        res = login_response(username, password)
        if res['Response']:
            if res['Role'] == 'donor':  # Role = 2 => Donor
                session['logged_in'] = True
                session['role'] = 'donor'
                return redirect(url_for('donor_ui.donor_page', user_id=res['ID'], username=res['Name']))
            elif res['Role'] == 'panchayat':  # Role = 3 => Panchayat
                session['logged_in'] = True
                session['role'] = 'panchayat'
                return redirect(url_for('panchayat_page', user_id=res['ID'], username=res['Name']))
            elif res['Role'] == 'user':  # Role = 4 => User
                session['logged_in'] = True
                session['role'] = 'user'
                return redirect(url_for('user_ui.user_page', user_id=res['ID'], username=res['Name']))
            elif res['Role'] == 'volunteer':  # Role = 5 => Volunteer
                session['logged_in'] = True
                session['role'] = 'volunteer'
                return redirect(url_for('volunteer_ui.volunteer_page', user_id=res['ID'], username=res['Name']))
        else:
            flash(message='Incorrect credentials, please try again', category='danger')
    return render_template('landing_page.html', form=login_form)


# --------------------------------------------------#
# Back end related part of the code
# --------------------------------------------------#

# donor stuff



# volunteer stuff




# admin stuff

@ui.route("/admin", methods=['GET', 'POST'])
def admin_login_page():
    admin_form = AdminLoginForm()
    if admin_form.validate_on_submit():
        username = admin_form.username.data
        password = admin_form.password.data
        if password == 'pass':
            return redirect(url_for('admin_page', username=username))

    return render_template('roles/admin/admin_login_page.html', form=admin_form)


@ui.route("/admin/<username>")
def admin_page(username):
    return render_template('roles/admin/admin_page.html', username=username)


# panchayat stuff

@ui.route("/panchayat/<username>")
def panchayat_page(username):
    user_id = request.args.get('user_id')
    return render_template('roles/panchayat/panchayat_page.html', user_id=user_id, username=username)


# user stuff


# registrations

@ui.route("/registration/donor", methods=['GET', 'POST'])
def donor_registration_page():
    """
    Donor registration form. from the donor registration class in the forms.py file, the needed templates are taken and
    the donor_form variable contains that. The proper checks for the passwords and emails are done in the forms, need to
    push the values into the db
    :return: html template
    """
    donor_form = DonorRegistrationForm()

    if donor_form.validate_on_submit():
        username = donor_form.username.data
        password = donor_form.password.data
        email = donor_form.email.data
        phone = donor_form.phone_number.data
        pmi_member = donor_form.pmi_member.data
        pmi_number = request.form.get('pmi_id')
        address = donor_form.donor_address_1.data + " " + donor_form.donor_address_2.data + " " + donor_form.donor_address_3.data
        city = donor_form.city.data
        state = donor_form.state.data
        pincode = donor_form.pincode.data

        res = don_registration_response(username, email, phone, password, address, city, state, pincode, pmi_number)
        if res['response'] == 1:
            flash("User Registered Successfully\nUser ID - {}\nUsername - {}".format(res['User ID'], username),
                  "success")
            return redirect(url_for('ui.landing_page'))
        elif res['response'] == 2:
            flash("{}".format(res['message']), "success")
    return render_template('roles/registrations/donor_registration.html', form=donor_form)


@ui.route("/registration/user", methods=['GET', 'POST'])
def user_registration_page():
    user_form = UserRegistrationForm()
    if user_form.validate_on_submit():
        username = user_form.username.data
        panchayat = user_form.panchayat.data
        password = user_form.password.data
        email = user_form.email.data
        phone_number = user_form.phone_number.data
        id_proof = request.form.get('id_proof')
        location_proof = request.form.get('location_proof')
        address = user_form.user_address_1.data
        student = user_form.student.data

        user_registration_response(username, panchayat, email, phone_number, password, id_proof, location_proof, address, student)
    return render_template('roles/registrations/user_registration.html', form=user_form)


@ui.route("/registration/panchayat", methods=['GET', 'POST'])
def panchayat_registration_page():
    panchayat_form = PanchayatRegistrationForm()
    # TODO include
    # pan_response(name, panchayat_name, email, phone, address, password)
    return render_template('roles/registrations/panchayat_registration.html', form=panchayat_form)


@ui.route("/registration/volunteer", methods=['GET', 'POST'])
def volunteer_registration_page():
    volunteer_form = VolunteerRegistrationForm()
    if volunteer_form.validate_on_submit():
        username = volunteer_form.username.data
        password = volunteer_form.password.data
        email = volunteer_form.email.data
        phone_number = volunteer_form.phone_number.data
        pmi_member = volunteer_form.pmi_member.data
        pmi_number = volunteer_form.pmi_id.data
        address = volunteer_form.volunteer_address_1.data + " " + volunteer_form.volunteer_address_2.data + " " + volunteer_form.volunteer_address_3.data
        city = volunteer_form.city.data
        state = volunteer_form.state.data
        pincode = volunteer_form.pincode.data
        res = vol_registration_response(
            name=username,
            password=password,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            pmi_number=pmi_number,
            email=email,
            phone_number=phone_number,
        )
        if res['response'] == 1:
            flash("User Registered Successfully\nUser ID - {}\nUsername - {}".format(res['User ID'], username),
                  "success")
            return redirect(url_for('ui.landing_page'))
        elif res['response'] == 2:
            flash("{}".format(res['message']), "success")
    return render_template('roles/registrations/volunteer_registration.html', form=volunteer_form)


# auxiliary functions


@ui.route('/logout', methods=['POST'])
def logout_post():
    session.pop('logged_in', None)
    session.pop('role', None)
    print('logged out')
    return redirect(url_for('ui.landing_page'))

@ui.route('/error/<error_code>', defaults={'error_code': 0})
def error_page(error_code):
    if error_code == 0:
        return render_template('error_pages/default_error_page.html')

@ui.route('/test', methods=['GET', 'POST'])
def test_route():
    if request.method == 'POST':
        print('success')
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        address = request.form['address']
        return jsonify({'hello': 'world'})
    else:
        return render_template('test.html')
