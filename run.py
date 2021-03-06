from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = 'random string'
CORS(app=app)
app.config['CORS_HEADERS'] = 'Content-Type'
site_name = "http://localhost:5000"

from donor_ui import donor_ui
from volunteer_ui import volunteer_ui
from user_ui import user_ui
from panchayat_ui import panchayat_ui
from admin_ui import admin_ui
from ui import ui

app.register_blueprint(ui)
app.register_blueprint(donor_ui)
app.register_blueprint(volunteer_ui)
app.register_blueprint(user_ui)
app.register_blueprint(panchayat_ui)
app.register_blueprint(admin_ui)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)