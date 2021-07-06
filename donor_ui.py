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

donor_ui = Blueprint('donor_ui', __name__)

plt.style.use('ggplot')


@donor_ui.route("/donor/<username>", methods=['GET', 'POST'])
def donor_page(username):
    """
    Donor page rerouting based on the username.
    :param username: String
    :return: html template
    """
    if session.get('logged_in') and session.get('role') == 'donor':
        user_id = request.args.get('user_id')
        details = get_donor_details(user_id)
        donor_details = details['donor_details']
        donor_details_dict = {'username': donor_details[0], 'mobile_number': donor_details[1], 'email': donor_details[2],
                              'pmi_member': donor_details[3], 'address': donor_details[4], 'city': donor_details[5],
                              'state': donor_details[6], 'pincode': donor_details[7]}
        return render_template('roles/donor/donor_page.html', username=username, user_id=user_id,
                               book_details=details['book_details'], donor_details=donor_details_dict)
    else:
        return redirect(url_for('ui.error_page'))


@donor_ui.route('/donor/update_details', methods=['POST'])
def update_donor_details():
    print('inside')
    user_id = request.form['user_id']
    username = request.form['username'] if request.form['username'] != "" else request.form['username_placeholder']
    email = request.form['email'] if request.form['email'] != "" else request.form['email_placeholder']
    mobile = request.form['mobile'] if request.form['mobile'] != "" else request.form['mobile_placeholder']
    address = request.form['address'] if request.form['address'] != "" else request.form['address_placeholder']
    city = request.form['city'] if request.form['city'] != "" else request.form['city_placeholder']
    state = request.form['state'] if request.form['state'] != "" else request.form['state_placeholder']
    pincode = request.form['pincode'] if request.form['pincode'] != "" else request.form['pincode_placeholder']
    resp = update_donor_details_backend(
        user_id=user_id,
        username=username,
        email=email,
        mobile=mobile,
        address=address,
        city=city,
        state=state,
        pincode=pincode
    )
    print(resp)
    return json.dumps({'username': username, 'email': email, 'mobile': mobile, 'address': address, 'city': city, 'state': state, 'pincode': pincode})


@donor_ui.route("/donor/<username>/donate_books", methods=['GET', 'POST'])
def donor_donation_page(username):
    user_id = request.args.get('user_id')
    donation_form = DonationTemplate()
    donation_form.category.choices = get_book_categories()
    if donation_form.validate_on_submit():
        book_name = donation_form.book_name.data
        no_of_copies = donation_form.no_of_books.data
        ISBN = donation_form.ISBN.data
        author_name = donation_form.author_name.data
        category = request.form.get('category')
        req = {
            "user_id": user_id,
            "username": username,
            "no_of_copies": no_of_copies if no_of_copies != "" else '0',
            "book_name": book_name,
            "ISBN": ISBN,
            "author_name": author_name,
            "category": category
        }
        # resp = requests.post(url="http://localhost:5000/donor/donor_donation"
        #                          "?user_id={}&book_name={}&no_of_copies={}&ISBN={}&author_name={}&category={}"
        #                      .format(req['user_id'], req['book_name'], req['no_of_copies'], req['ISBN'],
        #                              req['author_name'], req['category']))
        resp = requests.post(url=site_name + url_for('donor_donation_post_page', user_id=req['user_id'], book_name=req['book_name'], no_of_copies=req['no_of_copies'], ISBN=req['ISBN'],
                                     author_name=req['author_name'], category=req['category']))
        if str(resp.content).split("'")[1] == "Success":
            flash("Book Donated Successfully", "success")
            donation_form.book_name.data = ""
            donation_form.no_of_books.data = ""
            donation_form.ISBN.data = ""
            donation_form.author_name.data = ""
            donation_form.category.data = ""
        elif str(resp.content).split("'")[1] == "Failure":
            flash("Donation Failed. Please contact the Volunteer", "danger")

    return render_template('roles/donor/donate_books.html', form=donation_form, username=username, user_id=user_id)


@donor_ui.route("/donor/donor_donation", methods=['POST'])
def donor_donation_post_page():
    req = request.args
    user_id = req.get("user_id")
    book_name = req.get("book_name")
    no_of_copies = req.get("no_of_copies")
    no_of_copies = no_of_copies if no_of_copies.isnumeric() else None
    author_name = req.get("author_name")
    ISBN = req.get("ISBN")
    category = req.get("category")
    if donate_book(user_id, book_name, no_of_copies, author_name, ISBN, category) == -1:
        return "Failure"
    else:
        return "Success"


@donor_ui.route('/donor/<username>/donor_stats')
def donor_stats(username):
    user_id = request.args.get('user_id')
    if request.args.get('book_details') == None:
        return render_template('roles/donor/book_usage_statistics.html', book_details=[])
    book_details = request.args.to_dict(flat=False)['book_details']
    bd = []
    for x in book_details:
        bd.append(eval(x))
    return render_template('roles/donor/book_usage_statistics.html', book_details=bd)


@donor_ui.route('/donation_visualization/')
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
    if request.args.get('book_details') == None:
        print('none')
        fig, ax = plt.subplots()
        canvas = FigureCanvas(fig)
        ax.axes.xaxis.set_visible(False)
        plt.ylabel('Number of Books')
        img = BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img, mimetype='image/png')
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
    book_details['Donate Date'] = book_details['Donate Date'].apply(
        lambda x: "{}/{}\n({})".format(x.month, x.year, month_name[x.month]))
    book_details = book_details.groupby('Donate Date').agg(func=np.size)
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)
    x = list(book_details.index)
    y = list(book_details['Book ID'])
    if x.__len__() < 8:
        oldest_month = x[0].split('\n')[0]
        month, year = list(map(int, oldest_month.split('/')))
        months = []
        for _ in range(8 - x.__len__()):
            month -= 1
            if month == 0:
                month = 12
                year -= 1
            print(month, year)
            months.append("{}/{}\n({})".format(month, year, month_name[month]))
        plt.bar(months[::-1], [0] * months.__len__())
    plt.bar(x, y, color='blue')
    plt.ylabel('Number of Books')
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')
