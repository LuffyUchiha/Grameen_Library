from flask import *

user_ui = Blueprint('user_ui', __name__)

@user_ui.route("/user/<username>")
def user_page(username):
    user_id = request.args.get('user_id')
    if session.get('logged_in') and session.get('role') == 'user':
        return render_template('roles/user/user_page.html', user_id=user_id, username=username)
    else:
        return redirect(url_for('ui.error_page'))