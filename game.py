import board
from board import BOARD
from node import Node
from scoreboard import SCOREBOARD
import pygame
from enum import Enum
from pygame import mixer

GREEN = (17, 190, 27)

States = Enum('States', ['P1Choosing', 'P2Choosing'])

AI_WAIT_TIME = 300  # Time for the AI to wait before making a move, in milliseconds


class GAME:
    def __init__(self, screen, vs_ai=False) -> None:
        self.board = BOARD(GREEN, screen, vs_ai)
        self.screen = screen
        self.vs_ai = vs_ai
        self.scoreboard = SCOREBOARD(screen)
        self.sprites = pygame.sprite.Group()
        self.piece_sound = mixer.Sound("assets/sounds/piece_placement.wav")
        self.sprites.add(self.board)
        self.winner = None
        self.last = 0
        self.state = States.P1Choosing
        self.whos_turn_display = "Black"

        # Stuff for the piece count.

    """
    update()
    
    Turn logic for Othello. 
    
    
    """

    def update(self):
        highlights = self.board.get_highlights()
        # For the turn the display.
        if self.state == States.P1Choosing:
            self.whos_turn_display = "Black"
        else:
            self.whos_turn_display = "White"
        if not self.vs_ai:
            self.sprites.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    for i in range(self.board.width):
                        for j in range(self.board.height):
                            if (highlights[i][j].rect.collidepoint(position) and highlights[i][j].active):
                                self.piece_sound.play()
                                # Blacks turn.
                                if self.state == States.P1Choosing:
                                    self.board.add_piece(i, j, "black")
                                    highlights[i][j].active = False
                                    self.board.highlight_valid_tiles("white")
                                    self.state = States.P2Choosing
                                    self.board.change_over(i, j, "black")

                                    if not self.board.white_has_moves:
                                        self.board.highlight_valid_tiles("black")
                                        self.state = States.P1Choosing
                                # Whites turn
                                else:
                                    self.board.add_piece(i, j, "white")
                                    highlights[i][j].active = False
                                    self.board.highlight_valid_tiles("black")
                                    self.state = States.P1Choosing
                                    self.board.change_over(i, j, "white")

                                    if not self.board.black_has_moves:
                                        self.board.highlight_valid_tiles("white")
                                        self.state = States.P2Choosing
                                self.board.get_piece_count()
                                # Check if no one can move, then check who wins.
                                if not self.board.black_has_moves and not self.board.white_has_moves:
                                    self.set_winner(self.board.check_gameover())
                                    return True


        else:
            self.sprites.draw(self.screen)
            if self.state == States.P1Choosing:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        position = pygame.mouse.get_pos()
                        for i in range(self.board.width):
                            for j in range(self.board.height):
                                if highlights[i][j].rect.collidepoint(position) and highlights[i][j].active:
                                    self.piece_sound.play()
                                    # Blacks turn.
                                    self.board.add_piece(i, j, "black")
                                    highlights[i][j].active = False
                                    self.board.change_over(i, j, "black", False)
                                    # self.board.highlight_valid_tiles("white")
                                    self.state = States.P2Choosing
                                    self.last = pygame.time.get_ticks()

                                    if not self.board.white_has_moves:
                                        self.board.highlight_valid_tiles("black")
                                        self.state = States.P1Choosing

                                    self.board.get_piece_count()
                                    # Check if no one can move, then check who wins.
                                    if not self.board.black_has_moves and not self.board.white_has_moves:
                                        self.set_winner(self.board.check_gameover())
                                        return True

            else:
                if self.state == States.P2Choosing:
                    now = pygame.time.get_ticks()
                    if now - self.last >= AI_WAIT_TIME:
                        # Whites turn
                        node = Node(self.board.board, 'W', True)
                        _, move = self.board.minimax(node, depth=6, alpha=float('inf'), beta=float('-inf'),
                                                     is_maximizingPlayer=True)
                        if move:
                            i = move[0]
                            j = move[1]
                            self.piece_sound.play()
                            self.board.add_piece(i, j, "white")
                            self.board.change_over(i, j, "white")
                            highlights[i][j].active = False
                            self.board.white_has_moves = True
                        else:
                            self.board.white_has_moves = False
                        self.board.highlight_valid_tiles("black")
                        self.state = States.P1Choosing

                        self.board.get_piece_count()
                        # Check if no one can move, then check who wins.
                        if not self.board.black_has_moves and not self.board.white_has_moves:
                            self.set_winner(self.board.check_gameover())
                            return True

                        if not self.board.black_has_moves:
                            self.board.highlight_valid_tiles("white")
                            self.state = States.P2Choosing

        self.sprites.update()
        self.scoreboard.update(self.board.white_count, self.board.black_count, self.whos_turn_display)

    def keep_scoreboard(self):
        self.scoreboard.update(self.board.white_count, self.board.black_count, self.whos_turn_display)

    def set_winner(self, winner):
        self.winner = winner

    def get_winner(self):
        return self.winner
