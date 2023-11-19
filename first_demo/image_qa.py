# Task: Use Vertex AI to Implement a Image Q&A Model

# Libraries
import os
from redis_database import *
from google.cloud import aiplatform
import vertexai
from vertexai.vision_models import ImageTextModel, Image

def start_imageqa():
    # Google Cloud Parameters
    PROJECT_ID = "ai-atl-demo"  # @param {type:"string"}
    LOCATION = "us-central1"  # @param {type:"string"}

    # Default Responses 
    response1 = ""
    response2 = ""
    response3 = ""

    # Initialize Model
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = ImageTextModel.from_pretrained("imagetext@001")

    # Load the image from the specified path within the "Images" folder
    images_path = "/Users/phuc/Desktop/HappyBaby/first_demo/images/"
    image_filename = 'captured_image_0.jpeg'
    source_image_path = os.path.join(images_path, image_filename)
    source_image = Image.load_from_file(location=source_image_path)
    
    # Questions List
    questions = [
        "Identify the primary emotion expressed by the baby in the image among these options: Angry, Disgust, Fear, Jappy, Sad, Surprise, Neutral.",
        "Is there anything considered unsafe for a baby in the environment? If yes, respond with 'Alert:' followed by the event.",
        "Detail the most observable behavior or actions of the baby in the image that correspond to expressions such as crying, smiling, laughing, sleeping, or any other notable actions."
    ]
    
    # Generate Answers
    for i, question in enumerate(questions):
        answers = model.ask_question(
            image=source_image,
            question = question,
            number_of_results=1,
        )
        answer = (str(answers).replace('[','').replace(']','').replace("'","").strip())
        
        if i == 0:
            response1 = "Your baby is feeling " + answer + "."
        if i == 1:
            if answer == "yes":
                response2 = "There is something potentially unsafe or dangerous near your baby."
            elif answer == "no":
                response2 = "Your baby's environment is safe."
            else:
                response2 = "No info available on the environment near your baby."
        if i == 2:
            response3 = "Your baby is currently " + answer + "."

    # Initialize Redis database 
    r = create_redis_instance()
    
    try:
        # Check Connection
        response = r.ping()
        print("Connection successful. Redis server responded:", response)

        # Publish Context for Conversationer
        context = """Imagine that you are a baby monitor. 
                    Currently, this is the baby's current emotion: {}.
                    This is the description of the baby's environment: {}.
                    Finally, this is the baby's action: {}.
                    Your user is a parent who is currently unable to assist the baby.
                    Write as if you are a friendly young caretaker.
                    Answer the parent's question in one sentence.
                    """.format(response1, response2, response3)

        # Send Message
        r.hset("image-info", '0', context)

    except Exception as e:
        print(f"An error occurred while processing the image: {str(e)}")
