import pygame
import sys

class StartScreen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Set up display
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Chess Game")

        # Define colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (100, 100, 100)

        # Define fonts
        self.font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 50)

        # Button positions
        self.start_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 - 50, 200, 50)
        self.exit_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 50, 200, 50)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, textrect)

    def landing_menu(self):
        while True:
            self.screen.fill(self.white)
            
            self.draw_text('Chess Game', self.font, self.black, self.screen, self.screen_width // 2, self.screen_height // 4)
            
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
                        pygame.quit()
                        return True
                        # Here you would start your chess game
                    if self.exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()


if __name__ == "__main__":
    start_screen = StartScreen()
    start_screen.main_menu()