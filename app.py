import os
import requests

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect
from flask import url_for
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from random import shuffle
from random import choice
from datetime import datetime
from bs4 import BeautifulSoup



################################### CONFIG #####################################
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# Yelp OAuth
auth = Oauth1Authenticator(
    consumer_key=os.environ['CONSUMER_KEY'],
    consumer_secret=os.environ['CONSUMER_SECRET'],
    token=os.environ['TOKEN'],
    token_secret=os.environ['TOKEN_SECRET']
)

client = Client(auth)

################################## LIBRARY #####################################
def food_time(hours):
    '''
    Based on time of day of request, search term differs
    '''
    if hours < 12 and hours > 4:
        return 'brunch'
    elif hours >= 12 and hours <= 15:
        return 'lunch'
    elif hours >= 16 and hours <= 22:
        return 'dinner'
    else:
        return 'food'

def get_food_lat_lon(lat, lon, hours=0):
    '''
    Make yelp business search call based on lat, lon.
    '''
    # Make the search term different based on time of day
    params = {'term': food_time(hours)}
    response = client.search_by_coordinates(float(lat), float(lon), **params)
    restaurants = []
    for res in response.businesses:
        restaurants.append({'name': res.name, 'img': res.image_url,
            'url': res.url})
    shuffle(restaurants)
    return restaurants

def get_food(location, hours=datetime.now().hour):
    '''
    Make yelp business search call based on location.
    '''
    # Make the search term different based on time of day
    params = {'term': 'food'}
    response = client.search(location, **params)
    restaurants = []
    for res in response.businesses:
        restaurants.append({'name': res.name, 'img': res.image_url,
            'url': res.url})
    shuffle(restaurants)
    return restaurants

def get_food_porn():
    '''
    Grab background image using a scraper
    '''
    url = 'http://foodporndaily.com/'
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    return soup.find("img", {"id": "mainPhoto"})['src']

################################### ROUTES #####################################
@app.route('/')
def index():
    return render_template('index.html', background_img=get_food_porn())

@app.route('/eat', methods=['GET', 'POST'])
def eat():
    req = dict(request.form)
    args = dict(request.args)
    # POST Request from form
    if request.method == 'POST':
        if 'location' in req:
            loc = req['location']
            # Grab time
            hours = req['time'][0].split(':')[0][-2:]
            if len(loc) is 1 and loc[0] != u'':
                restaurants = get_food(loc[0], hours=int(hours))
                return render_template('eat.html', restaurants=restaurants)
            return redirect(url_for('index'))
        elif 'latitude' in req and 'longitude' in req:
            lat = req['latitude']
            lon = req['longitude']
            # Grab time
            hours = req['time'][0].split(':')[0][-2:]
            if len(lat) is 1 and len(lon) is 1 and lat[0] != u'':
                restaurants = get_food_lat_lon(lat[0], lon[0], hours=int(hours))
                return render_template('eat.html', restaurants=restaurants)
            return redirect(url_for('index'))
    # API GET Request
    else:
        if 'location' in args:
            loc = args['location']
            if len(loc) is 1:
                return jsonify(choice(get_food(loc[0])))
        elif 'latitude' in args and 'longitude' in args:
            lat = req['latitude']
            lon = req['longitude']
            if len(lat) is 1 and len(lon) is 1:
                return jsonify(choice(get_food_lat_lon(lat[0], lon[0])))
        else:
            return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
