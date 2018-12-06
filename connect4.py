
import numpy as np
from collections import namedtuple
import random

"""
CONNECT FOUR

Try functools.lru_cache for memoization. It's a decorator.

"""

INF = float('inf')
NEG_INF = float('-inf')


class Agent(object):
    def __init__(self, color):
        self.color = color #True == white, False = black


    def do_move(self, move, board):
        board.push(move)

    def turn(self, board):
        """
        Given the current board, decide a move to make.
        """
        pass


class HumanAgent(Agent):
    def __init__(self, n):
        Agent.__init__(self, n)


    def turn(self, board):
        """
        Prompt the user for a move, then return that move.
        """
        print("Player move: ", end="")
        col = 99
        while move not in board.legal_moves():
            col = str(int(input()))
        self.do_move(col)


class AiAgent(Agent):
    def __init__(self, n):
        Agent.__init__(self, n)


    def turn(self, board):
        """
        Prompt the user for a move, then return that move.
        """
        pass


class RandomAgent(AiAgent):
    def __init__(self, n):
        AiAgent.__init__(self, n)


    def turn(self, board):
        """
        Based on the board state, pick a random legal move.
        """
        legal_moves = board.legal_moves()
        self.do_move(random.choice(list(legal_moves)), board)


class MinMaxAgent(AiAgent):
    def __init__(self, n, ply):
        AiAgent.__init__(self, n)
        self.ply = ply

    def turn(self, board):
        """
        """
        score, move = self.negamax(board, self.ply, NEG_INF, INF)
        self.do_move(move, board)

    def negamax(self, board, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            if board.turn:
                return -board.eval(), board.peek()
            return board.eval(), board.peek()

        legal_moves = list(board.legal_moves())
        random.shuffle(legal_moves)
        value = NEG_INF
        best_moves = []
        for move in legal_moves:
            self.do_move(move, board)
            new_value = max(value, -self.negamax(board, depth - 1, -beta, -alpha)[0])
            board.pop()
            if new_value > value:
                best_moves = [move]
            else:
                best_moves.append(move) #TODO: is this right?
            value = new_value
            alpha = max(alpha, value)
            if alpha >= beta:
                break #(* cut-off *)
        return value, random.choice(best_moves)


class Board():
    ROWS = 6
    COLS = 7
    CONTIG = 4
    
    def __init__(self):
        self.array = np.zeros((ROWS,COLS))
        self.move_stack = []
#        self.legal_moves
        self.turn = True


    def __str__(self):
        s = ""
        for i in range(ROWS):
            for j in range(COLS):
                if self.array[i,j] == 1:
                    s += "X "
                elif self.array[i,j] == -1:
                    s += "O "
                else:
                    s += ". "
            s += "\n"
        return s


    def eval(self):
        if self.is_game_over():
            if self.is_4_in_row():
#                if self.turn:
#                    return NEG_INF
                return INF
        return 0


    def legal_moves(self):
        result = set()
        for j in range(COLS):
            row = self.top_empty_row(j)
            if row is not None:
                result.add(j)
        return result
                 

    def top_empty_row(self, col):
        for i in list(range(5,-1,-1)):
            if self.array[i,col] == 0:
                return i
        return None


    def top_full_row(self, col):
        for i in range(ROWS):
            if self.array[i,col] != 0:
                return i
        return None


    def push(self, col):
        if self.top_empty_row(col) is None:
            raise ValueError("Cannot add to a full column!")
        self.move_stack.append(col)

        if self.turn:
            color = 1
        else:
            color = -1
        self.array[self.top_empty_row(col),col] = color
        self.turn = not self.turn


    def peek(self):
        if len(self.move_stack) == 0:
            raise IndexError("Attempted to peek empty stack!")
        return self.move_stack[-1]


    def pop(self):
        if len(self.move_stack) == 0:
            raise IndexError("Attempted to pop empty stack!")
        last = int(self.move_stack[-1])
        del self.move_stack[-1]
        self.array[self.top_full_row(last), last] = 0
        self.turn = not self.turn
        return last


    def is_game_over(self):
        if self.is_board_full() or self.is_4_in_row():
            return True
        return False


    def is_4_in_row(self):
        if len(self.move_stack) == 0:
            return False
        most_recent_col = self.peek()
        most_recent_row = self.top_full_row(most_recent_col)
        color = 1
        if self.turn:
            color = -1
        dirs = [(0,1),(1,0),(1,1),(-1,1)]
        for direction in dirs:
            contig = 1
            cur_i = int(most_recent_row) + direction[0]
            cur_j = int(most_recent_col) + direction[1]
            while contig < CONTIG and cur_i >= 0 and cur_i < ROWS and cur_j >=0 and cur_j < COLS and self.array[cur_i,cur_j] == color:
                contig += 1
                cur_i += direction[0]
                cur_j += direction[1]        
            cur_i = int(most_recent_row) - direction[0]
            cur_j = int(most_recent_col) - direction[1]
            while contig < CONTIG and cur_i >= 0 and cur_i < ROWS and cur_j >=0 and cur_j < COLS and self.array[cur_i,cur_j] == color:
                contig += 1
                cur_i -= direction[0]
                cur_j -= direction[1]        
            if contig >= CONTIG:
                return True 
        return False


    def is_board_full(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.array[i][j] == 0:
                    return False
        return True
       
"""
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
"""


def play_game(board, p1, p2, console):
    turn = 0 
    while not board.is_game_over():
        turn += 1
        if console:
            print("TURN {}: X PLAYER".format(turn))
        p1.turn(board)
        if console:
            print(board)
        if not board.is_game_over():
            turn += 1
            if console:
                print("TURN {}: O PLAYER".format(turn))
            p2.turn(board)
            if console:
                print(board)
        else:
            break

    if console:
        if board.is_4_in_row():
            print("Four in a row!")
        elif board.is_board_full():
            print("Game over due to full board! Tie.")


def play_rand_ai_game(console=True):
    board = Board()
    p1 = MinMaxAgent(True, 8)
    p2 = RandomAgent(False)
    play_game(board, p1, p2, console)
    return board

play_rand_ai_game()

