import pygame
number_keys = {
                pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
                pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6,
                pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9
            }

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 3
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
LINE_WIDTH = 4
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 8
CROSS_WIDTH = 8
SPACE = CELL_SIZE // 4

# colors
LIGHT_GRAY = (240, 240, 240)      
CREAM = (248, 248, 248)           
DARK_BLUE = (31, 78, 121)         
BRIGHT_RED = (230, 57, 70)          
DARK_GRAY = (51, 51, 51)          
GREEN = (46, 204, 113)            
GOLD = (241, 196, 15)             
MEDIUM_GRAY = (85, 85, 85)        
BLUE_GRAY = (52, 73, 94)          
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)