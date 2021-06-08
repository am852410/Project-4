import models
import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
# from flask_cors import CORS, cross_origin
from playhouse.shortcuts import model_to_dict
from twilio.rest import Client
import random

users = Blueprint('users', 'users')

@users.route('', methods=['GET'])
def get_all_users():
    result = models.User.select()

    print("")
    print('result of user select query')
    print(result) #hmm looks like SQL

    user_dicts = [model_to_dict(user) for user in result]

    return jsonify({
        'data': user_dicts,
        'message': f"Successfully found {len(user_dicts)} users",
        'status': 200
    }), 200

    # @cross_origin()
@users.route('', methods=['POST'])
def create_user():
    # .get_json() attached to request will extract JSON from the request body
    payload = request.get_json() # this is like req.body in express
    print(payload) # you should see request body in your terminal :)

    new_user = models.User.create(firstName=payload['firstName'], lastName=payload['lastName'], address=payload['address'],
    cellPhone=payload['cellPhone'], email=payload['email'])
    print(new_user)
    user_dict = model_to_dict(new_user)

    return jsonify(
        data=user_dict,
        message='Successfully created user!',
        status=201
    ), 201

@users.route('', methods=['GET'])
def get_one_user():
    print("result of individual user query")


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
