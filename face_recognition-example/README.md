# face_recognition Example

This is a more complex example similar to the one Adam provides in his library for
use with his face_recognition library. This example builds off of his webcam live
facial recognition example which lives in the file at [examples/facerec_from_webcam_faster.py](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py).
This example will run similar to the gif that Adam has in his README where you see
a red box around each face with their name, but will allow you to upload images to
a directory for known faces and supply that directory name as an argument to the
application.

## Installation and Set Up  
Below are the instructions for installing this application.
*These instructions are valid as of 2018.01.18*

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
  `cd ~/path/to/facial-recognition-directory/face_recognition-example`
4. Start the application with the command  
   `python3 facial-recognition-webcam-complex.py [path-to-directory-with-known-face-images]`  
   path-to-directory-with-known-face-images should be the path to the directory
   containing the images with the faces you want the application to recognize with
   the file name for each being the name you want the application to display when
   it recognizes their face.

## Application Use  

After following the instructions above for setting up the environment and making
sure you have added images of the faces you want the application to recognize into
the directory with known face images and that the application is running with the
command listed above, make sure you have your focus on the Python window running
the application. This Python window should be showing the view from the web camera
on your machine. Once one of the known faces is in view of the web camera, you
should see a red box appear around the face with the person's name at the bottom
of the red box. To change how the name is displayed, simply change the file name
for the image. The application will display the name exactly as it is typed for
the file name (e.g., file name "bob-jones.jpg" will be displayed as "bob-jones",
"Bob Jones.jpg" will be displayed as "Bob Jones"). The application will also
recognize known faces in photographs or from images on another device (phone,
tablet, etc.).

To stop the project from running, return to the terminal window that the application
was started from and type `command + C`.
