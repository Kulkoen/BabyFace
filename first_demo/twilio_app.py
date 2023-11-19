# Initialize Front-End Development with User

# Libraries
from redis_database import *
from twilio.rest import Client
import time
import json


def main():
    # Create Redis Database Instance
    r = create_redis_instance()

    # Create Client
    account_sid = 'AC4265725f01b7b72b4287f09303d86241'
    auth_token = 'a9e13e625bdd9f8d6b95ccd1621b8128'
    client = Client(account_sid, auth_token)

    # Flags 
    entry_flag = True

    while True:

        # Retrieve Message
        messages = client.messages.list()
        userMessage = messages[1].body

        # Send Message to Happy
        if userMessage and entry_flag:
            response = r.ping()
            print("Connection successful. Redis server responded:", response)
            r.hset("send-to-happy", '0', userMessage)
            entry_flag = False
            print(userMessage)

        # Send Happy's Message to User
        r.ping()
        happyMessage = r.hget('send-to-user', '0')
        if happyMessage:
            client.messages \
                .create(
                    body=happyMessage,
                    from_='+18557018877',
                    to='+14047477045'
                )
            break

        time.sleep(2)

if __name__ == "__main__":
    main()