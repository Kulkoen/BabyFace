import os
from google.cloud import aiplatform
import vertexai
from vertexai.vision_models import ImageTextModel, Image

PROJECT_ID = "vertex-ai-qa"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

def main():
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = ImageTextModel.from_pretrained("imagetext@001")

    # Assuming the "Images" folder is within the GitHub repository directory
    #current_directory = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of your Python script
    #images_path = os.path.join(current_directory, 'Images')
    images_path = "/Users/lukehartzell/HappyBaby/HappyBaby/Images/"

    # Load the image from the specified path within the "Images" folder
    image_filename = 'baby_by_chemicals.jpeg'
    source_image_path = os.path.join(images_path, image_filename)

    try:
        if os.path.exists(source_image_path):
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
            print(response1)
            print(response2)
            print(response3)
        
        else:
            print(f"Image file '{image_filename}' not found in the specified location: '{source_image_path}'")
    except Exception as e:
        print(f"An error occurred while processing the image: {str(e)}")

if __name__ == "__main__":
    main()
