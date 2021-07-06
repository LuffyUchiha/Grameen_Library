from flask import Flask
from flask_cors import CORS
from donor_ui import donor_ui
from volunteer_ui import volunteer_ui
from user_ui import user_ui
from ui import ui

app = Flask(__name__)
app.secret_key = 'random string'
CORS(app=app)
app.config['CORS_HEADERS'] = 'Content-Type'
site_name = "http://localhost:5000"

app.register_blueprint(ui)
app.register_blueprint(donor_ui)
app.register_blueprint(volunteer_ui)
app.register_blueprint(user_ui)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)