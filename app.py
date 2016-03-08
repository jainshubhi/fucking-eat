import os

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect
from flask import url_for
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from random import shuffle


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

################################## LIBRARY #####################################
def get_food_lat_lon(lat, lon):
    params = {'term': 'food'}
    response = client.search_by_coordinates(float(lat), float(lon), **params)
    restaurants = []
    for res in response.businesses:
        restaurants.append({'name': res.name, 'img': res.image_url,
            'url': res.url})
    shuffle(restaurants)
    return restaurants

def get_food(location):
    params = {'term': 'food'}
    response = client.search(location, **params)
    restaurants = []
    for res in response.businesses:
        restaurants.append({'name': res.name, 'img': res.image_url,
            'url': res.url})
    shuffle(restaurants)
    return restaurants

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
            if len(loc) is 1 and loc[0] != u'':
                restaurants = get_food(loc[0])
                return render_template('eat.html', restaurants=restaurants)
            return redirect(url_for('index'))
        elif 'latitude' in req and 'longitude' in req:
            lat = req['latitude']
            lon = req['longitude']
            if len(lat) is 1 and len(lon) is 1 and lat[0] != u'':
                restaurants = get_food_lat_lon(lat[0], lon[0])
                return render_template('eat.html', restaurants=restaurants)
            return redirect(url_for('index'))
    # API GET Request
    else:
        if 'location' in args:
            loc = args['location']
            if len(loc) is 1:
                return jsonify({'restaurants': get_food(loc[0])})
        elif 'latitude' in args and 'longitude' in args:
            lat = req['latitude']
            lon = req['longitude']
            if len(lat) is 1 and len(lon) is 1:
                return jsonify({'restaurants': get_food_lat_lon(lat[0], lon[0])})
        else:
            return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
