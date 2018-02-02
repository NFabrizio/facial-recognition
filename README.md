# Facial Recognition Repo

This repo contains a few directories with code that uses facial recognition inside
of Python scripts.  

The [face_recognition-example](https://github.com/NFabrizio/facial-recognition/tree/master/face_recognition-example)
directory is just a sample script that builds on the work of Adam Geitgey. Once
the environment is properly set up, it will run using the web camera on your
computer and render a red box with the names of the faces it has been trained to
recognize around each face it recognizes.  

The [seinfeld-game](https://github.com/NFabrizio/facial-recognition/tree/master/seinfeld-game)
directory contains everything you need to be able to run a Seinfeld trivia game
using facial recognition. Once the environment is properly set up, it will run
using the web camera on your computer and render a red box with the names of the
faces it has been trained to recognize around each face it recognizes along with the
number of points they have earned. It will also display a randomly selected trivia
question at the top of the screen, and will add/subtract points for correct/incorrect
answers provided by the player. Answers are submitted by placing an image of the
Seinfeld character in view of the web camera.

The [facial-recognition-trivia-game-framework](https://github.com/NFabrizio/facial-recognition/tree/master/facial-recognition-trivia-game-framework)
directory is a framework built from the face_recognition-example and seinfeld-game.
It is configurable for creating facial recognition trivia games with any images,
questions and answers and also allows configuration of color schemes and text.
