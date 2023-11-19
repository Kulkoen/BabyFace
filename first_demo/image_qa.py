import os
from redis_database import *
from google.cloud import aiplatform
import vertexai
from vertexai.vision_models import ImageTextModel, Image

def main():
    PROJECT_ID = "ai-atl-demo"  # @param {type:"string"}
    LOCATION = "us-central1"  # @param {type:"string"}
    
    response1 = ""
    response2 = ""
    response3 = ""

    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = ImageTextModel.from_pretrained("imagetext@001")

    # Assuming the "Images" folder is within the GitHub repository directory
    #current_directory = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of your Python script
    images_path = "/Users/phuc/Desktop/HappyBaby/first_demo/images/"

    # Load the image from the specified path within the "Images" folder
    image_filename = 'baby_by_chemicals.jpeg'
    source_image_path = os.path.join(images_path, image_filename)
    source_image = Image.load_from_file(location=source_image_path)
    
    #questions list
    questions = [
        "Identify the primary emotion expressed by the baby in the image among these options: Angry, Disgust, Fear, Jappy, Sad, Surprise, Neutral.",
        "Is there anything considered unsafe for a baby in the environment? If yes, respond with 'Alert:' followed by the event.",
        "Detail the most observable behavior or actions of the baby in the image that correspond to expressions such as crying, smiling, laughing, sleeping, or any other notable actions."
    ]
    
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
        # Try to ping the Redis server to check the connection
        response = r.ping()
        print("Connection successful. Redis server responded:", response)

        # Publish Message
        context = """Imagine that you are a baby monitor. 
                    Currently, this is the baby's current emotion: {}.
                    This is the description of the baby's environment: {}.
                    Finally, this is the baby's action: {}.
                    Your user is a parent who is currently unable to assist the baby.
                    Write a brief summary to inform your user of all details.
                    Write as if you are a friendly young caretaker.
                    """.format(response1, response2, response3)

        r.hset("image-info", '0', context)

    except Exception as e:
        print(f"An error occurred while processing the image: {str(e)}")


if __name__ == "__main__":
    main()
