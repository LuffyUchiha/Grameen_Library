from flask import *
from get_values import vol_response, get_volunteer_details, get_collections
from datetime import datetime, date

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
    # data = [
    #     {
    #         'name': 'name1',
    #         'address': 'add',
    #         'date': datetime.strptime('2021-07-14', '%Y-%m-%d'),
    #         'no_of_books': '1',
    #         'contact': '123414324'
    #     },
    #     {
    #         'name': 'name2',
    #         'address': 'add',
    #         'date': datetime.strptime('2021-07-14', '%Y-%m-%d'),
    #         'no_of_books': '1',
    #         'contact': '123414324'
    #     },
    #     {
    #         'name': 'name3',
    #         'address': 'add',
    #         'date': datetime.strptime('2021-07-14', '%Y-%m-%d'),
    #         'no_of_books': '1',
    #         'contact': '123414324'
    #     },
    #     {
    #         'name': 'name3',
    #         'address': 'add',
    #         'date': datetime.strptime('2021-07-14', '%Y-%m-%d'),
    #         'no_of_books': '1',
    #         'contact': '123414324'
    #     },
    #     {
    #         'name': 'name3',
    #         'address': 'add',
    #         'date': datetime.strptime('2021-07-14', '%Y-%m-%d'),
    #         'no_of_books': '1',
    #         'contact': '123414324'
    #     },
    #     {
    #         'name': 'name3',
    #         'address': 'add',
    #         'start_date': datetime.strptime('2021-06-14', '%Y-%m-%d'),
    #         'end_date': datetime.strptime('2021-06-14', '%Y-%m-%d'),
    #         'no_of_books': '1',
    #         'contact': '123414324'
    #     },
    # ]
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
