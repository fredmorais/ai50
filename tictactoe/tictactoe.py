"""
Tic Tac Toe Player
"""

import math
import copy

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
    Xs = 0
    Os = 0

    for row in board:
        for place in row:
            if place == X:
                Xs += 1
            elif place == O:
                Os += 1
    
    if Xs > Os:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i, row in enumerate(board):
        for j, place in enumerate(row):
            if place == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("this move is not allowed")

    # Make deep copy
    newBoard = copy.deepcopy(board)

    # Get next player and update on board
    newBoard[action[0]][action[1]] = player(board)

    return newBoard


def winner(board):
    winnerX = [X, X, X]
    winnerO = [O, O, O]
    
    boardColumns = [list(t) for t in zip(*board)]
    diagonals = [
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]    
    ]

    if winnerX in [*board, *boardColumns, *diagonals]:
        return X
    if winnerO in [*board, *boardColumns, *diagonals]:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If there is winner or the board is full
    if winner(board) != None or not any(EMPTY in x for x in board):
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    utility = 0

    if winner(board) == X:
        utility = 1
    elif winner(board) == O:
        utility = -1
    
    return utility


def max_value(board):
    if terminal(board):
        return (utility(board))

    v = float('-inf')

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return (utility(board))

    v = float('inf')

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    next = player(board)

    acts = []
    utils = []

    for ac in actions(board):
        if next == X:
            utils.append(min_value(result(board, ac)))
        elif next == O:
            utils.append(max_value(result(board, ac)))
        acts.append(ac)

    if next == X:
        return acts[utils.index(max(utils))]
    elif next == O:
        return acts[utils.index(min(utils))]
