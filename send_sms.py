# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "ACe56bbc27bf0114dab95868649000f796"
auth_token = "33410b886687829a4c9e3113e278ac01"
# print(os.environ)
# account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
# auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

random_authcode = "61945"

message = client.messages \
                .create(
                     body=f"Hello! This is Tony Mendoza your fellow dog walker! Your authentication code is {random_authcode}",
                     from_='+16194863151',
                     to='+16194838798'
                 )

print(message.sid)
