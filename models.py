# all our models will go in this file
# http://docs.peewee-orm.com/en/latest/

# peewee in our flask app is like mongoose in our express app

from peewee import *
import datetime # built in to python
                # in python you often need to import things that would
                # already be there in other languages (think JS Date())
                # this keeps it lightweight

# import * means import everything
# in particular:
# SqliteDatabase - - adapter that lets us connect to sqlite databases
# and
# Model -- this Model() class is what we will will inherit from when
# defining our models (similar to what we did with mongoose in unit 2 and in our model files)


# we will use the flask_login module to set up our User model, sessions
# logins, authentication, requiring authentication for certain things
# https://flask-login.readthedocs.io/en/latest
from flask_login import UserMixin


# sqlite is a way to have a "database" that is just a stored in a file
# great for development bc you can have easily portable data (e.g. git)
# https://www.sqlite.org/index.html
# later when we deploy we will change this to postgres
# DATABASE = PostgresqlDatabase('dogs', user='postgres')


DATABASE = SqliteDatabase('dogs.sqlite')
# analogous to MONGO_DB_URL = mongod://localhost/dogs, {...} in unit 2
# there will be a file in our project called dogs.sqlite


# to behave correctly in flask-login's sessions/login/etc functionality,
# the User class must have certain methods and properties that
# a standard Peewee model (like Dog, e.g.) doesn't have
# our User class (model) will inherit from this UserMixin to provide
# those for use, see the docs below
# https://flask-login.readthedocs.io/en/latest/#your-user-class
# https://flask-login.readthedocs.io/en/latest/#flask_login.UserMixin
class User(UserMixin, Model):
    picture = CharField()
    name = CharField()
    address = CharField()
    cell_phone=CharField()
    email=CharField()

    class Meta:
        database = DATABASE



# define our Dog Model
# see here: http://docs.peewee-orm.com/en/latest/peewee/models.html
# Datetime
# https://docs.python.org/3/library/datetime.html


class Dog(Model):
    user_id = CharField()
    picture = CharField()
    name = CharField() # string
    breed = CharField()
    age = IntegerField()
    weight = CharField()
    additional_comments = CharField()
    # this is how you specify default values
    created_at: DateTimeField(default=datetime.datetime.now)

    # special constructor that gives our model/class instructions on
    # how to connect to a DB & where to store its data
    class Meta:
        database = DATABASE # use the db defined above as DATABASE



# run sqlite3 dogs.sqlite in your terminal to see that the user table was created when you start your app


# define a method that will get called when the app starts
# (in app.py) to set up our database connection
# similar to how we did require('./db/db.js') in server.js in unit 2
def initialize(): # NOTE we are making this name up
    DATABASE.connect() # analogous to mongoose.connect(....)

    # we need to explicity create the tables based on our schema
    # definitions above
    # use.create_tables()
    # first arg: is a LIST of tables to create
    # second arg: -- safe=True --- only create tables if they don't already exist
    DATABASE.create_tables([User, Dog], safe=True)
    print("Connected to the DB and created tables if they weren't already there")

    # with SQL, don't leave DB connection open, we don't want to hog space in the connection pool
    DATABASE.close()
