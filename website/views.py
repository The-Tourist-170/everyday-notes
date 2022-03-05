from flask import Blueprint, render_template, request, flash, jsonify
#render_template is used to render the files under template folder  
# Blueprint indicates that this file is a blueprint i.e. it consist of bunch of urls, routes in it. 

from flask_login import login_required, current_user
from .models import Note
from website import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) # it is a decorator used to tell the directory or url
@login_required
#login_required will make the home function only run when the user is logged in
def home():   # home fn for homepage of site
    if request.method == 'POST': #checking if the note has been added
        note = request.form.get('Note') #fetching user's note in note

        #checking if note is not empty
        if len(note) < 1:
            flash('Note is too short!', category='error') 

        else:
            #adding the note
            new_note = Note(data=note, User_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added! ', category='success')

    return render_template("home.html", user=current_user)  # returning home.html html 

# blueprint created now we have to register it to __init__ file

#creating route and function to delete notes in js file line 4
@views.route('/delete-note', methods=['POST'])
def delete_note():
    #requestt.data will request the data and then store it in python dictionary.
    note = json.loads(request.data)
    #this will fetch note key from the dictionary and store it to noteId.
    noteId = note['noteId']
    #query.get will check if the noteId exists in db
    note = Note.query.get(noteId)
    if note:
        #if user own this note
        if note.User_id == current_user.id:
            #deleting note from db
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})