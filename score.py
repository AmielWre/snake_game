"""
score.py - Score, level and high score tracking.

The high score is saved in highscore.txt next to this file, so it
survives between games. That file is created the first time a
high score is saved.
"""

import os

import config

# Always use the highscore.txt in the game folder, no matter where we run from
HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")


class Score:
    """Keeps track of the current score, level and best score ever."""

    def __init__(self):
        """Start a new game: score 0, level 1, and load the saved high score."""
        self.score = 0
        self.level = 1
        self.high_score = self.get_high_score()

    def add_point(self):
        """Add one point. Return True if the player has earned a level up."""
        self.score += 1
        return self.score % config.LEVEL_UP_SCORE == 0

    def level_up(self):
        """Go up one level and return the new frame speed in milliseconds."""
        self.level += 1
        # Level 1 runs at INITIAL_SPEED, every level after that is a bit faster
        speed = config.INITIAL_SPEED - (self.level - 1) * config.SPEED_INCREMENT
        if speed < config.MIN_SPEED:
            speed = config.MIN_SPEED
        return speed

    def save_high_score(self):
        """Write the score to highscore.txt if it beats the old high score."""
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open(HIGHSCORE_FILE, "w") as f:
                    f.write(str(self.high_score))
            except OSError:
                pass  # can't write the file (e.g. read-only folder) - not worth crashing for

    def get_high_score(self):
        """Read the high score from highscore.txt, or return 0 if there is none."""
        try:
            with open(HIGHSCORE_FILE) as f:
                return int(f.read().strip())
        except (OSError, ValueError):
            # File missing, unreadable, empty or not a number
            return 0
