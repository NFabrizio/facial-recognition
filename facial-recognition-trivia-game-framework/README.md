# Facial Recognition Trivia Game Framework

This is built from the complex face_recognition example at [face_recognition-example/facial-recognition-webcam-complex.py](https://github.com/NFabrizio/facial-recognition/blob/master/face_recognition-example/facial-recognition-webcam-complex.py).
This game will run similarly to the example, but also allows the ability to supply
custom question sets and known faces. It will also keep track of the number of
points a player earns by answering questions (it actually adds a point for each
correct answer and subtracts a point for each incorrect answer). To win the game,
the player must have a positive score once all the questions have been answered.

## Installation and Set Up  
Below are the instructions for installing this application.
*These instructions are valid as of 2018.01.31*

### Environment Set Up  
To get this example running, you will need to do a bit of set up and importing of
third-party libraries.
1. Install Python 3 and dlib.  
   Follow the instructions at https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf.
2. Clone this repository to your local environment.
  1. Fork this Github repo.
    1. In a web browser, visit https://github.com/NFabrizio/facial-recognition
    2. Click the Fork button in the upper right corner of the screen
    3. In the "Where should we fork this repository?" pop up, select your username.
    Github should create a fork of the repo in your account
  2. Clone your fork of the facial-recognition repo.
    1. In the terminal on your local environment, navigate to the directory where
    you want to clone the facial-recognition repo  
      `cd ~/path/to/your/directory`
    2. In the terminal, run:  
      `git clone [clone-url-for-your-fork]`  
      The URL should be in the format `git@github.com:YourUsername/facial-recognition.git`
3. In the terminal on your local environment, navigate to the facial recognition
   example  
  `cd ~/path/to/facial-recognition-directory/facial-recognition-trivia-game-framework`
4. Create a configuration file named config.py with question sets and answer options
   in the same directory as the facial-recognition-trivia-game-framework.py file.
5. Create a knowns directory and add images of the known faces you want the application
   to recognize, naming the image files with the names you want the application
   to use. These names should match the names you supplied for the answer options.
6. Start the application with the command  
   `python3 facial-recognition-trivia-game-framework.py`  

## Application Use  

After following the instructions above for setting up the environment and making
sure you have added images of the faces you want the application to recognize into
the directory with known face images and that the application is running with the
command listed above, make sure you have your focus on the Python window running
the application. This Python window should be showing the view from the web camera
on your machine. Once one of the known faces is in view of the web camera, you
should see a blue box appear around the face with the person's name at the bottom
of the blue box (if you have added their image to the `knowns` directory). To change
how the name is displayed, simply change the file name for the image. The
application will display the name exactly as it is typed for the file name (e.g.,
file name "bob-jones.jpg" will be displayed as "bob-jones", "Bob Jones.jpg" will
be displayed as "Bob Jones").  

This framework is currently only set up to allow one player to play at a time.

When the application loads, it will display a random trivia question from the list
supplied in the configuration file. To answer the question, find an image of the
character/person, that is the answer to the question, on another device or an actual
photograph of the character and hold it in view of the web camera. The application
should recognize the character's/person's face, and tell the player that the answer
is either correct or incorrect. A correct answer will earn the player 1 point. An
incorrect answer will cost the player one point.  

The game ends when all of the questions have been answered. If the player has a
positive score at the end of the game, that player wins. If they have a score of
zero or less, they lose.

To stop the application from running, return to the terminal window that the
application was started from and type `command + C`.  

# Configuration Settings

This framework requires some configuration to work properly. There are some required
configuration values and some optional ones. They are listed and described below.  
*To see an example of a configuration file, view the config example included with
this framework at [facial-recognition/facial-recognition-trivia-game-framework/examples/config.py](https://github.com/NFabrizio/facial-recognition/blob/master/facial-recognition-trivia-game-framework/examples/config.py)*  

## Required Configuration  

The minimum amount of configuration is to create a config.py file and add two
variables to it, answer_options and trivia_sets.  
`answer_options` = a Python list data type containing strings with possible answers  
`trivia_sets` = Python list data type containing lists of string pairs with the
first string being the question and the second string being the answer to the question  

## Optional Configuration

`color_bg` = Python dictionary with values for r, g and b (red, green and blue)
which will be used for the background color for the question display
`color_box` = Python dictionary with values for r, g and b (red, green and blue)
which will be used for the box around faces
`color_text` = Python dictionary with values for r, g and b (red, green and blue)
which will be used for the text color
`loser_phrase` = String containing text to display when the player loses the game
`winner_phrase` = String containing text to display when the player wins the game
