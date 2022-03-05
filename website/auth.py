from flask import Blueprint, render_template, flash, request, redirect, url_for
#importing redirect and url_for to redirect page after signing up to home
#flash is used to flash error or success or any messages
#the request object contains all the data that is sent from the client to the server. 
#render_template is used to render the files under template folder
# Blueprint indicates that this file is a blueprint i.e. it consist of bunch of urls, routes in it. 

from .models import User
#importing user from models file
#also hashing is a function that has no inverse means giving password will give you hash but no vie-versa.

from werkzeug.security import generate_password_hash, check_password_hash
#hash converts the password which is much more secure

#importing db
from website import db

#to hide home and login, logout when not logged in and when on home respectively.
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    #checking if the logged user's account exists.
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        #above code returns first filtered data by email.
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                #remember is used so that the user should not have to log in again and again.
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exists.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
#login_required will make the logout function only run when the user is logged in
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    #form- 	It is the dictionary object which contains the key-value pair of form parameters and their values.
    #get will fetch the details to it's variable assigned
    if request.method == 'POST':
        email = request.form.get('email')
        first_Name = request.form.get('firstName')
        last_Name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')

        #flashing error message
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_Name) < 2:
            flash('FirstName must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 8:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            # add user to the database
            #method means some hashing algorithm im this case sha256
            
            new_user = User(email=email, first_Name=first_Name, last_Name=last_Name, password=generate_password_hash(password1, method='sha256'))
            #The main reason technology leaders use SHA-256 is that it doesn't have any known vulnerabilities that make it insecure and it has not been “broken” unlike some other popular hashing algorithms.
            
            db.session.add(new_user)
            #adding new_user to db

            #comit is used to permanently save the changes in db
            db.session.commit()

            login_user(user, remember=True)
            flash('Account Created.', category='success')

            #redirecting to home
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)