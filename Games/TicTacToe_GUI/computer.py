import threading
from time import sleep
from random import choice

class Computer:
    def __init__(self, game):
        self.game = game
        self.player = "o"
        self.opponent = "x"

    def start(self):
        self.game.computer_thinking = True
        threading.Thread(target=self.make_move, daemon=True).start()

    def make_move(self):
        sleep(1)
        board = self.game.board

        # Win 
        move = self.find_best("o", board)
        if not move:
            # Block if necessary
            move = self.find_best("x", board)
        if not move:
            # Random move
            move = choice([(r, c) for r in range(3) for c in range(3) if board[r][c] not in ["x", "o"]])

        r, c = move
        self.game.make_move(r, c)

        self.game.computer_thinking = False

        if self.game.check_winner(board):
            self.game.winner = self.game.current_player
            self.game.set_winning_line()
            self.game.game_over = True
            self.game.game_state = "game_over"
        elif self.game.is_board_full():
            self.game.game_over = True
            self.game.game_state = "game_over"
        else:
            self.game.change_turn()

    def find_best(self, symbol, board):
        for r in range(3):
            for c in range(3):
                if board[r][c] not in ["x", "o"]:
                    temp = board[r][c]
                    board[r][c] = symbol
                    if self.game.check_winner(board, symbol):
                        board[r][c] = temp
                        return r, c
                    board[r][c] = temp
        return None
