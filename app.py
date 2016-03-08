import os
import requests

from flask import Flask
from flask import render_template
from flask import request


################################### CONFIG #####################################
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


################################### ROUTES #####################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eat', methods=['GET', 'POST'])
def eat():
    req = dict(request.form)
    args = dict(request.args)
    # POST Request from form
    if request.method == 'POST':
        if 'location' in req:
            loc = req['location']
    # API GET Request
    else:
        if 'location' in args:
            loc = args['location']
    return 'hi'


if __name__ == '__main__':
    app.run()
