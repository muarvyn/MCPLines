import numpy as np
from functools import reduce

def getVacationsIterator(board):
    return zip(*np.nonzero(np.array(board) == 0))

orig_dirs = [(-1,0),(-1,-1),(0,-1),(1,-1)]
SingleDim = 4
MIN_LINE_SIZE = 4
MIN_LINE_SIZE_M1 = MIN_LINE_SIZE - 1
isInRange = lambda loc: np.all(np.array(loc)>=0) and np.all(np.array(loc)<SingleDim)

def isStraitConnection(board, location, player):
    connection = []
    for shift in orig_dirs:
        line = []

        loc = location
        while True:
            loc = (loc[0]+shift[0], loc[1]+shift[1])
            if not isInRange(loc) or board[loc] != player: break
            line.append(loc)

        loc = location
        while True:
            loc = (loc[0]-shift[0], loc[1]-shift[1])
            if not isInRange(loc) or board[loc] != player: break
            line.append(loc)

        if len(line) >= MIN_LINE_SIZE_M1:
            return True

    return False

def getLocationsOf(board, mark):
    return zip(*np.nonzero(np.array(board) == mark))

# Early draw detection
board_shape = (SingleDim,SingleDim)
dir_inc = np.array([[0,1],[1,1],[1,0],[1,-1]])
# bit set of winning configurations a board cell is part of, built for each board cell
bit_sets = np.zeros(shape=board_shape, dtype=int)
bit = 0 # codes a distinct winning configuration
for row,col in np.ndindex(board_shape):
    for row_inc,col_inc in dir_inc:
        end = (row+row_inc*MIN_LINE_SIZE_M1, col+col_inc*MIN_LINE_SIZE_M1)
        if not end in np.ndindex(board_shape):
            continue
        for i in range(MIN_LINE_SIZE):
            bit_sets[row+row_inc*i, col+col_inc*i] |= 1<<bit
        bit += 1
        
complete_bit_set = reduce(lambda a,b: a|b, [bit_sets[x] for x in np.ndindex(board_shape)])

def isDraw(board):
    return \
        reduce(lambda a,b: a|b, [bit_sets[x] for x in getLocationsOf(board,2)]) == complete_bit_set \
        and reduce(lambda a,b: a|b, [bit_sets[x] for x in getLocationsOf(board,1)]) == complete_bit_set
