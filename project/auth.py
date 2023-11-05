from flask import Blueprint, render_template, redirect, url_for, request
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/signin')
def signin():
    return render_template('signIn.html')

@auth.route('/signin', methods=['POST'])
def login_post():
    # login code goes here
    print("signin")
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        print('Please check your login details and try again.')
        return redirect(url_for('auth.signin')) # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)

    return redirect(url_for('app.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    print("signUp")
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        print('Email address already exists')
        return redirect(url_for('auth.signup'))
    return redirect(url_for('auth.signin'))