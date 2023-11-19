# Task: Complete a Conversation given a Message from the Front User

# Libraries
from venv import create
from google.cloud import aiplatform

import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
from redis_database import *

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
    
def start_conversationer():
    global input_str

    # Initialize Redis database 
    r_get = create_redis_instance()

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
    context_str = r_get.hget('image-info', '0')
    input_str = r_get.hget('send-to-happy', '0')

    # Conversation
    chat = chat_model.start_chat(
        context=context_str
    )

    try:
        # Try to ping the Redis server to check the connection
        response = chat.send_message(str(input_str), **parameters)

        r_set = create_redis_instance()
        res = r_set.ping()
        print("Connection successful. Redis server responded:", res)
        r_set.hset('send-to-user', '0', response.text)


    except redis.exceptions.ConnectionError as e:
        print("Error connecting to Redis:", e)
