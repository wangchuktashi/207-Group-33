from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename

event_bp = Blueprint('event', __name__, url_prefix='/create-event')

# @event_bp.route('/create-event', methods=['GET', 'POST'])
@event_bp.route('/<int:event_id>', endpoint='view_event')
def view_event(event_id):
    e = Event.query.get_or_404(event_id)

    return render_template('event.html', title=e.title, event=e)

@event_bp.route('/', methods=['GET', 'POST'], endpoint='create_event')
def create_event():
    print('Method type: ', request.method)
    form = EventForm()

    # if user clicked reset
    if form.reset.data:
        return redirect(url_for('event.create_event'))
    
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        event = Event(
            title = form.title.data,
            sport_type = form.sport_type.data,
            home_team = form.home_team.data,
            away_team = form.away_team.data,
            start_datetime = form.start_datetime.data,
            end_datetime = form.end_datetime.data,
            venue = form.venue.data,
            total_tickets = form.total_tickets.data,
            description = form.description.data,
            image = db_file_path
        )
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        print('Successfully created new event', 'success')
        # Always end with redirect when form is valid
        return redirect(url_for('event.create_event'))
    
    return render_template('create_event.html', form=form)

def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/img',secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = 'static/img' + secure_filename(filename)
  # save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

