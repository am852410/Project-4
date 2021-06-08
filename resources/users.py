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
def login_code(cell_phone):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)


    random_authcode = []
    for i in range(0,5): #[0,1,2,3,4]
        n = random.randint(0,9)
        random_authcode.append(str(n))

    random_authcode_string = "".join(random_authcode)
    message = client.messages \
                .create(
                     body=f"Hello! This is Tony Mendoza your fellow dog walker! Your authentication code is {random_authcode_string}",
                     from_='+16194863151',
                     to=f"+1{cell_phone}"
                 )
    return random_authcode_string

@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json() #getting the body from frontend fetch
    user = models.User.query.filter_by(cellPhone=payload['cellPhone']).first() #checking the database for the User model
    if user: #checking if the user was found.
        user_dict = model_to_dict(user)
        new_auth_code = login_code(payload['cellPhone'])
        user_dict["authCode"] = new_auth_code
        try:
            models.User.update(authCode=new_auth_code).where(models.User.cellPhone==payload['cellPhone']).execute()
            return jsonify(
                 data=user_dict,
                 message='Successfully texted user',
                 status=201
             ), 201
        except:
            return jsonify(
            message='User could not update',
            status=400
            ), 400
    else:
        return jsonify(
             message='Log in unsuccessful',
             status=400
         ), 400
