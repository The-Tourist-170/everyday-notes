#init file is for making the website folder a package to use that in main

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from flask_login import LoginManager
#LoginManager will manage all the login stuff


#initializing db
db = SQLAlchemy()

#this db will be stored in website folder.

#setting name of db
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)  #initializing flask
    app.config['SECRET_KEY'] = 'kan3ki' #To secure the cookies and sessions. (Kind of encryption)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #above statement tells flask we are using database and and where it is loacted.
    db.init_app(app)

    from .views import views  # importing blueprint of views file
    from .auth import auth    # importing blueprint of auth file

    app.register_blueprint(views, url_prefix='/') #registering the blueprint of views file
    app.register_blueprint(auth, url_prefix='/')  #registering the blueprint of auth file
    # url prefix is used to access the route of file
    #telling db that we are using it in this app.

    #importing User and Note from models file.
    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    #if not logged in redirect to auth.login 
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#this will create database if it does not exists.
def create_database(app):
    #path will check if the path of db exists
    if not path.exists('website/' + DB_NAME):
        #this will create a db
        db.create_all(app=app)

#Successfully created the app and initialized the key