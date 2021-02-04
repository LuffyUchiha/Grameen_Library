from flask import *
from flask_cors import CORS, cross_origin

from forms import LandingPageLoginForm

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
    return render_template('landing_page.html', form=login_form)


@app.route("/about_grameen_library")
def about_page():
    return render_template('static/about_page.html')


@app.route("/about_donation")
def donation_info_page():
    return render_template('static/donation_info.html')


@app.route("/about_how_to_use")
def library_info_page():
    return render_template('static/library_info.html')


# -------------------------------------------------#


@app.route("/donor/<username>")
def donor_page(username):
    return render_template('roles/donor_page.html', user_id=username)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)

