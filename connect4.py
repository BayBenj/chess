
import numpy as np
from collections import namedtuple

"""
CONNECT FOUR

Try functools.lru_cache for memoization. It's a decorator.

"""


Coord = namedtuple("Coord", ["i","j"])


class Board():
    def __init__(self):
        self.array = np.zeros((6,7))
        self.move_stack = []
#        self.legal_moves
        self.turn = True


    def __str__(self):
        s = ""
        for i in range(6):
            for j in range(7):
                s += str(self.array[i,j]) + " "
            s += "\n"
        return s


    def legal_moves(self):
        result = set()
        for j in range(7):
            for i in range(6):
                if i == 0 and self.array[i,j] != 0:
                    break
                if i == 5 or (self.array[i,j] != 0 and i > 0):
                    result.add(j)
                    break
        return result
                 

    def top_empty_row(self, col):
        for i in list(range(5,-1,-1)):
            if self.array[i,col] == 0:
                return i
        return None


    def top_full_row(self, col):
        for i in range(6):
            if self.array[i,col] != 0:
                return i
        return None


    def push(self, col, color):
        if self.top_empty_row(col) is None:
            raise ValueError("Cannot add to a full column!")
        self.move_stack.append(col)
        self.array[self.top_empty_row(col),col] = color


    def peek(self):
        return self.move_stack[-1]


    def pop(self):
        last = self.move_stack[-1]
        del self.move_stack[-1]
        return last


    def is_game_over(self):
        if self.is_board_full() or is_4_in_row():
            return True
        return False


    def is_4_in_row(self):
        if len(self.move_stack) == 0:
            return False
        most_recent_col = self.peek()
        most_recent_row = self.top_full_row(most_recent_col)
        color = self.array[most_recent_row,most_recent_col]
        dirs = [(0,1),(1,0),(1,1),(-1,1)]
        for dir in dirs:
            sum = 0
            cur_i = most_recent_row
            cur_j = most_recent_col
            while cur_i >= 0 and cur_i < 6 and cur_j >=0 and cur_j < 7 and self.array[cur_i,cur_j] == color:
                sum += 1
                cur_i += dir[0]
                cur_j += dir[1]        
            cur_i = most_recent_row
            cur_j = most_recent_col
            while cur_i >= 0 and cur_i < 6 and cur_j >=0 and cur_j < 7 and self.array[cur_i,cur_j] == color:
                sum += 1
                cur_i -= dir[0]
                cur_j -= dir[1]        
            if sum >= 4:
                return True 
        return False


    def is_board_full(self):
        for i in range(6):
            for j in range(7):
                if self.array[i][j] == 0:
                    return False
        return True
       

board = Board()
print(board)
print(f"legal moves={board.legal_moves()}")
print(f"is 4 in a row? {board.is_4_in_row()}")
board.push(3,1) 
board.push(3,1) 
board.push(3,1) 
board.push(3,-1) 
board.push(3,1) 
board.push(3,1) 
board.push(2,1) 
board.push(1,1) 
board.push(4,1) 
print(board)
print(f"legal moves={board.legal_moves()}")
print(f"is board full? {board.is_board_full()}")
print(f"is 4 in a row? {board.is_4_in_row()}")
