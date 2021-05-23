# this app.py file is like server.js in the express unit
# CHECK OUT THE FLASK DOCUMENTATION: https://flask.palletsprojects.com/en/1.1.x/
from flask import Flask, jsonify # like: const express = require('express')
# now we're also importing jsonify from flask
# jsonify lets us send JSON HTTP responses (like res.json())

# from resources.dogs import dogs # import blueprint from resources.dogs
# think "const = dogController = require('./controllers/dogController.js')"
# from resources.users import users

# in python when you import a file, you get everything in the "global scope"
# of that file
# so this statement will import all variables and methods/functions from that
# file as properties on the models object (e.g. models.initialize() will be
# available in this file, etc)...note that we did not explicitly "export"
# anything in models.py
# google "namespacing in python" and "import in python"
import models

# import our package for handling cors
from flask_cors import CORS

# we need to import and configure the LoginManager
# https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager
# the LM is the main tool for coordinating session/login stuff in our app
from flask_login import LoginManager

import os

from dotenv import load_dotenv

load_dotenv() # takes the environment variables from .env

DEBUG=True # print nice helpful error msgs since we're in development
PORT=8000

# this is analogous to: const app = express()
app = Flask(__name__) # instantiating the Flask class to create an app



from twilio.rest import Client

import random


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def login_code(cell_phone):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)


    random_authcode = []
    for i in range(0,5):
        n = random.randint(0,9)
        random_authcode.append(str(n))

    random_authcode_string = "".join(random_authcode)
    message = client.messages \
                .create(
                     body=f"Hello! This is Tony Mendoza your fellow dog walker! Your authentication code is {random_authcode_string}",
                     from_='+16194863151',
                     to=f"+1{cell_phone}"
                 )



# configure the LoginManager. according the this:
# https://flask-login.readthedocs.io/en/latest/#configuring-your-application
# we need to do several things

# 1. set up a secret/key for sessions
# as demonstrated here: https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions
app.secret_key = os.environ.get('APP_SECRET')
print("Have a good night")

# 2. instantiate the LoginManager to actually get a login_manager
login_manager = LoginManager()

# 3. actually connect the app with the login_manager
login_manager.init_app(app)

# 4. load current_user from the user id store in the session
@login_manager.user_loader
def load_user(user_id):
    return models.User.get(models.User.id == user_id)





# CORS -- Cross Origin Resource Sharing
# a web domain (site/port/etc) is an "origin"
# this app is localhost:8000, that's an origin
# our react app is localhost:3000, that's a different origin
# Browsers implement CORS to prevent an JS app from sending requests
  # to origins other than the one the browser originally went to to get that JS
  # configuring CORS lets server say "here's who i'm expecting to hear from"

# first arg -- we are adding cors to blueprints, which blueprint to use
  # (you can CORS the whole app too)
# second arg -- which origins are allowed
# third arg -- lets us accept requests with cookies attached (so that we can
  # use sessions for auth)
CORS(dogs, origins=['http://localhost:3000'], supports_credentials=True)
 # also READ THIS: https://flask-cors.corydolphin.com/en/latest/api.html#using-cors-with-blueprints
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)

# use this blueprint (component/piece/section/controller of the app)
# to handle anything related to dogs
# analogous to app.use('/api/v1/dogs', dogController)
app.register_blueprint(dogs, url_prefix='/api/v1/dogs')
app.register_blueprint(users, url_prefix='/api/v1/users')


#GET /test
@app.route('/login', methods=["GET","POST"])
def login_page():

    error = ''
    attempted_random_authcode = request.form['random_authcode']
    try:
        user = models.User.get(models.User.cell_phone == payload['cell_phone'])
        if request.method == "POST":
           attempted_cellphone = request.form['cell_phone']
           return login_code(attempted_cellphone)


        else:
            error = "Invalid credentials. Try Again."

    # Log In route in Flask
    @app.route('/user')
    def user():
        if 'cell_phone' in session:
            return 'Logged in as %s' % escape(session['cell_phone'])
            return 'You are not logged in'






@app.route('/cat_json')
def get_cat_json():
    # you can pass key value pairs into jsonify()
    return jsonify(name="princess baby cat", age=9)

# you can use a dictionary as the value of a key-value pair in jsonify()
@app.route('/nested_json')
def get_nested_json():
    bebes = {
        'name': 'Princess baby cat',
        'age': 9,
        'cute': True,
        'sweet': True
    }
    return jsonify(name="Matt K", age=24, cat=bebes)

# can you pass an array of dicts?
@app.route('/two_cats')
def get_two_cats():
    bebes = {
        'name': 'Princess baby cat',
        'age': 9,
        'cute': True,
        'sweet': True
    }
    sir = {
        'name': 'Sir Charles III',
        'age': 5,
        'cute': True,
        'sweet': False
    }
    return jsonify(name="Matt K", age=24, cats=[bebes, sir])

# URL Parameters in Flask
# like (req.params in express: app.get('hello/:name'))
# name would be the parameter
@app.route('/say_hello/<username>')
def say_hello(username): #this function takes the URL parameter as an arg
    return "Hello {}".format(username)


# this is like app.listen() in express -- it goes at the bottom
# __name__ being '__main___' here means we just ran this file from the command line
# as opposed to exporting it and importing it somewhere else
if __name__ == '__main__':
    # when we start the app, set up out DB/tables as defined in models.property
    models.initialize() # remember in express we required the db before we did app.listen
    app.run(debug=DEBUG, port=PORT)
