# this app.py file is like server.js in the express unit
# CHECK OUT THE FLASK DOCUMENTATION: https://flask.palletsprojects.com/en/1.1.x/
from flask import Flask, jsonify, after_this_request # like: const express = require('express')
import models
# import our package for handling cors
from flask_cors import CORS
# we need to import and configure the LoginManager
# https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager
# the LM is the main tool for coordinating session/login stuff in our app
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from resources.dogs import dogs
from resources.users import users

load_dotenv() # takes the environment variables from .env

DEBUG=True # print nice helpful error msgs since we're in development
PORT=8000

# this is analogous to: const app = express()
app = Flask(__name__) # instantiating the Flask class to create an app

CORS(dogs, origins=['https://peacemakerdogwalkingcompany.herokuapp.com'], supports_credentials=True)
CORS(users, origins=['https://peacemakerdogwalkingcompany.herokuapp.com'], supports_credentials=True)
CORS(app, origins=['*'])


app.register_blueprint(dogs, url_prefix='/dogs')# analogous to app.use('/dogs', dogController)
app.register_blueprint(users, url_prefix='/users')# analogous to app.use('/users', userController)

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                      # (in our case this will be some JSON)


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
    user = models.User.get(models.User.id == user_id)
    user['auth_code'] = new_auth_code
    models.DATABASE.commit()


# this is like app.listen() in express -- it goes at the bottom
# __name__ being '__main___' here means we just ran this file from the command line
# as opposed to exporting it and importing it somewhere else
# if __name__ == '__main__':
#     # when we start the app, set up out DB/tables as defined in models.property
#     models.initialize() # remember in express we required the db before we did app.listen
#     app.run(debug=DEBUG, port=PORT)

if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()
