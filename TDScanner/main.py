# -*- coding: utf-8 -*-
# @Site    : www.TDScan.org

from flask import Flask, render_template
from trace import app as trace
from manager import app as manager

app = Flask(__name__)
app.register_blueprint(trace)
app.register_blueprint(manager)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run("0.0.0.0", port=5001,debug=True,threaded=True)