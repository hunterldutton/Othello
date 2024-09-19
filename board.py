from piece import PIECE
from highlight import HIGHLIGHT
from node import Node
import pygame


DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0,), (-1, -1), (0, -1), (1, -1)]

WIDTH = 8
HEIGHT = 8
TILE_SIZE = 50

GRID_MARGIN_X = 50
GRID_MARGIN_Y = 50

BLACK = (1, 1, 1)
GREEN = (17, 190, 27)


class BOARD(pygame.sprite.Sprite):
    def __init__(self, color, screen, vs_ai) -> None:
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.width = WIDTH
        self.height = HEIGHT
        self.vs_ai = vs_ai
        # Stays true as long as black/white has available highlights.
        self.black_has_moves = True
        self.white_has_moves = True

        self.screen = screen

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.

        self.image = pygame.Surface([self.width * TILE_SIZE + 2 * GRID_MARGIN_X,
                                     self.height * TILE_SIZE + 2 * GRID_MARGIN_Y])
        self.image.fill(color)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                rect = pygame.Rect(GRID_MARGIN_X + TILE_SIZE * x, GRID_MARGIN_Y + \
                                   TILE_SIZE * y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.image, BLACK, rect, 1)

            # Fetch the rectangle object that has the dimensions of the image
            # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

        self.piece_sprites = pygame.sprite.Group()
        self.highlight_sprites = pygame.sprite.Group()
        self.pieces = []
        self.highlights = []
        for i in range(WIDTH):
            self.pieces.append([])
            self.highlights.append([])
            for j in range(HEIGHT):
                self.pieces[i].append(None)
                self.highlights[i].append(None)
        # Count for black and white
        self.black_count = 0
        self.white_count = 0

        # Count for total pieces.
        self.piece_count = 0

        # Create starting pieces
        self.add_piece(3, 3, "white")
        self.add_piece(3, 4, "black")
        self.add_piece(4, 3, "black")
        self.add_piece(4, 4, "white")

        if self.vs_ai:
            self.valid_moves = []
            self.board = []
            for x in range(WIDTH):
                self.board.append([])
                for y in range(HEIGHT):
                    self.board[x].append('.')
            self.board[3][3] = 'W'
            self.board[3][4] = 'B'
            self.board[4][3] = 'B'
            self.board[4][4] = 'W'

        # Load border for the boardgame from the boarder.png in assets.

        # Create highlights
        for i in range(WIDTH):
            for j in range(HEIGHT):
                new_highlight = HIGHLIGHT(GRID_MARGIN_X + TILE_SIZE / 2 + i * TILE_SIZE,
                                          GRID_MARGIN_Y + TILE_SIZE / 2 + j * TILE_SIZE)
                self.highlights[i][j] = new_highlight
        self.highlight_valid_tiles("black")



    def generate_children(self, player):

        self.highlight_valid_tiles(player)
        for move in self.valid_moves:
            new_board = self.board.copy()
            new_board.make_move(player, move)
            child_node = Node(new_board, move)
            self.children.append(child_node)

    # Define the minimax pruning function
    def minimax(self, node: Node, depth, alpha, beta, is_maximizingPlayer):
        if depth == 0 or node.is_terminal():
            return node.evaluate_board(), None

        if is_maximizingPlayer:
            value = float('-inf')
            best_move = None
            for child in node.get_children():
                child_value, _ = self.minimax(child, depth - 1, alpha, beta, False)
                if child_value > value:
                    value = child_value
                    best_move = child.get_last_move()
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # beta cut-off
            return value, best_move
        else:
            value = float('inf')
            best_move = None
            for child in node.get_children():
                child_value, _ = self.minimax(child, depth - 1, alpha, beta, True)
                if child_value < value:
                    value = child_value
                    best_move = child.get_last_move()
                beta = min(beta, value)
                if beta <= alpha:
                    break  # alpha cut-off
            return value, best_move

    """
    add_piece():
    
    Called to add a new piece to the board. 
    
    """

    def add_piece(self, i, j, color):
        new_piece = PIECE(GRID_MARGIN_X + TILE_SIZE / 2 + i * TILE_SIZE, GRID_MARGIN_Y + TILE_SIZE / 2 + j * TILE_SIZE,
                          color)
        self.pieces[i][j] = new_piece
        self.piece_sprites.add(new_piece)


    """
    update_board():
    Helper function for update()
    
    Called everytime the board should be displayed. 
    
    """

    def update_board(self):
        self.image.fill(GREEN)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                rect = pygame.Rect(GRID_MARGIN_X + TILE_SIZE * x, GRID_MARGIN_Y + \
                                   TILE_SIZE * y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.image, BLACK, rect, 1)

    """
    update_pieces()
    
    Called everytime pieces are added to the board 
    
    """

    def update_pieces(self):
        self.piece_sprites = pygame.sprite.Group()
        for j in range(HEIGHT):
            for i in range(WIDTH):
                if self.pieces[i][j]:
                    self.piece_sprites.add(self.pieces[i][j])

    """
    update():
    
    Called after changes are made to the board pieces/highlights. 
    
    """

    def update(self):
        self.update_board()
        self.update_pieces()
        self.piece_sprites.draw(self.image)
        self.piece_sprites.update()
        self.highlight_sprites.draw(self.image)
        self.highlight_sprites.update()

    """
    highlight_valid_tiles()
    
    Called in the change_over() function to update the valid tiles for every turn. 
    
    """

    def highlight_valid_tiles(self, whose_turn):
        self.highlight_sprites.empty()
        player_color = whose_turn
        if whose_turn == "black":
            opponent_color = "white"
        else:
            opponent_color = "black"
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if self.pieces[i][j] == None:
                    self.highlights[i][j].active = False
                    valid_tile = False
                    for direction in DIRECTIONS:
                        seen_opponent_color = False
                        x = i
                        y = j
                        while x + direction[0] >= 0 and x + direction[0] < WIDTH and y + direction[1] >= 0 and y + \
                                direction[1] < HEIGHT and not valid_tile:
                            x += direction[0]
                            y += direction[1]
                            if self.pieces[x][y] == None:
                                break
                            elif self.pieces[x][y].color_name == opponent_color:
                                seen_opponent_color = True
                            elif self.pieces[x][y].color_name == player_color:
                                if seen_opponent_color:
                                    valid_tile = True
                                break
                    if valid_tile:
                        self.highlight_sprites.add(self.highlights[i][j])
                        self.highlights[i][j].active = True
                        if self.vs_ai:
                            self.valid_moves.append((i,j))

        # Returns false if no highlights were found/ no available turns.
        if len(self.highlight_sprites) == 0:
            if whose_turn == "black":
                self.black_has_moves = False
            else:
                self.white_has_moves = False
        else:
            if whose_turn == "black":
                self.black_has_moves = True
            else:
                self.white_has_moves = True
    """
    change_over(i, j, whoseturn)
    
    i: the x value of the new piece places on the board.
    j: the y value of the new piece placed on the board.
    
    whose_turn: the color/turn of the new piece placed on the board
    
    Logic for switching pieces between the same color after a piece is placed. 
    
    """

    def change_over(self, i, j, whose_turn, do_highlights=True):
        pieces_to_flip = []
        player_color = whose_turn

        if whose_turn == "black":
            opponent_color = "white"
            if self.vs_ai:
                self.board[i][j] = 'B'
        else:
            opponent_color = "black"
            if self.vs_ai:
                self.board[i][j] = 'W'

        valid_tile = False
        for direction in DIRECTIONS:
            seen_opponent_color = False
            x = i
            y = j
            while x + direction[0] >= 0 and x + direction[0] < WIDTH and y + direction[1] >= 0 and y + direction[
                1] < HEIGHT and not valid_tile:
                x += direction[0]
                y += direction[1]
                if self.pieces[x][y] == None:
                    break
                elif self.pieces[x][y].color_name == opponent_color:
                    seen_opponent_color = True
                elif self.pieces[x][y].color_name == player_color:
                    if seen_opponent_color:
                        while True:
                            x -= direction[0]
                            y -= direction[1]
                            if x == i and y == j:
                                break
                            pieces_to_flip.append([x, y])
                    break

        for piece in pieces_to_flip:
            i = piece[0]
            j = piece[1]
            new_piece = PIECE(GRID_MARGIN_X + TILE_SIZE / 2 + i * TILE_SIZE,
                              GRID_MARGIN_Y + TILE_SIZE / 2 + j * TILE_SIZE, player_color)
            self.pieces[i][j] = new_piece
            self.pieces[i][j].color_name = player_color

            if self.vs_ai:
                if player_color == "white":
                    self.board[i][j] = 'W'
                else:
                    self.board[i][j] = 'B'

            self.highlights[i][j].active = False

        if do_highlights:
            self.highlight_valid_tiles(opponent_color)
        else:
            self.highlight_sprites.empty()

    """
    get_highlights():
    
    Getter function for highlights. 
    
    """

    def get_highlights(self):
        return self.highlights


    """
    get_piece_count(self):
    
    Goes through the piece list and counts how many whites and blacks are currently on the board. 
    
    """
    def get_piece_count(self):
        self.white_count = 0
        self.black_count = 0
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if self.pieces[i][j] is not None:
                    piece = self.pieces[i][j]
                    if piece.color_name == "white":
                        self.white_count += 1
                    if piece.color_name == "black":
                        self.black_count += 1
        self.piece_count = self.white_count + self.black_count

    """
    check_gameover()
    
    Checks who wins. 
    
    """

    def check_gameover(self):
        if self.black_count > self.white_count:
            return "Black"
        if self.black_count < self.white_count:
            return "White"
        if self.black_count == self.white_count:
                return "Tie"

    """
    fill_board()
    
    Test function for game_over conditions. 
    
    """

    def fill_board(self):
        for i in range(WIDTH):
            for j in range(HEIGHT):
                self.add_piece(i, j, "black")
