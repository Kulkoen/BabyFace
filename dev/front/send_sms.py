# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC4265725f01b7b72b4287f09303d86241'
auth_token = '981bda211041a961a5d758425e943ae1'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='+18557018877',
         to='+14047477045'
     )

print(message.sid)
