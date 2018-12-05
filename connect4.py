
import numpy as np

"""
CONNECT FOUR

Try functools.lru_cache for memoization. It's a decorator.

"""

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


    def push(self, value):
        self.move_stack.append(value)


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
        return False


    def is_board_full(self):
        for i in range(6):
            for j in range(7):
                if self.array[i][j] == 0:
                    return False
        return True
       

board = Board()
print(board) 
