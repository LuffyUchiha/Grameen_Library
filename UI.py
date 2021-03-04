from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from flask import *
from flask_cors import CORS, cross_origin
import pandas as pd
from forms import *

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
        # TODO validate the with a query
        if login_form.password.data == "pass":
            return redirect(url_for('donor_page', username=username))
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
        pmi_member = donor_form.pmi_member.data

        print(username, password, email, phone, pmi_member)

        # TODO store the above details if valid. redirect to a different page is invalid
        return redirect(url_for('donor_page', username=username))

    return render_template('roles/registrations/donor_registration.html', form=donor_form)


@app.route("/donor/<username>/donate_books", methods=['GET', 'POST'])
def donor_donation_page(username):
    donation_form = DonationTemplate()
    if donation_form.validate_on_submit():
        book_name = donation_form.book_name.data
        ISBN = donation_form.ISBN.data
        author_name = donation_form.author_name.data
        category = donation_form.category.data

        # TODO push the values to the database
        return redirect(url_for('donor_donation_page', username=username))

    return render_template('roles/donor/donate_books.html', form=donation_form, username=username)


@app.route('/donation_visualization/')
def donation_visualization():
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)
    x = pd.DataFrame([1, 2, 3, 4])
    y1 = pd.DataFrame([2, 3, 4, 5])
    y2 = pd.DataFrame([5, 2, 4, 2])
    plt.plot(x, y1, color='blue')
    plt.plot(x, y2, color='red')
    plt.xlabel('Dates')
    plt.ylabel('Number of Books')
    plt.title('Distribution of books donated')
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


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

    return render_template('roles/registrations/user_registration.html', form=user_form)


@app.route("/registration/panchayat")
def panchayat_registration_page():
    panchayat_form = PanchayatRegistrationForm()

    return render_template('roles/registrations/panchayat_registration.html', form=panchayat_form)


@app.route('/test')
def test_route():
    return render_template('test.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
