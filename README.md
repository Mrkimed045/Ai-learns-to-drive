# Ai-learns-to-drive
This is a 2D simulation of AI-learns-to-drive. Program is imagined as a 2D game where you draw a racing track using your mouse, and letting the car learn how to pass the track on its own. Program uses a small neural network to control the car, and to get the right weights for the neural network I used genetic algorithm to find better solutions.
## Installation
I would recommend using virtual environment. I used `conda` virtual environment. To create virtual environment with `conda` type:
```
conda create -n AI_env python=3.10
```
After installing all the packages you need to activate the virtual environment by typing:
```
conda activate AI_env
```
Now you have to install the dependencies:
```
pip install pyglet
pip install tensorflow
```
That's all. Clone or download the code, and run the command:
```
python GameWindow.py
```

## How to use
When the canvas opens you can start drawing the racing track. Drawing and placing the car on track is done by several steps:
- draw one side of the racing track by continuously pressing `left mouse key` on the canvas
- when you are done, press the `middle mouse key` to start drawing det second side
- draw the second side of the racing track by continuously pressing the `left mouse key`
- when you are done, press the `middle mouse key` to start drawing the reward checkpoints (Reward checkpoints are green lines you have to draw on the racing track for the car to learn how to pass the track. Checkpoints have to be drawn one after the other on the track(order matters)).
- draw the checkpoints (Two `left mouse key` presses = one checkpoint) (check the photo below for better understanding) (more checkpoints = better fitness score) 
- when you are done, press the `middle mouse key`, and with your `left mouse key` place the car on the track, place it in front of the first checkpoint you drawn!
- press the `middle mouse key` and let the car drive.

![track](https://user-images.githubusercontent.com/45481420/195551249-e6599f88-f715-4a86-9219-fae5ec5821b5.PNG)

## NOTES
Car is driving the track in a loop. When he passes 3 loops he restarts. First 5 runs are pre learned agents I learned using this method. After them car is controlled by the neural network with random weight parameters, which wont be very effective (learning process starts agian).
