from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

#Load the Blueprints from views.py
views = Blueprint('views', __name__)


#If the Add Note Function has been Called
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #New NOTE Received
    if request.method == 'POST':
        note = request.form.get('note')

        #If the Note is too short, send error
        if len(note) <= 1:
            flash('Note is too short', category='error')
        #If the Note is fine
        else:
            # Adding the Note + Current_User.id to the Database
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            #Send the back notification from the Flask function
            flash('Note added!', category='success')

    # Send the HTML page to the screen
    return render_template("home.html", user=current_user)



# If the Delete-Note Function has been Called
@views.route('/delete-note', methods=['POST'])
def delete_note():
    # Delete the note in the List
    #Loading Json.Requested.Data
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        #If the NOTE User ID is the same as the Current User, Delete the Note
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    # Using JS to refresh the page
    return jsonify({})





