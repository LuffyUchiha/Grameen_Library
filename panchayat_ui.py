from flask import *

panchayat_ui = Blueprint('panchayat_ui', __name__)

@panchayat_ui.route("/panchayat/<username>")
def panchayat_page(username):
    print(session)
    user_id = request.args.get('user_id')
    if session.get('logged_in') and session.get('role') == 'panchayat':
        return render_template('roles/panchayat/panchayat_page.html', user_id=user_id, username=username)
    else:
        return redirect(url_for('ui.error_page'))