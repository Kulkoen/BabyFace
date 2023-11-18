# Task: Complete a Conversation given a Message from the Front User

# Libraries
from venv import create
from google.cloud import aiplatform

import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
from redis_database import *

# Paths 
CONTEXT_FILE = "context.txt"
INPUT_FILE = "input.txt"

# Defaults
context_str = ""
input_str = {}

def init_sample(
    project: None,
    location: None,
    experiment: None,
    staging_bucket: None,
    credentials: None,
    encryption_spec_key_name: None,
    service_account: None,
):

    from google.cloud import aiplatform

    aiplatform.init(
        project=project,
        location=location,
        experiment=experiment,
        staging_bucket=staging_bucket,
        credentials=credentials,
        encryption_spec_key_name=encryption_spec_key_name,
        service_account=service_account,
    )
    
def main():
    global input_str

    # Initialize Redis database 
    r = create_redis_instance()
    user_sub = r.pubsub()
    
    # Initialize Model
    vertexai.init(project="ai-atl-demo", location="us-central1")
    chat_model = ChatModel.from_pretrained("chat-bison")
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }

    # Initialize Inputs
    with open(CONTEXT_FILE) as f:
        context_str = f.read()
    # with open(CONTEXT_FILE) as f:
    #     input_str = f.read()
    
    # Conversation
    chat = chat_model.start_chat(
        context=context_str
    )

    try:
        # Try to ping the Redis server to check the connection
        response = r.ping()
        print("Connection successful. Redis server responded:", response)
        user_sub.subscribe("user-query")

        # Publish Message
        while True:
            # Listens to the message
            for message in user_sub.listen():
                if message['type'] == 'message':
                    input_str = message
                    break
            
            # Publish and print response
            if input_str:
                print(input_str['data'])

                response = chat.send_message(str(input_str['data']), **parameters)

                print(f"Response from Model: {response.text}")
                
                r.publish('chat-response', response.text)

    except redis.exceptions.ConnectionError as e:
        print("Error connecting to Redis:", e)
    
if __name__ == "__main__":
    main()