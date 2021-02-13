from flask import *
from flask_cors import CORS, cross_origin

from forms import LandingPageLoginForm, DonorRegistrationForm, UserRegistrationForm, PanchayatRegistrationForm

app = Flask(__name__)
app.secret_key = 'random string'
CORS(app=app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=['GET', 'POST'])
@app.route("/landing_page", methods=['GET', 'POST'])
def landing_page():
    login_form = LandingPageLoginForm()
    if login_form.validate_on_submit():
        print('username: {}\npassword: {}'.format(login_form.username.data, login_form.password.data))
        #TODO validate the with a query
        if login_form.username.data == "donor" and login_form.password.data == "pass":
            return render_template('roles/donor_page.html', user_id=login_form.username.data)
        else:
            flash(message='Incorrect credentials, please try again', category='danger')
    return render_template('landing_page.html', form=login_form)


@app.route("/about_grameen_library")
def about_page():
    return render_template('text_only/about_page.html')


@app.route("/about_donation")
def donation_info_page():
    return render_template('text_only/donation_info.html')


@app.route("/about_how_to_use")
def library_info_page():
    return render_template('text_only/library_info.html')


# -------------------------------------------------#


@app.route("/donor/<username>")
def donor_page(username):
    return render_template('roles/donor_page.html', user_id=username)

@app.route("/registration/donor")
def donor_registration_page():
    donor_form = DonorRegistrationForm()

    return render_template('roles/registrations/donor_registration.html', form=donor_form)

@app.route("/registration/user")
def user_registration_page():
    user_form = UserRegistrationForm()

    return render_template('roles/registrations/user_registration.html', form=user_form)

@app.route("/registration/panchayat")
def panchayat_registration_page():
    panchayat_form = PanchayatRegistrationForm()

    return render_template('roles/registrations/panchayat_registration.html', form=panchayat_form)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)

