
# Game Project
================

This project is a simple game written in Python using the Pygame library.

## main.py
------------

This is the main entry point of the game. It initializes the game window, sets up the game loop, and handles user input. The game loop updates the game state, draws the game objects, and checks for collisions.

## classes/Enemy.py
-------------------

This file contains the `Enemy` class, which represents a game enemy. The `Enemy` class has attributes such as `health`, `speed`, and `position`, and methods such as `move` and `update_visibility`. The `Enemy` class is used to create multiple enemy objects in the game.

## classes/Player.py
-------------------

This file contains the `Player` class, which represents the game player. The `Player` class has attributes such as `health`, `speed`, and `position`, and methods such as `move` and `update_visibility`. The `Player` class is used to create a single player object in the game.

## Game Overview
----------------

The game is a simple shooter where the player must avoid enemies and collect power-ups. The game uses a tile-based system for the game world, and the player and enemies move around on the screen.

## Requirements
------------

* Python 3.x
* Pygame library

## Running the Game
-------------------

To run the game, simply execute the `main.py` file using Python:

```bash
python main.py
```

This will launch the game window, and you can start playing the game using the keyboard and mouse.