"""
food.py - The Food class.

There is always exactly one piece of food on the playfield.
When the snake eats it, a new piece is spawned somewhere else.
"""

import random


class Food:
    """A piece of food at a random free cell of the playfield."""

    def __init__(self, height, width):
        """Remember the playfield size so food is always placed inside it."""
        self.height = height
        self.width = width
        self.position = (0, 0)

    def spawn(self, snake_body):
        """Move the food to a random cell that the snake is not on."""
        while True:
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)
            if (y, x) not in snake_body:
                break  # found a free cell
        self.position = (y, x)

    def get_position(self):
        """Return the (y, x) position of the food."""
        return self.position

    def is_eaten(self, head_pos):
        """Return True if the snake's head is on the food."""
        return head_pos == self.position
