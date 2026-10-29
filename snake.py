"""
snake.py - The Snake class.

The snake is a list of (y, x) positions. The head is the first
item and the tail is the last item. Positions are measured inside
the playfield, so (0, 0) is the top-left cell inside the border.
"""

from collections import deque

# How one step in each direction changes (y, x)
DIRECTION_STEPS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}

# The snake is not allowed to turn straight back into itself
OPPOSITE_DIRECTIONS = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
}


class Snake:
    """A snake that moves around the playfield and grows when it eats."""

    def __init__(self, start_y, start_x):
        """Create a snake of length 3 with its head at (start_y, start_x), facing right."""
        self.direction = "RIGHT"
        self.body = deque()  # deque = fast to add/remove at both ends
        for i in range(3):
            # Each segment is one cell to the left of the previous one
            self.body.append((start_y, start_x - i))
        self.growing = False
        self.removed_tail = None  # the cell the tail left on the last move

    def move(self):
        """Move one step in the current direction and return the new head position."""
        head_y, head_x = self.get_head()
        step_y, step_x = DIRECTION_STEPS[self.direction]
        new_head = (head_y + step_y, head_x + step_x)
        self.body.appendleft(new_head)

        if self.growing:
            # Keep the tail this time, so the snake gets one cell longer
            self.growing = False
            self.removed_tail = None
        else:
            self.removed_tail = self.body.pop()
        return new_head

    def grow(self):
        """Make the snake one cell longer on its next move."""
        self.growing = True

    def change_direction(self, new_dir):
        """Turn the snake, unless new_dir would reverse it into itself."""
        if new_dir != OPPOSITE_DIRECTIONS[self.direction]:
            self.direction = new_dir

    def replace_head(self, new_head):
        """Move the head to a different cell (used when wrapping around walls)."""
        self.body[0] = new_head

    def get_direction(self):
        """Return the current direction as a string."""
        return self.direction

    def get_head(self):
        """Return the (y, x) position of the head."""
        return self.body[0]

    def get_body(self):
        """Return all segments as a list, head first."""
        return list(self.body)

    def get_removed_tail(self):
        """Return the cell the tail left on the last move, or None if it grew."""
        return self.removed_tail

    def check_self_collision(self):
        """Return True if the head is on top of another body segment."""
        head = self.get_head()
        rest_of_body = self.get_body()[1:]
        return head in rest_of_body
