#!flask/bin/python

from app import app,socketio
socketio.run(app, debug = True)

from app import app
from app import socketio
socketio.run(app, debug=True)
