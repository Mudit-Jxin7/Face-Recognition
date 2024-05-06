import cv2
import face_recognition

# Load known face encodings & names

known_face_encodings = []
known_face_names = []

# Load known faces & their names

known_person1_image = face_recognition.load_image_file("/home/muditjain/Desktop/iot/ElonMusk.jpg")
known_person2_image = face_recognition.load_image_file("/home/muditjain/Desktop/iot/Srk.jpg")

known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]

known_face_encodings.append(known_person1_encoding)
known_face_encodings.append(known_person2_encoding)

known_face_names.append("Elon Musk")
known_face_names.append("Srk")

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
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        #Draw a box around the box & label the face_encoding
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV

video_capture.release()
cv2.destroyAllWindows()