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
        if username == 'test':
            if password == 'donor':
                return redirect(url_for('donor_page', user_id=0, username='tester'))
            elif password == 'panchayat':
                return redirect(url_for('panchayat_page', user_id=0, username='tester'))
            elif password == 'volunteer':
                return redirect(url_for('volunteer_page', user_id=0, username='tester'))
            elif password == 'user':
                return redirect(url_for('user_page', user_id=0, username='tester'))

        print('username: {}\npassword: {}'.format(username, password))
        res = login_response(username, password)
        if res['Response']:
            if res['Role'] == 'donor':  # Role = 2 => Donor
                return redirect(url_for('donor_page', user_id=res['ID'], username=res['Name']))
            elif res['Role'] == 'panchayat':  # Role = 3 => Panchayat
                return redirect(url_for('panchayat_page', user_id=res['ID'], username=res['Name']))
            elif res['Role'] == 'user':  # Role = 4 => User
                return redirect(url_for('user_page', user_id=res['ID'], username=res['Name']))
        else:
            flash(message='Incorrect credentials, please try again', category='danger')
    return render_template('landing_page.html', form=login_form)


# --------------------------------------------------#
# Back end related part of the code
# --------------------------------------------------#

# donor stuff

@app.route("/donor/<username>", methods=['GET', 'POST'])
def donor_page(username):
    """
    Donor page rerouting based on the username.
    :param username: String
    :return: html template
    """
    user_id = request.args.get('user_id')
    details = get_donor_details(user_id)
    donor_details = details['donor_details']
    donor_details_dict = {'username': donor_details[0], 'mobile_number': donor_details[1], 'email': donor_details[2],
                          'pmi_member': donor_details[3], 'address': donor_details[4]}
    return render_template('roles/donor/donor_page.html', username=username, user_id=user_id,
                           book_details=details['book_details'], donor_details=donor_details_dict)

@app.route('/donor/update_details', methods=['POST'])
def update_donor_details():
    user_id = request.form['user_id']
    username = request.form['username'] if request.form['username'] != "" else request.form['username_placeholder']
    email = request.form['email'] if request.form['email'] != "" else request.form['email_placeholder']
    mobile = request.form['mobile'] if request.form['mobile'] != "" else request.form['mobile_placeholder']
    address = request.form['address'] if request.form['address'] != "" else request.form['address_placeholder']
    resp = update_donor_details_backend(
        user_id=user_id,
        username=username,
        email=email,
        mobile=mobile,
        address=address
    )
    return json.dumps({'username': username, 'email': email, 'mobile': mobile, 'address': address})

@app.route("/donor/<username>/donate_books", methods=['GET', 'POST'])
def donor_donation_page(username):
    user_id = request.args.get('user_id')
    donation_form = DonationTemplate()
    donation_form.category.choices = get_categories()
    if donation_form.validate_on_submit():
        book_name = donation_form.book_name.data
        ISBN = donation_form.ISBN.data
        author_name = donation_form.author_name.data
        category = request.form.get('category')
        req = {
            "username": username,
            "book_name": book_name,
            "ISBN": ISBN,
            "author_name": author_name,
            "category": category
        }

        resp = requests.post(url="http://localhost:5000/donor/donor_donation"
                                 "?username={}&book_name={}&ISBN={}&author_name={}&category={}"
                             .format(username, book_name, ISBN, author_name, category))
        if str(resp.content).split("'")[1] == "Success":
            flash("Book Donated Successfully", "success")
            donation_form.book_name.data = ""
            donation_form.ISBN.data = ""
            donation_form.author_name.data = ""
            donation_form.category.data = ""
        elif str(resp.content).split("'")[1] == "Failure":
            flash("Donation Failed. Please contact the Volunteer", "danger")

    return render_template('roles/donor/donate_books.html', form=donation_form, username=username, user_id=user_id)


@app.route("/donor/donor_donation", methods=['POST'])
def donor_donation_post_page():
    req = request.args
    username = req.get("username")
    book_name = req.get("book_name")
    author_name = req.get("author_name")
    ISBN = req.get("ISBN")
    category = req.get("category")
    if donate_book(username, book_name, author_name, ISBN, category) == -1:
        return "Failure"
    else:
        print("success")
        return "Success"


