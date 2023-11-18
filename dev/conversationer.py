# Task: Complete a Conversation given a Message from the Front User

# Libraries
from google.cloud import aiplatform
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair

# Paths 
CONTEXT_FILE = "context.txt"
INPUT_FILE = "input.txt"

# Defaults
context_str = ""
input_str = ""

def init_sample(
    project: 'ai-atl-demo',
    location: 'us-central1',
    experiment: 'first-experiment',
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
    with open(CONTEXT_FILE) as f:
        input_str = f.read()
    
    # Conversation
    chat = chat_model.start_chat(
        context=context_str
    )
    response = chat.send_message(input_str, **parameters)
    print(f"Response from Model: {response.text}")

if __name__ == "__main__":
    main()