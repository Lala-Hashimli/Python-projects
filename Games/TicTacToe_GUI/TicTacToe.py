import pygame
import sys
from config import *
from computer import Computer

pygame.init()

class TicTacToe:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
        pygame.display.set_caption("Tic Tac Toe")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 28)
        self.big_font = pygame.font.SysFont('Arial', 36)
        self.number_font = pygame.font.SysFont('Verdana', 48)
        self.reset_game()
        self.game_state = "mode_selection"

    def reset_game(self):
        self.board = [[str(i*3 + j + 1) for j in range(3)] for i in range(3)]
        self.current_turn = "x"
        self.current_player = "Player 1"
        self.players = ["Player 1", "Player 2"]
        self.player_mode = None
        self.winner = None
        self.game_over = False
        self.computer_thinking = False
        self.winning_line = None

    def draw_background(self):
        self.screen.fill(LIGHT_GRAY)

    def draw_grid(self):
        self.draw_background()
        for i in range(1, GRID_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), LINE_WIDTH)
            pygame.draw.line(self.screen, DARK_GRAY, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), LINE_WIDTH)

    def draw_marks(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                val = self.board[row][col]
                if val == "x":
                    self.draw_cross(row, col)
                elif val == "o":
                    self.draw_circle(row, col)
                else:
                    self.draw_number(row, col, val)

    def draw_cross(self, row, col):
        start = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)
        end = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
        pygame.draw.line(self.screen, DARK_BLUE, start, end, CROSS_WIDTH)
        pygame.draw.line(self.screen, DARK_BLUE, (start[0], end[1]), (end[0], start[1]), CROSS_WIDTH)

    def draw_circle(self, row, col):
        center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(self.screen, BRIGHT_RED, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

    def draw_number(self, row, col, number):
        center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        text = self.number_font.render(number, True, MEDIUM_GRAY)
        self.screen.blit(text, text.get_rect(center=center))

    def draw_winning_line(self):
        if not self.winning_line or self.game_state != "game_over":
            return
        pygame.draw.line(self.screen, GREEN, *self.winning_line, 6)

    def draw_ui(self):
        ui_rect = pygame.Rect(0, WINDOW_SIZE, WINDOW_SIZE, 100)
        pygame.draw.rect(self.screen, CREAM, ui_rect)
        pygame.draw.line(self.screen, DARK_GRAY, (0, WINDOW_SIZE), (WINDOW_SIZE, WINDOW_SIZE), 2)

        if self.game_state == "mode_selection":
            text = "Select Game Mode: [0] vs Computer | [1] vs Player 2"
            color, font = BLUE_GRAY, self.font
        elif self.game_state == "playing":
            if self.computer_thinking:
                text, color, font = "Computer is thinking...", DARK_BLUE, self.big_font
            else:
                symbol = "X" if self.current_turn == "x" else "O"
                text = f"{self.current_player}'s turn ({symbol})"
                color, font = DARK_BLUE if symbol == "X" else BRIGHT_RED, self.font
        elif self.game_state == "game_over":
            if self.winner:
                text = f"{self.winner} WINS! Press R to restart"
                color, font = GREEN, self.big_font
            else:
                text, color, font = "DRAW! Press R to restart", GOLD, self.big_font

        surface = font.render(text, True, color)
        self.screen.blit(surface, surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE + 50)))

    def get_cell_from_click(self, pos):
        x, y = pos
        if y >= WINDOW_SIZE: return None, None
        return y // CELL_SIZE, x // CELL_SIZE

    def get_cell_from_number(self, number):
        if 1 <= number <= 9:
            number -= 1
            return number // 3, number % 3
        return None, None

    def is_valid_move(self, r, c):
        return self.board[r][c] not in ["x", "o"]

    def make_move(self, r, c):
        if self.is_valid_move(r, c):
            self.board[r][c] = self.current_turn
            return True
        return False

    def set_winning_line(self):
        for i in range(3):
            if all(self.board[i][j] == self.current_turn for j in range(3)):
                self.winning_line = ((0, i * CELL_SIZE + CELL_SIZE // 2), (WINDOW_SIZE, i * CELL_SIZE + CELL_SIZE // 2))
                return
            if all(self.board[j][i] == self.current_turn for j in range(3)):
                self.winning_line = ((i * CELL_SIZE + CELL_SIZE // 2, 0), (i * CELL_SIZE + CELL_SIZE // 2, WINDOW_SIZE))
                return
        if all(self.board[i][i] == self.current_turn for i in range(3)):
            self.winning_line = ((0, 0), (WINDOW_SIZE, WINDOW_SIZE))
        elif all(self.board[i][2 - i] == self.current_turn for i in range(3)):
            self.winning_line = ((WINDOW_SIZE, 0), (0, WINDOW_SIZE))

    def check_winner(self, board, symbol=None):
        player = symbol if symbol else self.current_turn

        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
            all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or \
        all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_board_full(self):
        return all(cell in ["x", "o"] for row in self.board for cell in row)

    def change_turn(self):
        self.current_turn = "o" if self.current_turn == "x" else "x"
        if self.player_mode == 0:
            self.current_player = "Computer" if self.current_player == "Player 1" else "Player 1"
        else:
            self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"

    def handle_move(self, r, c):
        if self.game_state != "playing" or self.computer_thinking:
            return
        if r is not None and c is not None and self.make_move(r, c):
            if self.check_winner(self.board):
                self.winner = self.current_player
                self.set_winning_line()
                self.game_over, self.game_state = True, "game_over"
            elif self.is_board_full():
                self.game_over, self.game_state = True, "game_over"
            else:
                self.change_turn()
                if self.player_mode == 0 and self.current_player == "Computer":
                    self.computer_move()

    def handle_click(self, pos):
        self.handle_move(*self.get_cell_from_click(pos))

    def handle_key(self, key):
        if self.game_state == "mode_selection":
            if key == pygame.K_0:
                self.player_mode = 0
                self.players = ["Player 1", "Computer"]
                self.current_player = "Player 1"
                self.game_state = "playing"
            elif key == pygame.K_1:
                self.player_mode = 1
                self.players = ["Player 1", "Player 2"]
                self.current_player = "Player 1"
                self.game_state = "playing"
        elif self.game_state == "playing" and key in number_keys:
            self.handle_move(*self.get_cell_from_number(number_keys[key]))
        elif self.game_state == "game_over" and key == pygame.K_r:
            self.reset_game()
            self.game_state = "mode_selection"

    def computer_move(self):
        self.computer = Computer(self)
        self.computer.start()

    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self.handle_click(e.pos)
                if e.type == pygame.KEYDOWN:
                    self.handle_key(e.key)

            if self.game_state == "mode_selection":
                self.draw_background()
            else:
                self.draw_grid()
                self.draw_marks()
                self.draw_winning_line()

            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    TicTacToe().run()
