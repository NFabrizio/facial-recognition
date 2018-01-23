import face_recognition
import face_recognition.cli as face_recognition_cli
import cv2
import os
import random
import sys
import time
from threading import Timer

# Get reference to arguments passed in
known_people_folder = sys.argv[1]

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

answer_options = [
"Cosmo Kramer",
"Elaine Benes",
"George Costanza",
"Jerry Seinfeld"
]

# Add some game functions
def add_point():
    global score
    score += 1

def check_answer(guess, answer):
    global correct_answer
    global guessed
    global random_trivia_set

    if guess == answer:
        set_answer_phrase(guess + " is correct! +1 point!")
        add_point()
        set_correct_answer(True)
        set_timer = Timer(3.0, set_random_trivia_set)
        set_timer.start()
        guessed = ""
    else:
        set_answer_phrase(guess + " is incorrect! -1 point!")
        subtract_point()
        set_correct_answer(False)
        phrase_timer = Timer(3.0, set_answer_phrase, [""])
        phrase_timer.start()
        guessed = ""

# Remove one of the trivia set from the list and return it
def get_random_trivia_set():
    global trivia_length

    trivia_length = len(trivia)
    if trivia_length > 0:
        random_trivia_index = random.randint(0, trivia_length - 1)
        return trivia.pop(random_trivia_index)
    if score > 0:
        return ["Congratulations! You win!", ""]
    return ["Sorry you didn't win. Please play again.", ""]

def points_text(points, name):
    if name in (answer_options):
        return
    elif points == 1:
        return str(points) + " point"
    else:
        return str(points) + " points"

def set_answer_phrase(text):
    global answer_phrase

    answer_phrase = text

def set_correct_answer(bool_value):
    global correct_answer

    correct_answer = bool_value

def set_random_trivia_set():
    global random_trivia_set

    random_trivia_set = get_random_trivia_set()
    set_answer_phrase("")
    return random_trivia_set

def subtract_point():
    global score
    score -= 1

# Initialize some variables
answer_phrase = ""
correct_answer = False
face_locations = []
face_encodings = []
face_names = []
font = cv2.FONT_HERSHEY_DUPLEX
guessed = ""
known_names, known_face_encodings = face_recognition_cli.scan_known_people(known_people_folder)
process_this_frame = True
score = 0
trivia = [
["Who is Jerry's neighbor?", "Cosmo Kramer"],
["Who grew up in a household where they had to be in bed by 9pm?", "Cosmo Kramer"],
["Whose father never made an appearance on the show?", "Cosmo Kramer"],
["Who never completed high school?", "Cosmo Kramer"],
["Who has a sister named Gail?", "Elaine Benes"],
["Who is the worst dancer?", "Elaine Benes"],
["Whose mother never made an appearance on the show?", "Elaine Benes"],
["Who is a Baltimore Orioles fan?", "Elaine Benes"],
["Who worked at the New York Yankees?", "George Costanza"],
["Who starts the master of their domain contest?", "George Costanza"],
["Who cheated on their IQ test?", "George Costanza"],
["Who gets fired from Pendant Publishing?", "George Costanza"],
["Who is the star of Seinfeld?", "Jerry Seinfeld"],
["Who gets sick after eating a black and white cookie?", "Jerry Seinfeld"],
["Who dated Bette Middler's understudy?", "Jerry Seinfeld"],
["Who broke up with the person they were dating because of a commercial?", "Jerry Seinfeld"]
]
trivia_length = 0

# Set video screen width
cv_frame_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)

# Set the initial random trivia set
set_random_trivia_set()

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Render trivia question box, random question and answer phrase
    cv2.rectangle(frame, (0, 0), (int(cv_frame_width), 100), (255, 0, 128), cv2.FILLED)
    cv2.putText(frame, random_trivia_set[0], (6, 35), font, 1.0, (255, 255, 255), 1)
    cv2.putText(frame, answer_phrase, (6, 70), font, 1.0, (255, 255, 255), 1)

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Render trivia question box, random question and answer phrase again to avoid flicker
        cv2.rectangle(frame, (0, 0), (int(cv_frame_width), 100), (255, 0, 128), cv2.FILLED)
        cv2.putText(frame, random_trivia_set[0], (6, 35), font, 1.0, (255, 255, 255), 1)
        cv2.putText(frame, answer_phrase, (6, 70), font, 1.0, (255, 255, 255), 1)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Loop through all matches and set the name to the known name where a match exists
            for index, match in enumerate(matches):
                if match:
                    name = known_names[index]

            face_names.append(name)

            if name in (answer_options):
                # Only check the answer the first time or if it is different from the last check
                if name != guessed:
                    check_answer(name, random_trivia_set[1])
                guessed = name

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom + 70), (right, bottom), (255, 0, 0), cv2.FILLED)

        cv2.putText(frame, name, (left + 6, bottom + 30), font, 1.0, (255, 255, 255), 1)
        cv2.putText(frame, points_text(score, name), (left + 6, bottom + 60), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
