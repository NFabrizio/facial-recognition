import face_recognition
import face_recognition.cli as face_recognition_cli
import cv2
import os
import random
import sys
import time
from threading import Timer
import importlib

# Set some default values
default_knowns_dir = "knowns"
default_winner_phrase = "Congratulations! You win!"
default_loser_phrase = "Sorry you didn't win. Please play again."
default_bg_color = {
"r": 128,
"g": 0,
"b": 255
}
default_box_color = {
"r": 0,
"g": 0,
"b": 255
}
default_text_color = {
"r": 255,
"g": 255,
"b": 255
}

def module_exists(module_name):
    try:
        global config
        config = importlib.import_module(module_name)
    except ImportError:
        return False
    else:
        return True

# Attempt to import config file
module_exists("config")

# If no known faces directory found, try the default and if still not found, exit the script
try:
    sys.argv[1]
except IndexError:
    # Check if default directory exists
    if os.path.isdir(default_knowns_dir):
        known_people_folder = default_knowns_dir
    else:
        print("*****************************************************************************************")
        print("No known faces directory supplied. Known faces directory required for application to run.")
        print("*****************************************************************************************")
        sys.exit()
else:
    # If argument passed in, check that is a directory
    if os.path.isdir(sys.argv[1]):
        known_people_folder = sys.argv[1]
    elif (sys.argv[1]):
        print("*****************************************************************************************")
        print(sys.argv[1] + " is not a directory. Known faces directory required for application to run.")
        print("*****************************************************************************************")
        sys.exit()

try:
    config
except NameError:
    try:
        # If there is no config file found, attempt to import the index 2 argument supplied when the script was run
        sys.argv[2]
    except IndexError:
        print("*************************************************************************")
        print("No configuration supplied. Configuration required for application to run.")
        print("*************************************************************************")
        sys.exit()
    else:
        module_exists(sys.argv[2])

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Set up configuration
answer_options = ""
trivia = []

# Make sure there are answer_options
try:
    config.answer_options
except AttributeError:
    print("***************************************************************************")
    print("No answer options supplied. Answer options required for application to run.")
    print("***************************************************************************")
    sys.exit()
else:
    answer_options = config.answer_options

# Make sure there are trivia sets
try:
    config.trivia
except AttributeError:
    print("*********************************************************************")
    print("No trivia sets supplied. Trivia sets required for application to run.")
    print("*********************************************************************")
    sys.exit()
else:
    trivia = config.trivia

# Check whether custom colors were provided
try:
    config.color_bg
except AttributeError:
    color_bg = default_bg_color
else:
    color_bg = config.color_bg

try:
    config.color_box
except AttributeError:
    color_box = default_box_color
else:
    color_box = config.color_box

try:
    config.color_text
except AttributeError:
    color_text = default_text_color
else:
    color_text = config.color_text

# Check whether custom winner and loser phrases were provided
try:
    config.loser_phrase
except AttributeError:
    loser_phrase = default_loser_phrase
else:
    loser_phrase = config.loser_phrase

try:
    config.winner_phrase
except AttributeError:
    winner_phrase = default_winner_phrase
else:
    winner_phrase = config.winner_phrase

# Add some game functions
def add_point():
    global score
    score += 1

def check_answer(guess, answer):
    global correct_answer
    global random_trivia_set

    if guess == answer:
        set_answer_phrase(guess + " is correct! +1 point!")
        add_point()
        set_correct_answer(True)
        set_timer = Timer(3.0, set_random_trivia_set)
        set_timer.start()
    else:
        set_answer_phrase(guess + " is incorrect! -1 point!")
        subtract_point()
        set_correct_answer(False)
        phrase_timer = Timer(3.0, set_answer_phrase, [""])
        phrase_timer.start()

# Remove one of the trivia set from the list and return it
def get_random_trivia_set():
    global trivia_length

    trivia_length = len(trivia)
    if trivia_length > 0:
        random_trivia_index = random.randint(0, trivia_length - 1)
        return trivia.pop(random_trivia_index)
    if score > 0:
        return [winner_phrase, ""]
    return [loser_phrase, ""]

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

def set_guessed(guess):
    global guessed

    guessed = guess

def set_random_trivia_set():
    global random_trivia_set

    random_trivia_set = get_random_trivia_set()
    set_answer_phrase("")
    set_guessed("")
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
trivia_length = 0

# Set video screen width
cv_frame_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)

# Set the initial random trivia set
set_random_trivia_set()

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Render trivia question box, random question and answer phrase
    cv2.rectangle(frame, (0, 0), (int(cv_frame_width), 100), (color_bg["b"], color_bg["g"], color_bg["r"]), cv2.FILLED)
    cv2.putText(frame, random_trivia_set[0], (6, 35), font, 1.0, (color_text["b"], color_text["g"], color_text["r"]), 1)
    cv2.putText(frame, answer_phrase, (6, 70), font, 1.0, (color_text["b"], color_text["g"], color_text["r"]), 1)

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Render trivia question box, random question and answer phrase again to avoid flicker
        cv2.rectangle(frame, (0, 0), (int(cv_frame_width), 100), (color_bg["b"], color_bg["g"], color_bg["r"]), cv2.FILLED)
        cv2.putText(frame, random_trivia_set[0], (6, 35), font, 1.0, (color_text["b"], color_text["g"], color_text["r"]), 1)
        cv2.putText(frame, answer_phrase, (6, 70), font, 1.0, (color_text["b"], color_text["g"], color_text["r"]), 1)

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
                set_guessed(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (color_box["b"], color_box["g"], color_box["r"]), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom + 70), (right, bottom), (color_box["b"], color_box["g"], color_box["r"]), cv2.FILLED)

        cv2.putText(frame, name, (left + 6, bottom + 30), font, 1.0, (color_text["b"], color_text["g"], color_text["r"]), 1)
        cv2.putText(frame, points_text(score, name), (left + 6, bottom + 60), font, 1.0, (color_text["b"], color_text["g"], color_text["r"]), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
