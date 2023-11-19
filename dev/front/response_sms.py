from twilio.rest import Client
import time

account_sid = 'AC4265725f01b7b72b4287f09303d86241'
auth_token = '981bda211041a961a5d758425e943ae1'
# client = Client(account_sid, auth_token)

while True:
    client = Client(account_sid, auth_token)
    messages = client.messages.list()
    print(messages[1].body)
    time.sleep(5)