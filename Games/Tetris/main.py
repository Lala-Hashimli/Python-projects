import pygame
import random
import sys
from enum import Enum
from config import *


# Initialize Pygame
pygame.init()



class GameMode(Enum):
    MENU = 1
    SINGLE_PLAYER = 2
    TWO_PLAYER = 3

class Piece:
    def __init__(self, x, y, shape_index, player=1):
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.rotation = 0
        self.player = player
        if player == 1:
            self.color = PIECE_COLORS_P1[shape_index]
        else:
            self.color = PIECE_COLORS_P2[shape_index]
    
    def get_rotated_shape(self):
        return PIECES[self.shape_index][self.rotation % len(PIECES[self.shape_index])]
    
    def get_cells(self):
        shape = self.get_rotated_shape()
        cells = []
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    cells.append((self.x + j, self.y + i))
        return cells

class TetrisBoard:
    def __init__(self, x_offset=0, player=1):
        self.board = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  
        self.x_offset = x_offset
        self.game_over = False
        self.player = player
        self.spawn_new_piece()
    
    def spawn_new_piece(self):
        if self.next_piece is None:
            self.next_piece = Piece(BOARD_WIDTH // 2 - 2, 0, random.randint(0, len(PIECES) - 1), self.player)
        
        self.current_piece = self.next_piece
        self.next_piece = Piece(BOARD_WIDTH // 2 - 2, 0, random.randint(0, len(PIECES) - 1), self.player)
        
        # Check if game over
        if self.is_collision(self.current_piece):
            self.game_over = True
    
    def is_collision(self, piece, dx=0, dy=0, rotation=0):
        test_piece = Piece(piece.x + dx, piece.y + dy, piece.shape_index, piece.player)
        test_piece.rotation = (piece.rotation + rotation) % len(PIECES[piece.shape_index])
        
        for x, y in test_piece.get_cells():
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                return True
            if y >= 0 and self.board[y][x] != BLACK:
                return True
        return False
    
    def place_piece(self):
        for x, y in self.current_piece.get_cells():
            if y >= 0:
                self.board[y][x] = self.current_piece.color
        
        # Clear completed lines
        lines_to_clear = []
        for y in range(BOARD_HEIGHT):
            if all(self.board[y][x] != BLACK for x in range(BOARD_WIDTH)):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [BLACK for _ in range(BOARD_WIDTH)])
        
        # Update score and level
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            self.score += len(lines_to_clear) * 100 * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
        
        self.spawn_new_piece()
    
    def move_piece(self, dx, dy):
        if self.current_piece and not self.is_collision(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False
    
    def rotate_piece(self):
        if self.current_piece and not self.is_collision(self.current_piece, rotation=1):
            self.current_piece.rotation += 1
    
    def drop_piece(self):
        if self.current_piece:
            while not self.is_collision(self.current_piece, 0, 1):
                self.current_piece.y += 1
    
    def update(self, dt):
        if self.game_over or not self.current_piece:
            return
        
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            if not self.move_piece(0, 1):
                self.place_piece()
            self.fall_time = 0
    
    def draw(self, screen):
        # Draw board background
        board_rect = pygame.Rect(
            self.x_offset + BOARD_MARGIN,
            BOARD_MARGIN,
            BOARD_WIDTH * CELL_SIZE,
            BOARD_HEIGHT * CELL_SIZE
        )
        pygame.draw.rect(screen, DARK_GRAY, board_rect)
        
        # Draw grid lines for better visibility
        for x in range(BOARD_WIDTH + 1):
            pygame.draw.line(screen, (80, 80, 80), 
                           (self.x_offset + BOARD_MARGIN + x * CELL_SIZE, BOARD_MARGIN),
                           (self.x_offset + BOARD_MARGIN + x * CELL_SIZE, BOARD_MARGIN + BOARD_HEIGHT * CELL_SIZE))
        for y in range(BOARD_HEIGHT + 1):
            pygame.draw.line(screen, (80, 80, 80),
                           (self.x_offset + BOARD_MARGIN, BOARD_MARGIN + y * CELL_SIZE),
                           (self.x_offset + BOARD_MARGIN + BOARD_WIDTH * CELL_SIZE, BOARD_MARGIN + y * CELL_SIZE))
        
        # Draw placed pieces
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x] != BLACK:
                    cell_rect = pygame.Rect(
                        self.x_offset + BOARD_MARGIN + x * CELL_SIZE,
                        BOARD_MARGIN + y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    pygame.draw.rect(screen, self.board[y][x], cell_rect)
                    pygame.draw.rect(screen, WHITE, cell_rect, 1)
        
        # Draw current piece
        if self.current_piece:
            for x, y in self.current_piece.get_cells():
                if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
                    cell_rect = pygame.Rect(
                        self.x_offset + BOARD_MARGIN + x * CELL_SIZE,
                        BOARD_MARGIN + y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    pygame.draw.rect(screen, self.current_piece.color, cell_rect)
                    pygame.draw.rect(screen, WHITE, cell_rect, 1)
        
        # Draw board border
        pygame.draw.rect(screen, WHITE, board_rect, 2)
        
        # Draw next piece preview (adjusted position for two-player mode)
        if self.next_piece:
            if self.player == 1:
                next_x = self.x_offset + BOARD_MARGIN + BOARD_WIDTH * CELL_SIZE + 10
            else:
                next_x = self.x_offset + BOARD_MARGIN + BOARD_WIDTH * CELL_SIZE + 10
            next_y = BOARD_MARGIN + 50
            
            # Draw background for next piece
            preview_bg = pygame.Rect(next_x - 5, next_y - 35, 120, 100)
            pygame.draw.rect(screen, (30, 30, 30), preview_bg)
            pygame.draw.rect(screen, WHITE, preview_bg, 1)
            
            font = pygame.font.Font(None, SMALL_FONT_SIZE)
            text = font.render("Next:", True, WHITE)
            screen.blit(text, (next_x, next_y - 30))
            
            shape = self.next_piece.get_rotated_shape()
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell == '#':
                        cell_rect = pygame.Rect(
                            next_x + j * (CELL_SIZE // 2),
                            next_y + i * (CELL_SIZE // 2),
                            CELL_SIZE // 2,
                            CELL_SIZE // 2
                        )
                        pygame.draw.rect(screen, self.next_piece.color, cell_rect)
                        pygame.draw.rect(screen, WHITE, cell_rect, 1)
        
        # Draw score and level (adjusted position for two-player mode)
        font = pygame.font.Font(None, SMALL_FONT_SIZE)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        lines_text = font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        
        if self.player == 1:
            info_x = self.x_offset + BOARD_MARGIN + BOARD_WIDTH * CELL_SIZE + 10
        else:
            info_x = self.x_offset + BOARD_MARGIN + BOARD_WIDTH * CELL_SIZE + 10
        info_y = BOARD_MARGIN + 170
        
        # Draw background for info
        info_bg = pygame.Rect(info_x - 5, info_y - 10, 120, 90)
        pygame.draw.rect(screen, (30, 30, 30), info_bg)
        pygame.draw.rect(screen, WHITE, info_bg, 1)
        
        screen.blit(score_text, (info_x, info_y))
        screen.blit(level_text, (info_x, info_y + 25))
        screen.blit(lines_text, (info_x, info_y + 50))
        
        # Draw game over message
        if self.game_over:
            font = pygame.font.Font(None, FONT_SIZE)
            game_over_text = font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(
                self.x_offset + BOARD_MARGIN + BOARD_WIDTH * CELL_SIZE // 2,
                BOARD_MARGIN + BOARD_HEIGHT * CELL_SIZE // 2
            ))
            # Draw background for game over text
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, RED, bg_rect, 2)
            screen.blit(game_over_text, text_rect)

class TetrisGame:
    def __init__(self):
        self.screen_width = 900
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Colorful Tetris - Single & Two Player")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.big_font = pygame.font.Font(None, 48)
        self.mode = GameMode.MENU
        self.board1 = None
        self.board2 = None
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        # Title
        title = self.big_font.render("COLORFUL TETRIS", True, CYAN)
        title_rect = title.get_rect(center=(self.screen_width // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Menu options
        single_text = self.font.render("1 - Single Player (WASD)", True, WHITE)
        two_text = self.font.render("2 - Two Player (WASD + Arrow Keys)", True, WHITE)
        quit_text = self.font.render("Q - Quit", True, WHITE)
        
        single_rect = single_text.get_rect(center=(self.screen_width // 2, 300))
        two_rect = two_text.get_rect(center=(self.screen_width // 2, 350))
        quit_rect = quit_text.get_rect(center=(self.screen_width // 2, 400))
        
        self.screen.blit(single_text, single_rect)
        self.screen.blit(two_text, two_rect)
        self.screen.blit(quit_text, quit_rect)
        
        # Instructions
        instructions = [
            "Single Player Controls:",
            "W - Rotate, A - Left, S - Down, D - Right, Space - Drop",
            "",
            "Two Player Controls:",
            "Player 1: W,A,S,D + Space",
            "Player 2: ↑,←,↓,→ + Enter"
        ]
        
        y = 480
        for instruction in instructions:
            if instruction:
                text = pygame.font.Font(None, 18).render(instruction, True, LIGHT_BLUE)
                text_rect = text.get_rect(center=(self.screen_width // 2, y))
                self.screen.blit(text, text_rect)
            y += 20
    
    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.mode = GameMode.SINGLE_PLAYER
                self.board1 = TetrisBoard(x_offset=(self.screen_width - BOARD_WIDTH * CELL_SIZE - 2 * BOARD_MARGIN) // 2, player=1)
            elif event.key == pygame.K_2:
                self.mode = GameMode.TWO_PLAYER
                self.board1 = TetrisBoard(x_offset=20, player=1)
                self.board2 = TetrisBoard(x_offset=450, player=2)
            elif event.key == pygame.K_q:
                sys.exit()
        return True
    
    def handle_game_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mode = GameMode.MENU
                self.board1 = None
                self.board2 = None
                return
            
            # Player 1 controls (WASD + Space)
            if self.board1 and not self.board1.game_over:
                if event.key == pygame.K_a:
                    self.board1.move_piece(-1, 0)
                elif event.key == pygame.K_d:
                    self.board1.move_piece(1, 0)
                elif event.key == pygame.K_s:
                    self.board1.move_piece(0, 1)
                elif event.key == pygame.K_w:
                    self.board1.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    self.board1.drop_piece()
            
            # Player 2 controls (Arrow keys + Enter)
            if self.board2 and not self.board2.game_over:
                if event.key == pygame.K_LEFT:
                    self.board2.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.board2.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.board2.move_piece(0, 1)
                elif event.key == pygame.K_UP:
                    self.board2.rotate_piece()
                elif event.key == pygame.K_RETURN:
                    self.board2.drop_piece()
    
    def draw_game(self):
        self.screen.fill(BLACK)
        
        if self.board1:
            self.board1.draw(self.screen)
            
            # Player 1 label
            player1_text = pygame.font.Font(None, 20).render("Player 1", True, CYAN)
            self.screen.blit(player1_text, (self.board1.x_offset + BOARD_MARGIN, 10))
        
        if self.board2:
            self.board2.draw(self.screen)
            
            # Player 2 label
            player2_text = pygame.font.Font(None, 20).render("Player 2", True, PINK)
            self.screen.blit(player2_text, (self.board2.x_offset + BOARD_MARGIN, 10))
        
        # ESC instruction
        esc_text = pygame.font.Font(None, 16).render("ESC - Back to Menu", True, WHITE)
        self.screen.blit(esc_text, (10, self.screen_height - 25))
    
    def run(self):
        running = True
        dt = 0
        
        while running:
            dt = self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.mode == GameMode.MENU:
                    running = self.handle_menu_input(event)
                else:
                    self.handle_game_input(event)
            
            # Update game state
            if self.mode != GameMode.MENU:
                if self.board1:
                    self.board1.update(dt)
                if self.board2:
                    self.board2.update(dt)
            
            # Draw
            if self.mode == GameMode.MENU:
                self.draw_menu()
            else:
                self.draw_game()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()