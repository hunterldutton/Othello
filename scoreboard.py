from board import BOARD
import pygame



class SCOREBOARD:
    def __init__(self, screen) -> None:
        self.white = 255, 255, 255
        self.black = 0, 0, 0
        self.screen = screen
        self.score_font = pygame.font.Font("assets/Hamletornot.ttf", 20)
        self.game_logo_font = pygame.font.Font("assets/Hamletornot.ttf", 40)
        self.othello_logo = self.game_logo_font.render("Othello", True, self.white)
        #Defines border image.
        self.game_border = pygame.image.load('assets/boarder.png')


    def update(self, white_count, black_count, whos_turn):
        #If statement for switching colors for the turn display.
        self.turn_display = self.game_logo_font.render(f"Turn:  {whos_turn}", 1, self.white)
        self.white_score = self.score_font.render("White Score : " + str(white_count), 1, self.white)
        self.black_score = self.score_font.render("Black Score : " + str(black_count), 1, self.white)
        self.screen.blit(self.white_score, (600, 75))
        self.screen.blit(self.black_score, (600, 125))
        self.screen.blit(self.othello_logo, (600, 10))
        self.screen.blit(self.turn_display, (150, 500))

        #Loads the border image for the board.
        self.screen.blit(self.game_border, (0, 0))




    # def show_score(self, screen):
    # screen.blit(self.text, (100, 100))
#
