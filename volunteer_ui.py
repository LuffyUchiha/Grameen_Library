from flask import *

volunteer_ui = Blueprint('volunteer_ui', __name__)

@volunteer_ui.route("/volunteer/<username>")
def volunteer_page(username):
    user_id = request.args.get('user_id')
    if session.get('logged_in') and session.get('role') == 'volunteer':
        return render_template('roles/volunteer/volunteer_page.html', user_id=user_id, username=username)
    else:
        return redirect(url_for('ui.error_page'))