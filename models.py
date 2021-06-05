# all our models will go in this file
# http://docs.peewee-orm.com/en/latest/

# peewee in our flask app is like mongoose in our express app
import os
from playhouse.db_url import connect
from peewee import *
import psycopg2
import datetime
from flask_login import UserMixin

DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///dogs.sqlite')

class User(UserMixin, Model):
    firstName = CharField()
    lastName = CharField()
    address = CharField()
    cellPhone=CharField()
    email=CharField()
    authCode=CharField(default="")

    class Meta:
        database = DATABASE


class Dog(Model):
    userId = CharField(default="")
    name = CharField() # string
    breed = CharField()
    age = IntegerField()
    weight = CharField()
    additionalComments = CharField()
    # this is how you specify default values
    # created_at: DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE # use the db defined above as DATABASE


def initialize(): # NOTE we are making this name up
    DATABASE.connect() # analogous to mongoose.connect(....)
    DATABASE.create_tables([User, Dog], safe=True)
    print("Connected to the DB and created tables if they weren't already there")
    DATABASE.close()
