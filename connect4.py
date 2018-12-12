
import numpy as np
from collections import namedtuple
import random
from abc import ABC, abstractmethod
from math import log10
import chess

"""
CONNECT FOUR

Try functools.lru_cache for memoization. It's a decorator.

Make parser for PGN files.

Train model on PGN files to score board state. Use model in evaluation function.
    1 image (chess board) -> [0 through 1] (regression, one float that predicts chance of white winning by state)

"""

INF = float('inf')
NEG_INF = float('-inf')


class Agent(object):
    def __str__(self):
        return type(self).__name__ + "   "


    def __eq__(self, other):
        return type(self) is type(other)


    def __hash__(self):
        return hash(str(self))


    def do_move(self, move, board):
        board.push(move)


    def turn(self, board):
        """
        Given the current board, decide a move to make.
        """
        pass


class HumanAgent(Agent):
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
    def turn(self, board):
        """
        Prompt the user for a move, then return that move.
        """
        pass


class RandomAgent(AiAgent):
    def turn(self, board):
        """
        Based on the board state, pick a random legal move.
        """
        legal_moves = board.legal_moves()
        self.do_move(random.choice(list(legal_moves)), board)


class NegamaxAgent(AiAgent):
    def __init__(self, ply):
        self.ply = ply


    def __str__(self):
        return type(self).__name__ + f"({self.ply})"


    def __hash__(self):
        return hash(self.ply)


    def __eq__(self, other):
        return type(self) is type(other) and self.ply == other.ply


    def turn(self, board):
        """
        """
        score, move = self.negamax(board, self.ply, NEG_INF, INF)
        self.do_move(move, board)


    def negamax(self, board, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            if board.turn:
                return board.eval(), board.peek()
            return -board.eval(), board.peek()

        legal_moves = list(board.legal_moves())
#        random.shuffle(legal_moves)
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

class Game(ABC):
    def __init__(self):
        self.turn = True

    @abstractmethod
    def legal_moves(self):
        pass


    @abstractmethod
    def push(self):
        pass


    @abstractmethod
    def peek(self):
        pass


    @abstractmethod
    def pop(self):
        pass


    @abstractmethod
    def eval(self):
        pass


    @abstractmethod
    def is_game_over(self):
        pass


    @abstractmethod
    def is_draw(self):
        pass


    def play(self, first, second, console):
        turn = 0 
        while not self.is_game_over():
            turn += 1
            if console:
                print("TURN {}: X PLAYER".format(turn))
            first.turn(self)
            if console:
                print(self)
            if not self.is_game_over():
                turn += 1
                if console:
                    print("TURN {}: O PLAYER".format(turn))
                second.turn(self)
                if console:
                    print(self)
            else:
                break

        if console:
            print("Game over!")
    #        if board.is_contig_line():
    #            print("Contiguous line!")
    #        elif board.is_board_full():
    #            print("Game over due to full board! Tie.")


class ContigGame(Game):
    def __init__(self):
        Game.__init__(self)
        self.ROWS = 0
        self.COLS = 0
        self.CONTIG = 0
        self.array = None
        self.move_stack = []


    def __str__(self):
        s = ""
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.array[i,j] == 1:
                    s += "X "
                elif self.array[i,j] == -1:
                    s += "O "
                else:
                    s += ". "
            s += "\n"
        return s


    @abstractmethod
    def is_contig_line(self):
        pass


    def peek(self):
        if len(self.move_stack) == 0:
            raise IndexError("Attempted to peek empty stack!")
        return self.move_stack[-1]


    def is_game_over(self):
        if self.is_board_full() or self.is_contig_line():
            return True
        return False


    def is_board_full(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.array[row,col] == 0:
                    return False
        return True


    def eval(self):
        if self.is_game_over():
            if self.is_contig_line():
                if self.turn:
                    return NEG_INF
                return INF
        return 0


    def is_draw(self):
        if self.is_board_full() and not self.is_contig_line():
            return True
        return False


class TicTacToeBoard(ContigGame):
    def __init__(self):
        Board.__init__(self)
        self.ROWS = 3
        self.COLS = 3
        self.CONTIG = 3
        self.array = np.zeros((self.ROWS,self.COLS))


    def legal_moves(self):
        result = set()
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.array[row,col] == 0:
                    result.add((row,col))
        return result


    def push(self, coord):
        self.move_stack.append(coord)
        if self.turn:
            color = 1
        else:
            color = -1
        self.array[coord[0],coord[1]] = color
        self.turn = not self.turn


    def pop(self):
        if len(self.move_stack) == 0:
            raise IndexError("Attempted to pop empty stack!")
        last = self.move_stack[-1] #TODO does this cause issues? (not casting to int, for example?)
        del self.move_stack[-1]
        self.array[last[0], last[1]] = 0
        self.turn = not self.turn
        return last


    def is_contig_line(self):
        if len(self.move_stack) == 0:
            return False
        most_recent_row = self.peek()[0]
        most_recent_col = self.peek()[1]
        color = 1
        if self.turn:
            color = -1
        dirs = [(0,1),(1,0),(1,1),(-1,1)]
        for direction in dirs:
            contig = 1
            cur_i = int(most_recent_row) + direction[0]
            cur_j = int(most_recent_col) + direction[1]
            while contig < self.CONTIG and cur_i >= 0 and cur_i < self.ROWS and cur_j >=0 and cur_j < self.COLS and self.array[cur_i,cur_j] == color:
                contig += 1
                cur_i += direction[0]
                cur_j += direction[1]        
            cur_i = int(most_recent_row) - direction[0]
            cur_j = int(most_recent_col) - direction[1]
            while contig < self.CONTIG and cur_i >= 0 and cur_i < self.ROWS and cur_j >=0 and cur_j < self.COLS and self.array[cur_i,cur_j] == color:
                contig += 1
                cur_i -= direction[0]
                cur_j -= direction[1]        
            if contig >= self.CONTIG:
                return True 
        return False


class Connect4Board(ContigGame):
    def __init__(self):
        ContigGame.__init__(self)
        self.ROWS = 6
        self.COLS = 7
        self.CONTIG = 4
        self.array = np.zeros((self.ROWS,self.COLS))
        self.move_stack = []
#        self.legal_moves


    def __str__(self):
        s = ""
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.array[i,j] == 1:
                    s += "X "
                elif self.array[i,j] == -1:
                    s += "O "
                else:
                    s += ". "
            s += "\n"
        return s


    def legal_moves(self):
        result = set()
        for j in range(self.COLS):
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
        for i in range(self.ROWS):
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


    def pop(self):
        if len(self.move_stack) == 0:
            raise IndexError("Attempted to pop empty stack!")
        last = int(self.move_stack[-1])
        del self.move_stack[-1]
        self.array[self.top_full_row(last), last] = 0
        self.turn = not self.turn
        return last


    def is_contig_line(self):
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
            while contig < self.CONTIG and cur_i >= 0 and cur_i < self.ROWS and cur_j >=0 and cur_j < self.COLS and self.array[cur_i,cur_j] == color:
                contig += 1
                cur_i += direction[0]
                cur_j += direction[1]        
            cur_i = int(most_recent_row) - direction[0]
            cur_j = int(most_recent_col) - direction[1]
            while contig < self.CONTIG and cur_i >= 0 and cur_i < self.ROWS and cur_j >=0 and cur_j < self.COLS and self.array[cur_i,cur_j] == color:
                contig += 1
                cur_i -= direction[0]
                cur_j -= direction[1]        
            if contig >= self.CONTIG:
                return True 
        return False


class ChessBoard(Game):
    def __init__(self):
        Game.__init__(self)
        self.board = chess.Board()
        self.score_map = {1:100, 2:320, 3:330, 4:500, 5:900, 6:20000}


    def __str__(self):
        return str(self.board)


    def legal_moves(self):
        return self.board.legal_moves


    def peek(self):
        return self.board.peek()


    def push(self, move):
        self.turn = not self.turn
        self.board.push(move)


    def pop(self):
        self.turn = not self.turn
        return self.board.pop()
    
       
    def eval(self):
        white = 0 
        black = 0 
        if self.board.is_checkmate():
            if self.board.turn:
                return NEG_INF
            else:
                return INF 
        elif self.is_draw():
                return 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                if piece.color:
                    white += self.score_map[piece.piece_type]
                else:
                    black += self.score_map[piece.piece_type]
        return white - black


    def is_game_over(self):
        return self.board.is_game_over()


    def is_draw(self):
        return self.board.is_seventyfive_moves() or self.board.is_insufficient_material() or self.board.is_stalemate() or self.board.is_fivefold_repetition()


"""
board = Connect4Board()
print(board)
print(f"legal moves={board.legal_moves()}")
print(f"is 4 in a row? {board.is_contig_line()}")
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
print(f"is 4 in a row? {board.is_contig_line()}")
"""


def play_random_ai_game(game=TicTacToeBoard, console=True):
    board = game()
    p1 = RandomAgent(True)
    p2 = RandomAgent(False)
    play(board, p1, p2, console)
    return board


def duel_ais(p1, p2, n=1000, game=TicTacToeBoard, console=True):
    p1_wins = 0
    p2_wins = 0
    draws = 0
    for i in range(int(n/2)): 
        board = game()
        board.play(p1, p2, False)
        if board.is_draw():
            draws += 1
        elif board.turn:
            p2_wins += 1
        else:
            p1_wins += 1
    for i in range(int(n/2)):
        board = game()
        board.play(p2, p1, False)
        if board.is_draw():
            draws += 1
        elif board.turn:
            p1_wins += 1
        else:
            p2_wins += 1
    if console:
        print(f"{n} games played:")
        print(f"\tdraws: {draws}")
        print(f"\t{type(p1).__name__} P1 wins: {p1_wins}")
        print(f"\t{type(p2).__name__} P2 wins: {p2_wins}")
    return p2_wins / (p1_wins + p2_wins)


def confusion_matrix(ais,game=TicTacToeBoard,n=1000):
    ratios = {}
    pairs = set()
    print("\t\t", end="")
    for ai in ais:
        print(f"{ai}", end="\t")
    print("")
    for ai1 in ais:
        print(f"{ai1}", end="\t")
        for ai2 in ais:
            pair = (ai1,ai2)
            if pair not in pairs and (ai2,ai1) not in pairs:
                ratio = duel_ais(ai1,ai2,n,game,False)
                ratios[pair] = ratio
                pairs.add(pair)
                precision = int(log10(n))
                print(f"{ratio:.{int(log10(n))}}", end="\t\t") 
            else:
                print("\t\t", end="")
        print("")
    return ratios


#board = ChessBoard()
#board.play(NegamaxAgent(1), RandomAgent(), True)

#duel_ais(NegamaxAgent(2), RandomAgent(), 100, Connect4Board)

confusion_matrix([RandomAgent(), NegamaxAgent(1)], ChessBoard, 100)