@app.route('/donor/<username>/donor_stats')
def donor_stats(username):
    user_id = request.args.get('user_id')
    book_details = request.args.to_dict(flat=False)['book_details']
    bd = []
    for x in book_details:
        bd.append(eval(x))
    return render_template('roles/donor/book_usage_statistics.html', book_details=bd)

@app.route('/donation_visualization/')
def donation_visualization():
    """
    A function which uses matplotlib to plot the donor donation graph
    :return: Image(File)
    """
    month_name = {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec',
    }
    book_details = request.args.to_dict(flat=False)['book_details']
    t = {'Book ID': [], 'Book Name': [], 'Donate Date': [], 'isIdentified': []}
    for x in book_details:
        x = eval(x)
        t['Book ID'].append(x['Book ID'])
        t['Book Name'].append(x['Book Name'])
        t['Donate Date'].append(x['Donate Date'])
        t['isIdentified'].append(x['isIdentified'])
    book_details = pd.DataFrame(t)
    book_details = book_details[['Donate Date', 'Book ID']]
    book_details['Donate Date'] = pd.to_datetime(book_details['Donate Date'])
    start_time = datetime.datetime.now().replace(datetime.date.today().year - 1)
    book_details = book_details[book_details['Donate Date'] > start_time]
    book_details = book_details.sort_values(by='Donate Date')
    book_details['Donate Date'] = book_details['Donate Date'].apply(lambda x: "{}/{}\n({})".format(x.month, x.year, month_name[x.month]))
    book_details = book_details.groupby('Donate Date').agg(func=np.size)
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)
    x = list(book_details.index)
    y = list(book_details['Book ID'])
    if x.__len__() < 8:
        oldest_month = x[0].split('\n')[0]
        month, year = list(map(int, oldest_month.split('/')))
        months = []
        for _ in range(8-x.__len__()):
            month -= 1
            if month == 0:
                month = 12
                year -= 1
            print(month, year)
            months.append("{}/{}\n({})".format(month, year, month_name[month]))
        plt.bar(months[::-1], [0]*months.__len__())
    plt.bar(x, y, color='blue')
    plt.ylabel('Number of Books')
    plt.title('Distribution of books donated')
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

# volunteer stuff

@app.route("/volunteer/<username>")
def volunteer_page(username):
    user_id = request.args.get('user_id')
    return render_template('roles/volunteer/volunteer_page.html', user_id=user_id, username=username)


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


# panchayat stuff

@app.route("/panchayat/<username>")
def panchayat_page(username):
    user_id = request.args.get('user_id')
    return render_template('roles/panchayat/panchayat_page.html', user_id=user_id, username=username)


# user stuff

@app.route("/user/<username>")
def user_page(username):
    user_id = request.args.get('user_id')
    return render_template('roles/user/user_page.html', user_id=user_id, username=username)


# registrations

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
        address = donor_form.donor_address_1.data + " " + donor_form.donor_address_2.data + " " + donor_form.donor_address_3.data

        res = don_registration_response(username, email, phone, password, address)
        if res['response'] == 1:
            flash("User Registered Successfully\nUser ID - {}\nUsername - {}".format(res['User ID'], username),
                  "success")
            return redirect(url_for('landing_page'))
        else:
            # TODO  redirect Error Page
            pass
    return render_template('roles/registrations/donor_registration.html', form=donor_form)


@app.route("/registration/user", methods=['GET', 'POST'])
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
    # TODO include
    # user_response(name, panchayat, email, phone, password)
    return render_template('roles/registrations/user_registration.html', form=user_form)


@app.route("/registration/panchayat", methods=['GET', 'POST'])
def panchayat_registration_page():
    panchayat_form = PanchayatRegistrationForm()
    # TODO include
    # pan_response(name, panchayat_name, email, phone, address, password)
    return render_template('roles/registrations/panchayat_registration.html', form=panchayat_form)


@app.route("/registration/volunteer", methods=['GET', 'POST'])
def volunteer_registration_page():
    volunteer_form = VolunteerRegistrationForm()
    return render_template('roles/registrations/volunteer_registration.html', form=volunteer_form)


# auxiliary functions



@app.route('/test',methods=['GET', 'POST'])
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


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
