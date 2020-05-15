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
    """
    Returns player who has the next turn on a board.
    """
    l_r = len(board)
    l_c = len(board[0])
    x_count = 0
    o_count = 0
    moves = []
    for i in range(l_r):
        for j in range(l_c):
            if board[i][j] == X:
                x_count+=1
            elif board[i][j] == O:
                o_count+=1
                
    if x_count == o_count:
        return X
    else:
        return O
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    l_r = len(board)
    l_c = len(board[0])
    moves = []
    for i in range(l_r):
        for j in range(l_c):
            if board[i][j] == EMPTY:
                moves.append((i,j))
                
    return set(moves)
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row,col = action
    board_copy = copy.deepcopy(board)
    if board_copy[row][col] == EMPTY:
        board_copy[row][col] = player(board_copy)
        return board_copy
    else:
        raise Exception("Invalid Move")
        

    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    row = len(board)
    col = len(board[0])
    #row
    for i in range(row):
        prev = ''
        flag = 0
        
        for j in range(col):
            if prev == '':
                prev = board[i][j]
                
            if not board[i][j] == prev:
                flag = 1
                break
                
        if flag == 0:
            return prev
        
        
    #col
    for j in range(col):
        prev = ''
        flag = 0
        
        for i in range(row):
            if prev == '':
                prev = board[i][j]
                
            if not board[i][j] == prev:
                flag = 1
                break
                
        if flag == 0:
            return prev
        
        
    #diag1
    prev = ''
    flag = 0
    for i in range(row):
        if prev == '':
                prev = board[i][i]
                
        if not board[i][i] == prev:
            flag = 1
            break
                
    if flag == 0:
        return prev
    
    
    #diag2
    prev = ''
    flag = 0
    for i in range(row-1,-1,-1):
        if prev == '':
                prev = board[i][i]
                
        if not board[i][i] == prev:
            flag = 1
            break
                
    if flag == 0:
        return prev
    
    return None
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    res = winner(board)
    row = len(board)
    col = len(board[0])
    if res == None:
        for i in range(row):
            for j in range(col):
                if board[i][j] == EMPTY:
                    return False
                
    return True
    
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res = winner(board)
    if res == X:
        return 1
    elif res == O:
        return -1
    return 0
    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    p = player(board)
    
    if p == X:
        return max_value(board,2)[1]
    else:
        return min_value(board,-2)[1]
    
    
    

def min_value(board,alpha):
    if terminal(board):
        return utility(board),None
    
    v = 2
    ac = None
    acs = actions(board)
    for a in acs:
        res_board = result(board,a)
        val = max_value(res_board,v)[0]
        v = min(v,val)
        if v == val:
            ac = a
            
        if v == -1:
            return v,ac
        
        if v <= alpha:
            return alpha-1,ac
        
    return v,ac

def max_value(board,alpha):
    if terminal(board):
        return utility(board),None
    
    v = -2
    ac = None
    acs = actions(board)
    for a in acs:
        res_board = result(board,a)
        val = min_value(res_board,v)[0]
        v = max(v,val)
        if v == val:
            ac = a
        
        if v == 1:
            return v,ac
        
        if v >= alpha:
            return alpha+1,ac
        
    return v,ac

    #raise NotImplementedError
