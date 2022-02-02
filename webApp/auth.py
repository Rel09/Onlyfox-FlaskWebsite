from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

# Loading the Auth Blueprint
auth = Blueprint('auth', __name__)

#User Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # LOGIN Has been clicked
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Search the User in the Database
        user = User.query.filter_by(email=email).first()

        #Check if the Password is good
        if user:
            #If the Encrypted Password is the password Received
            if check_password_hash(user.password, password):
                #You are now Logged in
                flash('Logged in succesfully', category='success')
                login_user(user, remember=True)
                #Redirect to the Home page with Views Backend
                return redirect(url_for('views.home'))
            #Wrong Password
            else:
                flash('Incorrect password, try again', category='error')
        #Wrong Email
        else:
            flash('Email does not exist', category='error')
    #Reload the Login Page
    return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    #New account is being made
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #Check if the email already exist in the Database
        user = User.query.filter_by(email=email).first()

        # Very basic Check-up
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater then 4 characters', category='error')
        elif len(first_name) < 2:
            flash('Username must be greater then 1 character', category='error')
        elif password1 != password2:
            flash('Password do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            #Preparing the New User for the Database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            #Log the user and Remember his session
            login_user(user, remember=True)
            flash('Account Created!', category='success')
            #Return the Logged Home page
            return redirect(url_for('views.home'))
    # If Login fail, send back to Sign up Page
    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    #Logout the user, Thanks FLask
    logout_user()
    # Return to the Login page
    return redirect(url_for('auth.login'))


