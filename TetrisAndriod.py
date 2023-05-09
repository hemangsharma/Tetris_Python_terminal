import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from random import randint

class TetrisGame(Widget):
    board = []
    current_piece = []
    next_piece = []
    score = 0

    def __init__(self, **kwargs):
        super(TetrisGame, self).__init__(**kwargs)
        self.board = [[0 for x in range(10)] for y in range(20)]
        self.current_piece = self.generate_piece()
        self.next_piece = self.generate_piece()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def generate_piece(self):
        pieces = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 0], [1, 1], [0, 1]],
            [[0, 1], [1, 1], [1, 0]],
            [[1, 1, 0], [0, 1, 1]]
        ]
        return pieces[randint(0, len(pieces) - 1)]

    def update(self, dt):
        self.move_down()

    def move_down(self):
        # Check if the current piece can move down
        if not self.check_collision(0, -1):
            # Move the piece down
            self.current_piece_y -= 1
        else:
            # Lock the current piece in place
            self.lock_piece()
            # Check for completed rows
            self.check_rows()
            # Spawn the next piece
            self.current_piece = self.next_piece
            self.next_piece = self.generate_piece()

    def lock_piece(self):
        # Add the current piece to the board
        for i in range(len(self.current_piece)):
            for j in range(len(self.current_piece[i])):
                if self.current_piece[i][j] == 1:
                    self.board[self.current_piece_y + i][self.current_piece_x + j] = 1

    def check_rows(self):
        completed_rows = []
        # Check for completed rows
        for i in range(len(self.board)):
            if sum(self.board[i]) == len(self.board[i]):
                completed_rows.append(i)
        # Remove completed rows
        for i in completed_rows:
            self.board.pop(i)
            self.board.insert(0, [0 for x in range(10)])
            self.score += 1

    def check_collision(self, x_offset, y_offset):
        for i in range(len(self.current_piece)):
            for j in range(len(self.current_piece[i])):
                if self.current_piece[i][j] == 1:
                    x = self.current_piece_x + j + x_offset
                    y = self.current_piece_y + i + y_offset
                    if x < 0 or x >= len(self.board[0]) or y < 0 or y >= len(self.board) or self.board[y][x] == 1:
                        return True
        return False

class Tetris
