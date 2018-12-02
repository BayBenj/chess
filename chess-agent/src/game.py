
import chess
from random import randint
import sys
from collections import namedtuple


ScoreMove = namedtuple("ScoreMove", ["score","move"])


def rand_elem(l):
    size = len(l)
    r = randint(0,size-1)
    return l[r]


def rand_elem_count(l):
    size = l.count()
    r = randint(0,size-1)
    i = 0
    for o in l:
        if i == r:
            return o
        i += 1


def max_with_tup(num, tup):
    return max(num,tup.score)


def min_with_tup(num, tup):
    return min(num,tup.score)


class Agent(object):
    def __init__(self, color):
        self.color = color #True == white, False = black


    def do_move(self, move, board):
        # Check for move validity if human
        board.push_san(board.san(move))

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
        i = input()
        if i == "p":
            print("Turn passed")
            return
        i = str(i)
        j = int(input())
        k = int(input())
        l = int(input())
        if board[i][j].owner == player:
            if Coord(k,l) in board.board[i][j].get_possible_moves():
                self.board.movement(Movement(i,j,k,l))
                self.board.print()
            else:
                print("Move not allowed!")
        else:
            print("You do not own that piece!")

  
class AiAgent(Agent):
    def __init__(self, n):
        Agent.__init__(self, n)


    def turn(self, board):
        """
        Prompt the user for a move, then return that move.
        """
        pass


class RandomAiAgent(AiAgent):
    def __init__(self, n):
        AiAgent.__init__(self, n)


    def turn(self, board):
        """
        Based on the board state, pick a random legal move.
        """
        legal_moves = board.legal_moves
        n = legal_moves.count()
        r = randint(0,n-1)
        for i, legal_move in enumerate(legal_moves):
            if i == r:
                self.do_move(legal_move, board)
                return


SCORE_MAP = {1:1, 2:3, 3:3, 4:5, 5:9, 6:100}


class MinMaxAgent(AiAgent):
    def __init__(self, n, ply):
        AiAgent.__init__(self, n)
        self.ply = ply

    def turn(self, board):
        """
        """
        #_, move = self.recurse_minimax2(board, 2, self.color)
        score, move = self.alpha_beta_max(board, float('-inf'), float('inf'), 2)
        self.do_move(move, board)


    def maxi(depth):
        if depth == 0:
            return eval_board(board, SCORE_MAP)
        max_score = float('-inf')
        for move in board.legal_moves:
            score = self.mini(board, depth - 1)
            if score > max_score:
                max_score = score
        return max_score


    def mini(self, board, depth):
        if depth == 0:
            return -eval_board(board, SCORE_MAP)
        min_score = float('inf');
        for move in board.legal_moves:
            score = self.maxi(board, depth - 1)
            if score < min_score:
                min_score = score
        return min_score


    def alpha_beta_max(self, board, alpha, beta, depth):
        if depth == 0:
            return eval_board(board, SCORE_MAP), board.peek()
        best_moves = []
        for move in board.legal_moves:
            self.do_move(move, board)
            score, _ = self.alpha_beta_min(board, alpha, beta, depth - 1)
            board.pop()
            if score >= beta:
                return beta, move     #fail hard beta-cutoff
            if score > alpha:
                alpha = score   #alpha acts like max in MiniMax
                best_moves = [move]
            elif score == alpha:
                best_moves.append(move)
        if len(best_moves) == 0:
            return alpha, rand_elem_count(board.legal_moves)
        return alpha, rand_elem(best_moves)


    def alpha_beta_min(self, board, alpha, beta, depth):
        if depth == 0:
            return -1 * eval_board(board, SCORE_MAP), board.peek()
        best_moves = []
        for move in board.legal_moves:
            self.do_move(move, board)
            score, _ = self.alpha_beta_max(board, alpha, beta, depth - 1)
            board.pop()
            if score <= alpha:
                return alpha, move     #fail hard alpha-cutoff
            if score < beta:
                beta = score     #beta acts like max in MiniMax
                best_move = [move]
            elif score == beta:
                best_moves.append(move)
        if len(best_moves) == 0:
            return beta, rand_elem_count(board.legal_moves)
        return beta, rand_elem(best_moves)


    def recurse_minimax2(self, board, depth, is_maxer, alpha, beta):
        if depth == 0:
            return eval_board(board, SCORE_MAP), board.peek()
        legal_moves = board.legal_moves
        best_move = None
        for i, move in enumerate(legal_moves):
            self.do_move(move, board)
            new_score, _ = self.recurse_minimax2(board, depth - 1, not is_maxer)
            board.pop()
            if is_maxer:
#                best_score = -9_999
                if new_score >= beta:
                    return beta
                    best_move = move
                    best_score = new_score
                elif new_score == best_score:
                    r = randint(0,1)
                    if r == 0:
                        best_move = move
                return alpha
            else:
#                best_score = 9_999
                if new_score < best_score:
                    best_move = move
                    best_score = new_score
                elif new_score == best_score:
                    r = randint(0,1)
                    if r == 0:
                        best_move = move
                return beta
#        return best_score, best_move


    def recurse_minimax(self, board, lvl):
        legal_moves = board.legal_moves
        maximize = self.color

        if lvl == self.ply:
            my_moves = []
            my_scores = []
            # all my possible moves
            for legal_move in legal_moves:
                self.do_move(legal_move, board)
                opp_scores = []
                opp_moves = []
                # all opponent's possible moves
                for opp_legal_move in board.legal_moves:
                    self.do_move(opp_legal_move, board)
                    opp_score = eval_board(board, SCORE_MAP)
                    opp_scores.append(opp_score)
                    opp_moves.append(board.pop())
                my_moves.append(board.pop())
                optimize = max
                if maximize:
                    optimize = min
                my_scores.append(optimize(opp_scores))
            optimize = min
            if maximize:
                optimize = max
            optimum = optimize(my_scores)
            opt_inds = [i for i, x in enumerate(my_scores) if x == optimum]
            opt_moves = []
            for ind in opt_inds:
                opt_moves.append(my_moves[ind])
            return rand_elem(opt_moves)
        else:
            my_moves = []
            my_scores = []
            # all my possible moves
            for legal_move in legal_moves:
                self.do_move(legal_move, board)
                opp_scores = []
                opp_moves = []
                # all opponent's possible moves
                for opp_legal_move in board.legal_moves:
                    self.do_move(opp_legal_move, board)
                    self.recurse_minimax(board, lvl + 1)



def eval_board(board, score_map):
    white = 0
    black = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color:
                white += score_map[piece.piece_type]
            else:
                black += score_map[piece.piece_type]
    return white - black


def print_state(board):
    print("-" * 16)
#    print("a b c d e f g h")
    print(board)
    print("board score: {}".format(eval_board(board, SCORE_MAP)))
    print("")
    
 
def play_game(board, p1, p2, console):
    turn = 0
    while not board.is_game_over():
        turn += 1
        if console:
            print("TURN {}: WHITE".format(turn))
        p1.turn(board)
        if console:
            print_state(board)
        if not board.is_game_over():
            turn += 1
            if console:
                print("TURN {}: BLACK".format(turn))
            p2.turn(board)
            if console:
                print_state(board)
        else:
            break

    if console:
        if board.is_seventyfive_moves():
            print("Game over due to 75 move rule!")
        elif board.is_insufficient_material():
            print("Game over due to insufficient material!")
        elif board.is_stalemate():
            print("Stalemate!")
        elif board.is_checkmate():
            print("Checkmate!")
        elif board.is_fivefold_repetition():
            print("Game over due to fivefold repetition!")
        else:
            print("Draw?")


def play_rand_ai_game(console=True):
    board = chess.Board()
#    p1 = RandomAiAgent(True)
    p1 = MinMaxAgent(True, 1)
    p2 = MinMaxAgent(False, 1)
    play_game(board, p1, p2, console)
    return board


play_rand_ai_game(True)

"""
game_ends = {'75':0, 'insuf':0, 'stalemate':0, 'checkmate':0, '5-rep':0, 'draw':0}
for i in range(100):
    result = play_rand_ai_game(False)
    if result.is_seventyfive_moves():
       game_ends['75'] = game_ends['75'] + 1
       game_ends['draw'] = game_ends['draw'] + 1
    elif result.is_insufficient_material():
       game_ends['insuf'] = game_ends['insuf'] + 1
       game_ends['draw'] = game_ends['draw'] + 1
    elif result.is_stalemate():
       game_ends['stalemate'] = game_ends['stalemate'] + 1
       game_ends['draw'] = game_ends['draw'] + 1
    elif result.is_checkmate():
       game_ends['checkmate'] = game_ends['checkmate'] + 1
    elif result.is_fivefold_repetition():
       game_ends['5-rep'] = game_ends['5-rep'] + 1
       game_ends['draw'] = game_ends['draw'] + 1
print(game_ends)
"""
