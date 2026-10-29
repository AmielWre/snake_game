"""
renderer.py - Everything that draws on the screen.

All curses drawing code lives here, so the other files only deal with
game logic. Screen layout (top to bottom):

    row 0         score panel
    rows 1 ...    playfield with a border around it
"""

import curses

import config

# Turn the color names from config.py into curses colors
COLOR_NAMES = {
    "black": curses.COLOR_BLACK,
    "red": curses.COLOR_RED,
    "green": curses.COLOR_GREEN,
    "yellow": curses.COLOR_YELLOW,
    "blue": curses.COLOR_BLUE,
    "magenta": curses.COLOR_MAGENTA,
    "cyan": curses.COLOR_CYAN,
    "white": curses.COLOR_WHITE,
}

# Space needed: the playfield plus 2 for the border, plus 1 row for the score
NEEDED_ROWS = config.HEIGHT + 3
NEEDED_COLS = config.WIDTH + 2


class Renderer:
    """Draws the snake, food, border, score and messages using curses."""

    def __init__(self, stdscr):
        """Set up curses and colors, and create the windows if the terminal is big enough."""
        self.stdscr = stdscr
        curses.curs_set(0)  # hide the blinking cursor
        stdscr.keypad(True)  # let curses understand arrow keys

        if curses.has_colors():
            curses.start_color()
            self.add_color_pair(config.SNAKE_PAIR, config.SNAKE_COLOR)
            self.add_color_pair(config.FOOD_PAIR, config.FOOD_COLOR)
            self.add_color_pair(config.BORDER_PAIR, config.BORDER_COLOR)
            self.add_color_pair(config.SCORE_PAIR, config.SCORE_COLOR)

        self.score_win = None
        self.field_win = None
        if self.is_big_enough():
            self.score_win = curses.newwin(1, NEEDED_COLS, 0, 0)
            self.field_win = curses.newwin(config.HEIGHT + 2, NEEDED_COLS, 1, 0)

    def add_color_pair(self, pair_number, color_name):
        """Register a color pair: the given text color on a black background."""
        curses.init_pair(pair_number, COLOR_NAMES[color_name], curses.COLOR_BLACK)

    def color(self, pair_number):
        """Return the curses attribute for a color pair (or plain text if no colors)."""
        if curses.has_colors():
            return curses.color_pair(pair_number)
        return curses.A_NORMAL

    def is_big_enough(self):
        """Return True if the terminal can fit the whole game."""
        rows, cols = self.stdscr.getmaxyx()
        return rows >= NEEDED_ROWS and cols >= NEEDED_COLS

    def draw_too_small(self):
        """Tell the player to make the terminal bigger."""
        self.stdscr.erase()
        lines = [
            "Terminal too small!",
            "Need {} x {}.".format(NEEDED_COLS, NEEDED_ROWS),
            "Resize, then restart.",
            "Press any key to quit.",
        ]
        rows, cols = self.stdscr.getmaxyx()
        for i, line in enumerate(lines):
            if i < rows:
                # addnstr cuts the text so it never goes past the screen edge
                self.stdscr.addnstr(i, 0, line, cols - 1)
        self.stdscr.refresh()

    def draw_border(self):
        """Clear the playfield and draw a box around it."""
        self.field_win.erase()
        self.field_win.attron(self.color(config.BORDER_PAIR))
        self.field_win.box()
        self.field_win.attroff(self.color(config.BORDER_PAIR))

    def draw_cell(self, y, x, char, attributes):
        """Draw one character in the playfield (+1 skips over the border)."""
        self.field_win.addstr(y + 1, x + 1, char, attributes)

    def draw_snake(self, body):
        """Draw the snake: a bright green head and a green body."""
        snake_color = self.color(config.SNAKE_PAIR)
        for y, x in body[1:]:
            self.draw_cell(y, x, "o", snake_color)
        head_y, head_x = body[0]
        self.draw_cell(head_y, head_x, "@", snake_color | curses.A_BOLD)

    def draw_food(self, pos):
        """Draw the food as a red '*'."""
        y, x = pos
        self.draw_cell(y, x, "*", self.color(config.FOOD_PAIR) | curses.A_BOLD)

    def clear_cell(self, y, x):
        """Erase one cell of the playfield (used when the tail moves away)."""
        self.draw_cell(y, x, " ", curses.A_NORMAL)

    def draw_score(self, score, level, high_score):
        """Draw the score panel above the playfield."""
        text = " Score: {}  Level: {}  Best: {}".format(score, level, high_score)
        self.score_win.erase()
        self.score_win.addnstr(0, 0, text, NEEDED_COLS - 1, self.color(config.SCORE_PAIR))

    def draw_centered(self, lines):
        """Draw a few lines of text in the middle of the playfield."""
        first_row = (config.HEIGHT + 2 - len(lines)) // 2
        for i, line in enumerate(lines):
            col = (NEEDED_COLS - len(line)) // 2
            self.field_win.addstr(first_row + i, col, line, curses.A_BOLD)

    def draw_start_screen(self):
        """Show the welcome screen with the controls."""
        self.draw_border()
        self.score_win.erase()
        self.draw_centered([
            "S N A K E",
            "",
            "Move:  arrow keys or WASD",
            "Quit:  Q",
            "",
            "Press any key to start",
        ])

    def draw_game_over(self, score):
        """Show the game over message with the final score."""
        self.draw_centered([
            "  GAME OVER  ",
            " Final score: {} ".format(score),
            "",
            " R = restart   Q = quit ",
        ])

    def refresh(self):
        """Push everything drawn so far to the real screen."""
        self.score_win.noutrefresh()
        self.field_win.noutrefresh()
        curses.doupdate()  # one screen update instead of two = less flicker
