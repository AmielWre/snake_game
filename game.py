"""
game.py - Start here! The main game loop for Snake.

Run with:  python game.py

This file connects the pieces: it reads the keyboard, moves the
snake, checks for collisions and food, and asks the renderer to draw.
"""

import curses

import config
from food import Food
from renderer import Renderer
from score import Score
from snake import Snake

# Which key turns the snake which way (arrow keys + WASD)
KEY_DIRECTIONS = {
    curses.KEY_UP: "UP",
    curses.KEY_DOWN: "DOWN",
    curses.KEY_LEFT: "LEFT",
    curses.KEY_RIGHT: "RIGHT",
    ord("w"): "UP",
    ord("W"): "UP",
    ord("s"): "DOWN",
    ord("S"): "DOWN",
    ord("a"): "LEFT",
    ord("A"): "LEFT",
    ord("d"): "RIGHT",
    ord("D"): "RIGHT",
}
QUIT_KEYS = (ord("q"), ord("Q"))
RESTART_KEYS = (ord("r"), ord("R"))


def is_outside_field(pos):
    """Return True if the position is outside the playfield (in a wall)."""
    y, x = pos
    return y < 0 or y >= config.HEIGHT or x < 0 or x >= config.WIDTH


def wrap_position(pos):
    """Move a position that left the playfield to the opposite side."""
    y, x = pos
    # % (modulo) turns -1 into the last row/column and HEIGHT/WIDTH into 0
    return (y % config.HEIGHT, x % config.WIDTH)


def play_round(stdscr, renderer):
    """Play one game until the snake dies. Return (score, player_quit)."""
    snake = Snake(config.HEIGHT // 2, config.WIDTH // 2)
    food = Food(config.HEIGHT, config.WIDTH)
    score = Score()
    food.spawn(snake.get_body())

    stdscr.timeout(config.INITIAL_SPEED)  # getch() waits this many ms = one frame
    renderer.draw_border()

    while True:
        key = stdscr.getch()  # -1 if no key was pressed during this frame
        if key in QUIT_KEYS:
            return score, True
        if key in KEY_DIRECTIONS:
            snake.change_direction(KEY_DIRECTIONS[key])

        new_head = snake.move()

        # Wall collision
        if is_outside_field(new_head):
            if config.WRAP_AROUND:
                new_head = wrap_position(new_head)
                snake.replace_head(new_head)
            else:
                return score, False

        if snake.check_self_collision():
            return score, False

        if food.is_eaten(new_head):
            snake.grow()
            if score.add_point():
                speed = score.level_up()
                stdscr.timeout(speed)  # faster frames = faster snake
            food.spawn(snake.get_body())

        # Draw this frame
        tail = snake.get_removed_tail()
        if tail is not None:
            renderer.clear_cell(tail[0], tail[1])
        renderer.draw_food(food.get_position())
        renderer.draw_snake(snake.get_body())
        renderer.draw_score(score.score, score.level, score.high_score)
        renderer.refresh()


def main(stdscr):
    """Run the whole game: start screen, rounds, and game over screens."""
    renderer = Renderer(stdscr)
    if not renderer.is_big_enough():
        renderer.draw_too_small()
        stdscr.getch()
        return

    renderer.draw_start_screen()
    renderer.refresh()
    if stdscr.getch() in QUIT_KEYS:
        return

    while True:
        score, player_quit = play_round(stdscr, renderer)
        score.save_high_score()
        if player_quit:
            return

        renderer.draw_score(score.score, score.level, score.high_score)
        renderer.draw_game_over(score.score)
        renderer.refresh()

        # Wait (no timeout) until the player picks restart or quit
        stdscr.timeout(-1)
        key = stdscr.getch()
        while key not in RESTART_KEYS and key not in QUIT_KEYS:
            key = stdscr.getch()
        if key in QUIT_KEYS:
            return


if __name__ == "__main__":
    curses.wrapper(main)  # sets up the terminal and restores it, even after a crash
