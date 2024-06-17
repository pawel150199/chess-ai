import pygame
from ai import AutonomyPlayer
from board import Board
from dragger import Dragger
from configuration import Config

from const import WIDTH, HEIGHT, ROWS, COLS, SQSIZE, GREEN, WHITE


class Game:
    def __init__(self):
        self.ai = AutonomyPlayer()
        self.next_player = 'white'
        self.hovered_sqr = None
        self.select_piece = None
        self.gamemode = 'pvp'
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        self.ai = AutonomyPlayer()

    def set_engine(self, engine):
        self.ai.set_engine(engine)

    def show_background(self, surface):
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
            for move in piece.moves:
                color = '#C86464' if (move.final_square.row + move.final_square.col) % 2 == 0 else '#C84646'
                rect = (move.final_square.col * SQSIZE, move.final_square.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial_square = self.board.last_move.initial_square
            final_square = self.board.last_move.final_square

            for pos in [initial_square, final_square]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def select_piece(self, piece):
        self.selected_piece = piece

    def unselect_piece(self):
        self.selected_piece = None

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'


    def reset(self):
        self.__init__()
