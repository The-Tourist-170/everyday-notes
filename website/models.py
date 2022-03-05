from website import db
#importing db from init file line 7.
from flask_login import UserMixin
#flask_login helps user to login and UserMixin provides the implementation of properties of flask_login like is_authenticated, is_active, is_anonymous etc
from sqlalchemy.sql import func


#db.model is the blueprint of db that means all the data must look like this.
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))

    #func will fetch the current datetime and set it default and everytime new note object is created it will store the default timezone into date.
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #references to who created this note
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    #setting id as primary key
    id = db.Column(db.Integer, primary_key=True)
    #unique means no 2 same email can exist.
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_Name = db.Column(db.String(150))
    last_Name = db.Column(db.String(150))

    #A relationship is established between two database tables when one table uses a foreign key that references the primary key of another table
    #notes will store all our notes
    notes = db.relationship('Note')