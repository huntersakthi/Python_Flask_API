from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

#Creating the Blueprint for auth route
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Getting the inputndata from HTML forms using POST method
        email = request.form.get('email')
        password = request.form.get('password')

        #Querying the data base whether the Email which is entered in the login page exists or not
        user = User.query.filter_by(email=email).first()

        #If email Exists
        if user:

            #Checking the password hash from DB and hasing and comparing the currently entered password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')

                #If Both the password hashes matches the flask login_user logs in the user
                login_user(user, remember=True)

                #Once login comleted the user gets redirected to the home page
                return redirect(url_for('views.home'))
            
            #Else Incorrect Password Message is Displayed
            else:
                flash('Incorrect password, try again.', category='error')

        #If EMail doesn't Exists the below message is displayed
        else:
            flash('Email does not exist.', category='error')

    #The HTML to be rendered by the /login route
    return render_template("login.html", user=current_user)


@auth.route('/logout')
#@login_required decorator to check whether the user is logged in before logout is displayed 
@login_required
def logout():

    #Flask Logout_user method to logout the user
    logout_user()

    #Once logout id done it redirects to login page
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():

    #Getting the inputndata from HTML forms for Sign Up page using POST method
    if request.method == 'POST':

        #Getting the EMail and Password data from the forms
        email = request.form.get('email')
        password = request.form.get('password_signup')

        #Querying the data base whether the Email which is entered in the Sign Up Page exists or not
        user = User.query.filter_by(email=email).first()

        #If email Exists
        if user:
            flash('Email already exists.', category='error')
        
        #If Email not Exists
        else:

            #A new user object with user email and password
            new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

            #Inserting the record to the database and commit it
            db.session.add(new_user)
            db.session.commit()

            #Once Sign Up is completed flask login_user method logs in the user
            login_user(new_user, remember=True)
            #Notification
            flash('Account created!', category='success')

            #Once Sign Up is completed flask redirects to the homepage of the application
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)
