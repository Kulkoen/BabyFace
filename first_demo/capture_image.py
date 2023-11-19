# Task: Capture an Image Subscriber

import cv2
import time

# Open a connection to the camera (0 represents the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set the frame width and height (you can adjust these values)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Variable to keep track of captured image index
image_index = 0

# Time at which the last image was captured
last_capture_time = time.time()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Camera Feed', frame)

    # Check if 10 seconds have passed since the last image capture
    current_time = time.time()
    if current_time - last_capture_time >= 1:
        # Save the frame as an image
        image_filename = f"./images/captured_image_{image_index}.jpeg"
        cv2.imwrite(image_filename, frame)
        print(f"Image saved as {image_filename}")
        last_capture_time = current_time  # Update the last capture time

    # Check if the 'Esc' key is pressed (to exit)
    key = cv2.waitKey(1)
    if key == 27:
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
