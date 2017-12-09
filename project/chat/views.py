from flask import Flask, render_template, flash, redirect, request, session, url_for, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, socketio
from app.models import User
from functools import wraps


chat_blueprint = Blueprint(
    'chat', __name__,
    template_folder='templates'
)

@chat_blueprint.route('/competitors')
def competitors():
    #comp = Competition.query.filter_by(comp_id=comp_id).first()
    return render_template('competitors.html')

def messageReceived():
  print( 'Message was received!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'Received my event: ' + str( json ) )
  socketio.emit( 'my_response', json, callback = messageReceived )
