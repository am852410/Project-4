import models
import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
# from flask_cors import CORS, cross_origin
from playhouse.shortcuts import model_to_dict
from twilio.rest import Client
import random

login = Blueprint('login', 'login')

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

@login.route('', methods=['POST'])
def login():
    payload = request.get_json() #getting the body from frontend fetch
    user_matches = models.User.select().where(models.User.cellPhone ** f"%{payload['cellPhone']}%") #checking the database for the User model
    user_matches_arr = [model_to_dict(user) for user in user_matches]
    user_dict = user_matches_arr[0]
    if user_dict: #checking if the user was found.
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
