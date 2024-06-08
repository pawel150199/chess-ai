import pygame
import sys
import os

from const import WIDTH, HEIGHT, ROWS, COLS, SQSIZE
from game import Game
from square import Square
from move import Move

from configuration import Config


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess game with AI')
        self.game = Game()
        self.game_started = False
        self.show_exit_menu = False

        # colors
        self.white = (255, 255, 255)
        self.green = (76, 153, 0)
        self.black = (0, 0, 0)
        self.gray = (100, 100, 100)
        self.lgray = (212, 217, 219)

        self.font = pygame.font.Font(None, 70)
        self.button_font = pygame.font.Font(None, 70)

        # Button dimensions
        self.button_width = 400
        self.button_height = 100
    
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

        img = pygame.transform.scale(pygame.image.load(texture), (250, 320))

        img_center = (400, 200)
        texture_rect = img.get_rect(center=img_center)
        surface.blit(img, texture_rect)
    
    def landing_menu(self):
        start_button_rect = pygame.Rect((WIDTH - self.button_width) // 2, HEIGHT // 2 + 25, self.button_width, self.button_height)
        exit_button_rect = pygame.Rect((WIDTH - self.button_width) // 2, HEIGHT // 2 + 150, self.button_width, self.button_height)

        while not self.game_started:
            self.screen.fill(self.lgray)
            self._draw_logo(self.screen)
            
            pygame.draw.rect(self.screen, self.gray, start_button_rect)
            pygame.draw.rect(self.screen, self.gray, exit_button_rect)
            
            self.draw_text('Start Game', self.button_font, self.black, self.screen, start_button_rect.centerx, start_button_rect.centery)
            self.draw_text('Exit', self.button_font, self.black, self.screen, exit_button_rect.centerx, exit_button_rect.centery)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        self.game_started = True
  
                    if exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()
    
    def end_menu(self):
        looping = True
        restart_button_rect = pygame.Rect((WIDTH - self.button_width) // 2, HEIGHT // 2 + 100, self.button_width, self.button_height)
        exit_button_rect = pygame.Rect((WIDTH - self.button_width) // 2, HEIGHT // 2 + 205, self.button_width, self.button_height)
        winner = self.game.next_player

        while looping:
            self.screen.fill(self.lgray)
            self._draw_logo(self.screen)
            self.draw_text(f'{winner.upper()} WON THE GAME', self.button_font, self.black, self.screen, self.screen.get_width() // 2, (self.screen.get_height() // 2) + 15)
            pygame.draw.rect(self.screen, self.gray, restart_button_rect)
            pygame.draw.rect(self.screen, self.gray, exit_button_rect)
                
            self.draw_text('Try Again', self.button_font, self.black, self.screen, restart_button_rect.centerx, restart_button_rect.centery)
            self.draw_text('Exit', self.button_font, self.black, self.screen, exit_button_rect.centerx, exit_button_rect.centery)

                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button_rect.collidepoint(event.pos):
                        looping = False

                    if exit_button_rect.collidepoint(event.pos):
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
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game.reset()
                        screen = self.screen
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
            
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
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)  

                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                

                    dragger.undrag_piece(dragger.piece)

                if board.checkmate:
                    self.end_menu()
                    game.reset()
                    screen = self.screen
                    game = self.game
                    board = self.game.board
                    dragger = self.game.dragger

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

