from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Length


class LandingPageLoginForm(FlaskForm):
    username = StringField('User ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()


class DonorRegistrationForm(FlaskForm):
    username = StringField('Userame', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    phone_number = StringField('Phone No.', validators=[DataRequired()])
    pmi_member = BooleanField('Are you a PMIPCC member?')
    submit = SubmitField()


class UserRegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password)])
    pmi_member = BooleanField('Are you a PMIPCC member?', validators=[DataRequired()])
    submit = SubmitField()


class PanchayatRegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password)])
    pmi_member = BooleanField('Are you a PMIPCC member?', validators=[DataRequired()])
    submit = SubmitField()


class DonorDonateForm(FlaskForm):
    pass
