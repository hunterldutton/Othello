import copy
WIDTH = 8
HEIGHT = 8
DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0,), (-1, -1), (0, -1), (1, -1)]


class Node:
    def __init__(self, board, current_player, is_maximizing_player, last_move=None):
        self.board = board.copy()  # the current state of the board
        self.last_move = last_move  # the move that led to this state
        self.player = current_player
        self.is_maximizing_player = is_maximizing_player

    def evaluate_board(self):
        """
        Evaluate the current board position for the given player.

        Arguments:
        - board: a 2D array representing the current board position.
        - maximizing_player: a boolean indicating which player is currently maximizing their score.

        Returns:
        - The score for the given player, based on the board position.
        """
        score = 0
        # Board Control: count the number of pieces on the board for each player.
        player_counts = [0, 0]  # player[0] for White and player[1] for Black
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'W':
                    player_counts[0] += 1
                elif self.board[i][j] == 'B':
                    player_counts[1] += 1
        if self.is_maximizing_player:
            score += player_counts[0] - player_counts[1]
        else:
            score += player_counts[1] - player_counts[0]

        # Mobility: count the number of legal moves available to each player.
        mobility = [0, 0] # mobility[0] for White and mobility[1] for Black
        legal_moves = self.get_valid_moves()
        if len(legal_moves)>0:
            if self.is_maximizing_player:
                mobility[0] += len(legal_moves)
            else:
                mobility[1] += len(legal_moves)
        if mobility[0] + mobility[1] != 0:
            mobility_score = (mobility[0] - mobility[1]) / (mobility[0] + mobility[1])
            score += mobility_score

        # Corner Control: count the number of corners controlled by each player.
        corner_control = [0, 0] # corner_control[0] for White and corner_control[1] for Black
        for i, j in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            if self.board[i][j] == 'W':
                corner_control[0] += 1
            elif self.board[i][j] == 'B':
                corner_control[1] += 1
        if self.is_maximizing_player:
            score += 5 * (corner_control[0] - corner_control[1])
        else:
            score += 5 * (corner_control[1] - corner_control[0])

        return score

    def is_terminal(self):
        if len(self.get_valid_moves()) == 0:
            return True
        else:
            return False

    def get_last_move(self):
        return self.last_move

    def get_valid_moves(self):
        valid_moves = []
        if self.player == 'B':
            opponent_color = 'W'
        else:
            opponent_color = 'B'

        for i in range(WIDTH):
            for j in range(HEIGHT):
                if self.board[i][j] == '.':
                    valid_tile = False
                    for direction in DIRECTIONS:
                        seen_opponent_color = False
                        x = i
                        y = j
                        while x + direction[0] >= 0 and x + direction[0] < WIDTH and y + direction[1] >= 0 and y + \
                                direction[1] < HEIGHT and not valid_tile:
                            x += direction[0]
                            y += direction[1]
                            if self.board[x][y] == '.':
                                break
                            elif self.board[x][y] == opponent_color:
                                seen_opponent_color = True
                            elif self.board[x][y] == self.player:
                                if seen_opponent_color:
                                    valid_tile = True
                                break
                    if valid_tile:
                        valid_moves.append((i,j))

        return valid_moves

    def change_over(self, move, new_board):

        i = move[0]
        j = move[1]
        pieces_to_flip = []
        player_color = self.player

        if player_color == 'B':
            opponent_color = 'W'
            new_board[i][j] = 'B'
        else:
            opponent_color = 'B'
            new_board[i][j] = 'W'

        valid_tile = False
        for direction in DIRECTIONS:
            seen_opponent_color = False
            x = i
            y = j
            while x + direction[0] >= 0 and x + direction[0] < WIDTH and y + direction[1] >= 0 and y + direction[
                1] < HEIGHT and not valid_tile:
                x += direction[0]
                y += direction[1]
                if new_board[x][y] == None:
                    break
                elif new_board[x][y] == opponent_color:
                    seen_opponent_color = True
                elif new_board[x][y] == player_color:
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

        if player_color == 'W':
            new_board[i][j] = 'W'
        else:
            new_board[i][j] = 'B'


    def get_children(self):
        children = []
        for move in self.get_valid_moves():
            new_board = copy.deepcopy(self.board)
            self.change_over(move, new_board)

            if self.player == 'W':
                child_node = Node(new_board, 'B', not self.is_maximizing_player, move)
            else:
                child_node = Node(new_board, 'W', not self.is_maximizing_player, move)
            children.append(child_node)
        return children

