import os

from flask import Flask
from flask import render_template
from flask import request
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


################################### CONFIG #####################################
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

auth = Oauth1Authenticator(
    consumer_key=os.environ['CONSUMER_KEY'],
    consumer_secret=os.environ['CONSUMER_SECRET'],
    token=os.environ['TOKEN'],
    token_secret=os.environ['TOKEN_SECRET']
)

client = Client(auth)

URL = 'https://api.yelp.com/v2/search'
################################## LIBRARY #####################################
def get_food(lat, lon):
    pass


################################### ROUTES #####################################
@app.route('/')
def index():
    return render_template('index.html', SITE_ADDRESS=os.environ['SITE_ADDRESS'])

@app.route('/eat', methods=['GET', 'POST'])
def eat():
    req = dict(request.form)
    args = dict(request.args)
    # POST Request from form
    if request.method == 'POST':
        print
        if 'location' in req:
            loc = req['location']
            print loc
        elif 'latitude' in req and 'longitude' in req:
            print 'do i get here'
            lat = req['latitude']
            lon = req['longitude']
            print lat, lon
    # API GET Request
    else:
        if 'location' in args:
            loc = args['location']
            print loc
    return render_template('eat.html')


if __name__ == '__main__':
    get_food(u'34.1364537', u'-118.12331379999999')
    app.run()
