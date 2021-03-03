from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
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
    submit = SubmitField()


class UserRegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField()


class PanchayatRegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField()


class DonorDonateForm(FlaskForm):
    no_of_books = IntegerField('Number of books', validators=[DataRequired()])
    submit = SubmitField()


class DonationTemplate(FlaskForm):
    book_name = StringField('Book Name')
    ISBN = StringField('ISBN')
    author_name = StringField('Author Name')
    category = StringField('Category')
    submit = SubmitField('Donate')
    pass
