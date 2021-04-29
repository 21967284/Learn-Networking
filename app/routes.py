## define the urls of each webpage ##

from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

# homepage (set to the root page)
@app.route('/')
def home():
    return render_template('home.html', title="A journey through the tcp/ip model")

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    #don't allow logged in users to access this page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    lForm = LoginForm()

    # if the login details are validated - NOTE WE WILL ALSO ADD JAVASCRIPT VALIDATION FOR RESPONSIVE FEEDBACK
    if lForm.validate_on_submit():
        # try setting user to the associated username's row - if that returns None then try email
        user = User.query.filter_by(username=lForm.username.data).first() or User.query.filter_by(email=lForm.username.data).first()
        # non-existant user or invalid password
        if user is None or not user.check_password(lForm.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=lForm.remember_me.data)
        # handle users clicking on pages that require login
        next_page = request.args.get('next')
        # if there is no specified next page, or the 'next' query points to a page outside this domain
        if not next_page or url_parse(next_page).netloc != '':
            # set the default location to the home page
            next_page = url_for('home')
        return redirect(next_page)

    return render_template('login.html', title="Login", lForm=lForm)

# logout button replaces login if the user is authenticated
@app.route('/logout')
def logout():
    logout_user()
    # if the link is clicked, log the user out then reroute them back to home
    return redirect(url_for('home'))

# register page - this function is very similar to the login function
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    rForm = RegisterForm()

    if rForm.validate_on_submit():
        user = User(first_name=rForm.firstname.data, last_name=rForm.lastname.data, username=rForm.username.data, email=rForm.email.data)
        user.set_password(rForm.password.data)
        # add the new user to the database and save the changes
        db.session.add(user)
        db.session.commit()
        # we can edit the style of flash messages to help the website interact with users
        flash('Congratulations {}, you are now a registered user!'.format(rForm.firstname.data))
        return redirect(url_for('login'))

    return render_template('register.html', title="Register", rForm=rForm)

# all empty pages (yet to be implemented so far)

# we may require user to be logged in to view their progress page
@app.route('/progress')
@login_required
def progress():
    return
@app.route('/application')
def application():
    return
@app.route('/transport')
def transport():
    return
@app.route('/network')
def network():
    return
@app.route('/link')
def link():
    return