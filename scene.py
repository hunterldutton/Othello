import pygame
from game import GAME
from enum import Enum

# Initialize RGB variables
BLACK = (1, 1, 1)
WHITE = (255, 255, 255)
BUTTON = BLACK
BUTTON_HOVER = (50, 205, 50)

# Initialize dimension variables
BUTTON_PADDING = 10
WIDTH = 800
HEIGHT = 600

# Initialize enumerated SceneType
SceneType = Enum('SceneType', ['Super', 'Title', 'Game', 'Game_Over'])

# SCENE():
# Scene superclass
# Takes in "screen" variable at initialization,
# holds next scene variable,
# and enumerated type of Scene active
class SCENE():
    def __init__(self, screen) -> None:
        self.next = self
        self.screen = screen
        self.type = SceneType.Super

    def switch_scenes(self, next_scene):
        self.next = next_scene

    def get_scene_type(self):
        if self.type == SceneType.Title:
            return "Title"
        elif self.type == SceneType.Game:
            return "Game"
        elif self.type == SceneType.Game_Over:
            return "Game_Over"

# STARTSCENE():
# Subclass of SCENE()
# Loads start screen,
# takes user input to switch to next scene
# (GAMESCENE())
# OR to quit the program
class STARTSCENE(SCENE):
    def __init__(self, screen) -> None:
        SCENE.__init__(self, screen)
        self.type = SceneType.Title
    def process_input(self, events):
        running = True
        self.mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect.collidepoint(self.ai_button_back, self.mouse):
                    self.switch_scenes(GAMESCENE(self.screen, ai=True))
                elif pygame.Rect.collidepoint(self.human_button_back, self.mouse):
                    self.switch_scenes(GAMESCENE(self.screen, ai=False))
                elif pygame.Rect.collidepoint(self.quit_button_back, self.mouse):
                    running = False
        return running

    def update(self):
        pass
    def render(self, screen):
        screen.fill(BLACK)
        self.mouse = pygame.mouse.get_pos()
        self.button_font = pygame.font.Font("assets/Hamletornot.ttf", 40)
        self.logo_font = pygame.font.Font("assets/Hamletornot.ttf", 70)
        self.othello_logo = self.logo_font.render("Othello", True, WHITE)
        self.v_ai_button = self.button_font.render("Human vs. AI", True, WHITE)
        self.ai_button_back = pygame.Rect(290 - BUTTON_PADDING, 260 - BUTTON_PADDING // 2,
                                          self.v_ai_button.get_width() + BUTTON_PADDING * 2, self.v_ai_button.get_height() + BUTTON_PADDING)
        self.v_human_button = self.button_font.render("Human vs. Human", True, WHITE)
        self.human_button_back = pygame.Rect(255 - BUTTON_PADDING, 333 - BUTTON_PADDING // 2,
                                          self.v_human_button.get_width() + BUTTON_PADDING * 2,
                                          self.v_human_button.get_height() + BUTTON_PADDING)
        self.quit_button = self.button_font.render("Quit", True, WHITE)
        self.quit_button_back = pygame.Rect(360 - BUTTON_PADDING, 400,
                                          self.quit_button.get_width() + BUTTON_PADDING * 2,
                                          self.quit_button.get_height() + BUTTON_PADDING // 2)
        self.screen.blit(self.othello_logo, (290, 125))
        if (pygame.Rect.collidepoint(self.ai_button_back, self.mouse)):
            pygame.draw.rect(screen, BUTTON_HOVER, self.ai_button_back)
        else:
            pygame.draw.rect(screen, BUTTON, self.ai_button_back)
        self.screen.blit(self.v_ai_button, (290, 260))
        if (pygame.Rect.collidepoint(self.human_button_back, self.mouse)):
            pygame.draw.rect(screen, BUTTON_HOVER, self.human_button_back)
        else:
            pygame.draw.rect(screen, BUTTON, self.human_button_back)
        self.screen.blit(self.v_human_button, (255, 330))
        if (pygame.Rect.collidepoint(self.quit_button_back, self.mouse)):
            pygame.draw.rect(screen, BUTTON_HOVER, self.quit_button_back)
        else:
            pygame.draw.rect(screen, BUTTON, self.quit_button_back)
        self.screen.blit(self.quit_button, (360, 400))

# GAMESCENE():
# Subclass of SCENE()
# Has a GAME object that is called
# To play Othello
class GAMESCENE(SCENE):
    def __init__(self, screen, ai):
        SCENE.__init__(self, screen)
        self.next = self
        self.ai = ai
        self.type = SceneType.Game
        self.game = GAME(self.screen, self.ai)
        self.gameover = False

    def render(self):
        self.screen.fill(BLACK)
        gameover = self.game.update()
        if (gameover):
            self.switch_scenes(GAMEOVERSCENE(self.screen, self.game, self.ai))

# GAMEOVERSCENE():
# Adds Play Again, Main Menu,
# and Quit buttons to the Board.
# Awaits input and performs action based on input
class GAMEOVERSCENE(SCENE):
    def __init__(self, screen, game, ai):
        SCENE.__init__(self, screen)
        self.ai = ai
        self.next = self
        self.type = SceneType.Game_Over
        self.game = game

    def process_input(self, events):
        running = True
        self.mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (pygame.Rect.collidepoint(self.again_button_back, self.mouse)):
                    self.switch_scenes(GAMESCENE(self.screen, self.ai))
                    ## TODO: Call AI vs Human OR Human vs Human based on previous game
                    self.switch_scenes(GAMESCENE(self.screen, self.ai))
                elif (pygame.Rect.collidepoint(self.menu_button_back, self.mouse)):
                    self.switch_scenes(STARTSCENE(self.screen))
                elif (pygame.Rect.collidepoint(self.quit_button_back, self.mouse)):
                    running = False
        return running
    def render(self, screen):
        self.mouse = pygame.mouse.get_pos()
        self.gameover_font = pygame.font.Font("assets/Hamletornot.ttf", 40)
        self.gameover_text = self.gameover_font.render("Game Over!", True, WHITE)
        if (self.game.get_winner() == "Black"):
            self.winner_text = self.gameover_font.render("Black Wins!", True, WHITE)
        elif (self.game.get_winner() == "White"):
            self.winner_text = self.gameover_font.render("White Wins!", True, WHITE)
        elif (self.game.get_winner() == "Tie"):
            self.winner_text = self.gameover_font.render("Tie!", True, WHITE)
        self.play_again_button = self.gameover_font.render("Play Again", True, WHITE)
        self.main_menu_button = self.gameover_font.render("Main Menu", True, WHITE)
        self.quit_button = self.gameover_font.render("Quit", True, WHITE)
        self.again_button_back = pygame.Rect(570 - BUTTON_PADDING, 315 - BUTTON_PADDING // 2,
                                          self.play_again_button.get_width() + BUTTON_PADDING * 2,
                                          self.play_again_button.get_height() + BUTTON_PADDING)
        self.menu_button_back = pygame.Rect(568 - BUTTON_PADDING, 390 - BUTTON_PADDING // 2,
                                             self.main_menu_button.get_width() + BUTTON_PADDING * 2,
                                             self.main_menu_button.get_height() + BUTTON_PADDING)
        self.quit_button_back = pygame.Rect(620 - BUTTON_PADDING, 455,
                                            self.quit_button.get_width() + BUTTON_PADDING * 2,
                                            self.quit_button.get_height() + BUTTON_PADDING // 2)
        self.screen.blit(self.gameover_text, (565, 175))
        self.screen.blit(self.winner_text, (565, 225))
        if (pygame.Rect.collidepoint(self.again_button_back, self.mouse)):
            pygame.draw.rect(screen, BUTTON_HOVER, self.again_button_back)
        else:
            pygame.draw.rect(screen, BUTTON, self.again_button_back)
        self.screen.blit(self.play_again_button, (570, 310))
        if (pygame.Rect.collidepoint(self.menu_button_back, self.mouse)):
            pygame.draw.rect(screen, BUTTON_HOVER, self.menu_button_back)
        else:
            pygame.draw.rect(screen, BUTTON, self.menu_button_back)
        self.screen.blit(self.main_menu_button, (570, 380))
        if (pygame.Rect.collidepoint(self.quit_button_back, self.mouse)):
            pygame.draw.rect(screen, BUTTON_HOVER, self.quit_button_back)
        else:
            pygame.draw.rect(screen, BUTTON, self.quit_button_back)
        self.screen.blit(self.quit_button, (620, 450))
        self.game.update()
        self.game.keep_scoreboard()

