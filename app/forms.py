from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

# handles fields of the login form
class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Sign In")

# handles fields of the register form
class RegisterForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    # might not need to make last name necessary (or even store it at all, will depend on how we use it)
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # make sure the password and confirmpassword fields are equal
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register Account")

    # confirm that the username is unique in the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("That username is already in use. Please use a different username.")

    # confirm that the email is unique in the database as well
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            # could possible add a 'reset password' functionality to help in this case
            raise ValidationError('There is already an account associated with that email.')