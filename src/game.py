import pygame
from board import Board
from dragger import Dragger

from const import WIDTH, HEIGHT, ROWS, COLS, SQSIZE, GREEN, WHITE


class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
    
    def show_backgroud(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = GREEN
                else:
                    color = WHITE
                
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE  + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)
    
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            print(piece.moves)
            for move in piece.moves:
                color = '#C86464' if (move.final_square.row + move.final_square.col) % 2 == 0 else '#C84646'
                rect = (move.final_square.col * SQSIZE, move.final_square.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)