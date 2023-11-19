from database import *
from google.cloud import aiplatform
from content import *
from customsendblue import sendMessage, sendContactCard
from readPayload import parse_payload, generate_prompt


def register_worker(payload):
    # get items out of our typeform
    print(payload)
    name, phone_number = parse_payload(payload)

    # create our user in dynamodb
    create_user(phone_number, name)

    # generate our prompt
    message = generate_prompt(name)

    # send them a message
    sendMessage(phone_number, message)
    # print("SendBlue:", message)

    # send them the contact card
    # print("SendBlue: sending contact card")
    sendContactCard(phone_number, message)


def worker(phoneId, message):
    try: 
        # validate our user
        # note: user_name is currently not set
        phoneId, user_name, timestamp = check_user(phoneId)

        # extract information from links
        content, percentage, link_type = handle_message(phoneId, message)

        # processing message
        sendMessage(phoneId, "Processing...")
        # print('SendBlue: Processing...')

        # update user request information
        create_link_item(phoneId, message)

        # gpt summary
        # summary = gp3(content, link_type)

        # output
        # output = format_message(summary, link_type, percentage)

        # send response
        # sendMessage(phoneId, output)
        # print("SendBlue:", phoneId, output)
    
    except Exception as e:
        # error message
        e_message = e.args[0]

        # print it out
        print(e_message)

        if(e_message == "User cooldown activated"):
            sendMessage(phoneId, "Please wait a moment before sending another article.")
            # print("SendBlue: Please wait a moment before sending another article.")
            return
        
        if(e_message == "User request limit reached"):
            sendMessage(phoneId, "If you would like to keep using Hal, please fill out this form: https://forms.gle/5cxS6NTsktYKGZhq8.")
            # print("SendBlue: If you would like to keep using Hal, please create an account at <link>")
            return
        
        if(e_message == "Twitter not supported"):
            sendMessage(phoneId, "I'm still learning to use Twitter.")
            # print("SendBlue: Twitter is not yet supported.")
            return

        # sendMessage(phoneId, error_message_handler(e_message))



r = redis.Redis(
    host='redis-11936.c1.us-east1-2.gce.cloud.redislabs.com',
    port=11936,
    password='MDBI6iRZeKrpTdRrhYqVaCJyY3l19FN4')

def main():
    # update_prompts("14045198006", "What should I do")
    # print(read_prompts("14045198006"))
    # sendMessage("14045198006","wassup")
    # print(check_user("14045198006"))
    worker("14045198006","help")

if __name__ == "__main__":
    main()
