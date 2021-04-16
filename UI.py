from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from flask import *
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
from forms import *
from get_values import *

plt.style.use('ggplot')

app = Flask(__name__)
app.secret_key = 'random string'
CORS(app=app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Adresses to the static pages

@app.route("/about_grameen_library")
def about_page():
    return render_template('text_only/about_page.html')


@app.route("/about_donation")
def donation_info_page():
    return render_template('text_only/donation_info.html')


@app.route("/about_how_to_use")
def library_info_page():
    return render_template('text_only/library_info.html')


@app.route("/", methods=['GET', 'POST'])
@app.route("/landing_page", methods=['GET', 'POST'])
def landing_page():
    login_form = LandingPageLoginForm()
    if login_form.validate_on_submit():

        username = login_form.username.data
        password = login_form.password.data

        print('username: {}\npassword: {}'.format(username, password))
        res= login_response(username, password)
        if res['Response']:
            return redirect(url_for('donor_page', username=res['ID']))
        else:
            flash(message='Incorrect credentials, please try again', category='danger')
    return render_template('landing_page.html', form=login_form)


# --------------------------------------------------#
# Back end related part of the code
# --------------------------------------------------#

# donor stuff

@app.route("/donor/<username>")
def donor_page(username):
    """
    Donor page rerouting based on the username.
    :param username: String
    :return: html template
    """
    return render_template('roles/donor/donor_page.html', username=username)


@app.route("/registration/donor", methods=['GET', 'POST'])
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

        print(username, password, email, phone)
        res=don_response(username, email, phone, password)
        if res['response'] == 1:
            return redirect(url_for('donor_page', username=res['User ID']))
        else:
            # TODO  redirect Error Page
            pass

    return render_template('roles/registrations/donor_registration.html', form=donor_form)


@app.route("/donor/<username>/donate_books", methods=['GET', 'POST'])
def donor_donation_page(username):
    donation_form = DonationTemplate()
    if donation_form.validate_on_submit():
        book_name = donation_form.book_name.data
        ISBN = donation_form.ISBN.data
        author_name = donation_form.author_name.data
        category = donation_form.category.data
        if donate_book(username, book_name, author_name, ISBN, category) == -1:
            pass
        else:
            return redirect(url_for('donor_donation_page', username=username))

    return render_template('roles/donor/donate_books.html', form=donation_form, username=username)


@app.route('/donation_visualization/')
def donation_visualization():
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)
    x = np.arange(5)
    y1 = np.random.randint(1, 10)
    y2 = np.random.randint(1, 10)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.xlabel('Dates')
    plt.ylabel('Number of Books')
    plt.title('Distribution of books donated')
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route('/donor/<username>/donor_stats')
def donor_stats(username):
    #TODO get me the books donated by "username"(which is currently donor_id, will change later) as a json
    return render_template('roles/donor/book_usage_statistics.html')

# admin stuff

@app.route("/admin", methods=['GET', 'POST'])
def admin_login_page():
    admin_form = AdminLoginForm()
    if admin_form.validate_on_submit():
        username = admin_form.username.data
        password = admin_form.password.data
        if password == 'pass':
            return redirect(url_for('admin_page', username=username))

    return render_template('roles/admin/admin_login_page.html', form=admin_form)


@app.route("/admin/<username>")
def admin_page(username):
    return render_template('roles/admin/admin_page.html', username=username)


@app.route("/registration/user")
def user_registration_page():
    user_form = UserRegistrationForm()
    #TODO include
    #user_response(name, panchayat, email, phone, password)
    return render_template('roles/registrations/user_registration.html', form=user_form)


@app.route("/registration/panchayat")
def panchayat_registration_page():
    panchayat_form = PanchayatRegistrationForm()
    # TODO include
    #pan_response(name, panchayat_name, email, phone, address, password)
    return render_template('roles/registrations/panchayat_registration.html', form=panchayat_form)


@app.route('/test')
def test_route():
    return render_template('test.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
