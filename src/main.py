import pygame
import sys
import os

from const import WIDTH, HEIGHT, ROWS, COLS, SQSIZE
from game import Game
from square import Square
from move import Move
from exception import CheckmateException

from configuration import Config


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess game with AI')
        self.game = Game()
        self.game_started = False
        self.game_checkmate = False

        # colors
        self.white = (255, 255, 255)
        self.green = (76, 153, 0)
        self.black = (0, 0, 0)
        self.gray = (100, 100, 100)
        self.lgray = (212, 217, 219)

        self.font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 60)

        # Button dimensions
        self.button_width = 400
        self.button_height = 100

        # Button positions
        self.start_button_rect = pygame.Rect((WIDTH - self.button_width) // 2, HEIGHT // 2 + 25, self.button_width, self.button_height)
        self.exit_button_rect = pygame.Rect((WIDTH - self.button_width) // 2, HEIGHT // 2 + 150, self.button_width, self.button_height)
    
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, textrect)

    def _draw_logo(self, surface):
        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.dirname(current_directory)

        texture = os.path.join(
            f'{parent_directory}/assets/chess.png'
        )

        img = pygame.transform.scale(pygame.image.load(texture), (250, 350))

        img_center = (400, 200)
        texture_rect = img.get_rect(center=img_center)
        surface.blit(img, texture_rect)
    
    def landing_menu(self):
        while not self.game_started:
            self.screen.fill(self.lgray)
            self._draw_logo(self.screen)
            
            pygame.draw.rect(self.screen, self.gray, self.start_button_rect)
            pygame.draw.rect(self.screen, self.gray, self.exit_button_rect)
            
            self.draw_text('Start Game', self.button_font, self.black, self.screen, self.start_button_rect.centerx, self.start_button_rect.centery)
            self.draw_text('Exit', self.button_font, self.black, self.screen, self.exit_button_rect.centerx, self.exit_button_rect.centery)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(event.pos):
                        print("Start Game clicked")
                        self.game_started = True

  
                    if self.exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()
    
    def end_menu(self):
        while self.game_checkmate == True:
            self.screen.fill(self.lgray)
            self._draw_logo(self.screen)
            self.draw_text('MAT - GAME OVER', self.button_font, self.black, self.screen, self.screen.get_width() // 2, self.screen.get_height() // 2)
            pygame.draw.rect(self.screen, self.gray, self.exit_button_rect)
                
            self.draw_text('Exit', self.button_font, self.black, self.screen, self.exit_button_rect.centerx, self.exit_button_rect.centery)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                
            pygame.display.update()

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        if  not self.game_started:
            self.landing_menu()

        while self.game_started:
            try:
                game.show_background(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():

                    # mouse click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)

                                # show methods on screen
                                game.show_background(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)

                
                    # mouse movement
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            # show methods on screen
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            dragger.update_blit(screen)

                    # mouse release button
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX //SQSIZE

                            # create possible move
                            initial_square  = Square(dragger.initial_row, dragger.initial_col)
                            final_square  = Square(released_row, released_col)
                            move = Move(initial_square, final_square)
                            
                            # check if it is valid move
                            if board.valid_move(dragger.piece, move):
                                # print("valid move")
                                captured = board.squares[released_row][released_col].has_piece()
                                board.move(dragger.piece, move)

                                board.set_true_en_passant(dragger.piece)  

                                game.show_background(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                # next turn
                                game.next_turn()

                        dragger.undrag_piece(dragger.piece)

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
            except CheckmateException:
                self.game_started = False
                self.game_checkmate = True
        if self.game_checkmate == True:
            self.game_started = True
            self.end_menu()

