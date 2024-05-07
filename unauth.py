import cv2
import face_recognition
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Global variable to track the last time an email was sent
last_email_time = 0

# Function to send email
def send_email(recognized_person):
    global last_email_time
    current_time = time.time()
    
    # Check if it's been less than 2 minutes since the last email was sent
    if current_time - last_email_time < 120:
        return  # Skip sending the email
        
    # Email configuration
    sender_email = "muditert34@gmail.com"
    receiver_email = "muditert34@gmail.com"
    password = "otzbxqvmoeoihfoe"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Recognized Person Detected!"

    # Email content
    body = f"A recognized person, {recognized_person}, has been detected."
    msg.attach(MIMEText(body, 'plain'))

    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login to Gmail
    server.login(sender_email, password)

    # Send email
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)

    # Close the connection
    server.quit()
    
    # Update the last email time
    last_email_time = current_time

# Load known face encodings & names
known_face_encodings = []
known_face_names = []

# Load known faces & their names
known_person1_image = face_recognition.load_image_file("ElonMusk.jpg")
known_person2_image = face_recognition.load_image_file("Srk.jpg")
known_person3_image = face_recognition.load_image_file("Mudit.jpg")

known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]
known_person3_encoding = face_recognition.face_encodings(known_person3_image)[0]

known_face_encodings.append(known_person1_encoding)
known_face_encodings.append(known_person2_encoding)
known_face_encodings.append(known_person3_encoding)

known_face_names.append("Elon Musk")
known_face_names.append("Srk")
known_face_names.append("Mudit")

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame by frame
    ret, frame = video_capture.read()

    # Find all face location in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each frame found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Intruder"
        box_color = (0, 0, 255)  # Red color for intruder

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            box_color = (0, 255, 0)  # Green color for recognized person
            
            # If the recognized person is not an intruder, send an email
            if name != "Intruder":
                send_email(name)

        # Draw a box around the face & label the name
        cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, box_color, 2)

    # Display the resulting frame
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV
video_capture.release()
cv2.destroyAllWindows()