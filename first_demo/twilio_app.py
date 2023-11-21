# Initialize Front-End Development with User

# Libraries
from redis_database import *
from twilio.rest import Client
import time
import json

from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

from conversationer import start_conversationer
from image_qa import start_imageqa

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def handle_sms():
    # Create Redis Database Instance
    r = create_redis_instance()

    # Create Client
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    # Flags 
    entry_flag = True

    while True:
        # Retrieve Message
        messages = client.messages.list()
        userMessage = messages[0].body

        # Send Message to Happy
        if userMessage and entry_flag:
            response = r.ping()
            r.hset("send-to-happy", '0', userMessage)
            start_imageqa()
            start_conversationer()
            entry_flag = False

        # Send Happy's Message to User
        r.ping()
        happyMessage = r.hget('send-to-user', '0')
        if happyMessage:
            client.messages \
                .create(
                    body=happyMessage,
                    from_='',
                    to=''
                )
            break

        time.sleep(2)
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)