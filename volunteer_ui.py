from flask import *
from get_values import vol_response, get_volunteer_details, get_collections, enter_book
from datetime import datetime, date
from forms import *

volunteer_ui = Blueprint('volunteer_ui', __name__)

@volunteer_ui.route("/volunteer/<username>")
def volunteer_page(username):
    user_id = request.args.get('user_id')
    if session.get('logged_in') and session.get('role') == 'volunteer':
        details = get_volunteer_details(user_id)
        return render_template('roles/volunteer/volunteer_page.html', vol_details = details)
    else:
        return redirect(url_for('ui.error_page'))


@volunteer_ui.route("/volunteer/get_donors", methods=['POST'])
def get_donor_post():
    # number_of_donors = int(request.form['number_of_donors'])
    user_id = request.form['volunteer_id']
    from_date = request.form['from_date'].split('-')
    from_date = date(year=int(from_date[0]), month=int(from_date[1]), day=int(from_date[2]))
    to_date = request.form['to_date'].split('-')
    to_date = date(year=int(to_date[0]), month=int(to_date[1]), day=int(to_date[2]))

    # print(user_id, from_date, to_date)
    data = get_collections(user_id)
    ret_data = []
    for x in data:
        if from_date < x['start_date'] < to_date or from_date < x['end_date'] < to_date:
            x['start_date'] = str(x['start_date'])
            x['end_date'] = str(x['end_date'])
            ret_data.append(x)
    # print(data,'\n', ret_data)
    return json.dumps({
        'data': ret_data,
    })


@volunteer_ui.route('/volunteer/confirm_donation', methods=['GET', 'POST'])
def confirm_donation():
    volunteer_id = request.args.get('volunteer_id')
    if session['logged_in'] and session['role']=='volunteer':
        if request.method=='GET':
            return render_template('roles/volunteer/confirm_donation.html')
        elif request.method=='POST':
            donor_id = request.form.get('donor_id')
            book_name = request.form.get('book_name')
            isbn = request.form.get('isbn')
            enter_book(donor_id, book_name, isbn, volunteer_id)
            return "Success"
    else:
        return redirect(url_for('ui.error_page'))