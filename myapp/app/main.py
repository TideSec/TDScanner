#!/opt/python27/bin/python

from flask import Flask, render_template

from .upload import app as upload
from .history_record import app as history_record
from .breed_track import app as breed_track

app = Flask(__name__)
app.register_blueprint(upload)
app.register_blueprint(history_record)
app.register_blueprint(breed_track)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
