"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flat_board = [pos for row in board for pos in row]

    return X if flat_board.count(X) <= flat_board.count(O) else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for r_i, row in enumerate(board):
        for c_i, cell in enumerate(row):
            if cell is EMPTY:
                moves.add((r_i, c_i))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] not in [0, 1, 2] or action[1] not in [0, 1, 2]:
        raise IndexError("out-of-bounds move")
    if board[action[0]][action[1]]:
        raise NameError("Already chosen")

    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for row in board:
        if len(set(row)) == 1 and list(set(row))[0] in [X, O]:
            return list(set(row))[0]

    for col in zip(*board):
        if len(set(col)) == 1 and list(set(col))[0] in [X, O]:
            return list(set(col))[0]

    left_diagonal = [board[0][0], board[1][1], board[2][2]]
    if len(set(left_diagonal)) == 1:
        return list(set(left_diagonal))[0]

    rigt_diagonal = [board[0][2], board[1][1], board[2][0]]
    if len(set(rigt_diagonal)) == 1:
        return list(set(rigt_diagonal))[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not actions(board):
        return True

    return True if winner(board) else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if "O" == winner(board):
        return -1
    elif "X" == winner(board):
        return 1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        """
        Returns the best value achievable from board assuming the player to move will try to maximize the score.
        """
        if terminal(board):
            return utility(board)

        value = -math.inf
        for action in actions(board):
            value = max(value, min_value(result(board, action)))
            if value == 1:
                return 1
        return value

    def min_value(board):
        """
        Returns the best value achievable from board assuming the player to move will try to minimize the score.
        """
        if terminal(board):
            return utility(board)

        value = math.inf
        for action in actions(board):
            value = min(value, max_value(result(board, action)))
            if value == -1:
                return -1
        return value

    best_action = None
    if terminal(board):
        return best_action

    current = player(board)

    if current == X:
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
                if best_value == 1:
                    break
    else:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
                if best_value == -1:
                    break

    return best_action
