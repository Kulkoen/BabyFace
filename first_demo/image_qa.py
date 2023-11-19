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
    #source_image_path = "/Users/phuc/Desktop/HappyBaby/Images/happy_baby.jpeg"
    source_image = Image.load_from_file(location=source_image_path)
    
    
    # Questions List
    questions = [
        "Identify the primary emotion expressed by the baby in the image among these options: Angry, Disgust, Fear, Happy, Sad, Surprised, Neutral",
        "Is there anything considered unsafe for a baby in the environment? Yes or no",
        "Detail the most observable behavior or action of the baby in the image that correspond to expressions such as crying, smiling, laughing, sleeping, crawling, babbling, and other notable actions."
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
        context = """Imagine that you are a child caretaker that is observing a baby. 
                    Currently, this is the baby's current emotion: {}.
                    If the answer 'yes', the baby is in a potentially dangerous environment, if 'no', the baby is safe: {}.
                    Finally, this is the baby's current action: {}.
                    Write as if you are a young caretaker.
                    In a couple sentences, answer the parent's prompt in the appropiate tone for the situation.
                    Provide additional context if deemed helpful.
                    Make sure to include all provided context about the baby in your description.
                    """.format(response1, response2, response3)

        # Send Message
        r.hset("image-info", '0', context)

    except Exception as e:
        print(f"An error occurred while processing the image: {str(e)}")
