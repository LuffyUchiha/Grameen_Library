from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Optional




class LandingPageLoginForm(FlaskForm):
    username = StringField('User ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()


class DonorRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Regexp(regex=r'\d{8,13}')])
    donor_address_1 = StringField('Address', validators=[DataRequired()])
    donor_address_2 = StringField('Address', validators=[Optional()])
    donor_address_3 = StringField('Address', validators=[Optional()])
    pmi_member = BooleanField('Are you a pmi member?')
    submit = SubmitField()

class VolunteerRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    pmi_id = StringField('PMI ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    pmi_member = BooleanField('Are you a pmi member?')
    submit = SubmitField()

class UserRegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    panchayat = StringField('Panchayat', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Regexp(regex=r'\d{8,13}')])
    user_address_1 = StringField('Address', validators=[DataRequired()])
    user_address_2 = StringField('Address', validators=[Optional()])
    user_address_3 = StringField('Address', validators=[Optional()])
    id_proof = SelectField('ID Proof', choices=['Aadhar Card', 'Pan Card', 'Voter ID'])
    location_proof = SelectField('Address Proof', choices=['location-{}'.format(x) for x in range(1, 4)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    student = BooleanField('Are you a Student?')
    submit = SubmitField()


class PanchayatRegistrationForm(FlaskForm):
    panchayat_name = StringField('Panchayat Name', validators=[DataRequired()])
    poc_name = StringField('POC Name', validators=[DataRequired()])
    poc_email = StringField('POC Email', validators=[DataRequired(), Email()])
    poc_phone_number = StringField('POC Phone Number', validators=[DataRequired(), Regexp(regex=r'\d{8,13}')])
    poc_address_1 = StringField('Panchayat or POC Address', validators=[DataRequired('The address is required')] )
    poc_address_2 = StringField('Address', validators=[Optional()])
    poc_address_3 = StringField('Address', validators=[Optional()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()



class DonorDonateForm(FlaskForm):
    no_of_books = IntegerField('Number of books', validators=[DataRequired()])
    submit = SubmitField()


class DonationTemplate(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    ISBN = StringField('ISBN')
    author_name = StringField('Author Name')
    category = SelectField('Category', choices=['Category 1', 'Category 2', 'Category 3'])
    submit = SubmitField('Donate Books')


class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
