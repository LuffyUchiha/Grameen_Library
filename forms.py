from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class LandingPageLoginForm(FlaskForm):
    username = StringField('User ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()


class DonorRegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password)])
    pmi_member = BooleanField('Are you a PMIPCC member?', validators=[DataRequired()])
    submit = SubmitField()

class UserRegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password)])
    pmi_member = BooleanField('Are you a PMIPCC member?', validators=[DataRequired()])
    submit = SubmitField()

class PanchayatRegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password)])
    pmi_member = BooleanField('Are you a PMIPCC member?', validators=[DataRequired()])
    submit = SubmitField()

