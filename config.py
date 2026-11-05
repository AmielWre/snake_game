"""
config.py - Game settings for Snake.

Change the numbers here to tweak the game. No other file
should contain "magic numbers" for size, speed or colors.
"""

# Size of the playfield, measured inside the border
WIDTH = 40
HEIGHT = 20

# Speed: milliseconds per frame (lower = faster)
INITIAL_SPEED = 120
SPEED_INCREMENT = 8   # how many ms faster each new level is
MIN_SPEED = 50         # the game never gets faster than this
LEVEL_UP_SCORE = 5     # points needed for each level up

# If True, the snake comes out the other side instead of dying at a wall
WRAP_AROUND = False

# Color pair numbers (curses refers to color pairs by number)
SNAKE_PAIR = 1
FOOD_PAIR = 2
BORDER_PAIR = 3
SCORE_PAIR = 4

# Color names for each pair (renderer.py turns these into curses colors)
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BORDER_COLOR = "blue"
SCORE_COLOR = "red"
