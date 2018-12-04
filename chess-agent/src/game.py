
import chess
import random
import sys
from collections import namedtuple


INF = float('inf')
NEG_INF = float('-inf')


def rand_elem_count(l):
    size = l.count()
    r = random.randint(0,size-1)
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
        j = str(int(input()))
        k = str(input())
        l = str(int(input()))
        move = chess.Move.from_uci(f'{i}{j}{k}{l}')
        if move in board.legal_moves:
            self.do_move(move, board)


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
        self.do_move(random.choice(list(legal_moves)), board)


SCORE_MAP = {1:100, 2:320, 3:330, 4:500, 5:900, 6:20000}


class MinMaxAgent(AiAgent):
    def __init__(self, n, ply):
        AiAgent.__init__(self, n)
        self.ply = ply

    def turn(self, board):
        """
        """
        #_, move = self.recurse_minimax2(board, 2, self.color)
        #score, move = self.alpha_beta_max(board, NEG_INF, INF, self.ply)
        mm = self.alpha_beta_max
        alpha = NEG_INF
        beta = INF
        if not self.color:
            mm = self.alpha_beta_min
        score, move = mm(board, alpha, beta, self.ply)
        self.do_move(move, board)


    def alpha_beta_max(self, board, alpha, beta, depth):
        if depth == 0:
            return eval_board(board, SCORE_MAP), board.peek()
        best_moves = []
        legal_moves = board.legal_moves
        for move in legal_moves:
            self.do_move(move, board)
            score, _ = self.alpha_beta_min(board, alpha, beta, depth - 1)
            board.pop()
            if score >= beta:
                return beta, move       #fail hard beta-cutoff
            if score > alpha:
                alpha = score           #alpha acts like max in MiniMax
                best_moves = [move]
            elif score == alpha:
                best_moves.append(move)
        if legal_moves.count() == 0:
            raise ValueError("No legal moves!")
        if len(best_moves) == 0:
            return alpha, rand_elem_count(legal_moves)
        return alpha, random.choice(best_moves)


    def alpha_beta_min(self, board, alpha, beta, depth):
        if depth == 0:
            return eval_board(board, SCORE_MAP), board.peek(), board.peek()
        best_moves = []
        legal_moves = board.legal_moves
        for move in legal_moves:
            self.do_move(move, board)
            score, _ = self.alpha_beta_max(board, alpha, beta, depth - 1)
            board.pop()
            if score <= alpha:
                return alpha, move      #fail hard alpha-cutoff
            if score < beta:
                beta = score            #beta acts like max in MiniMax
                best_moves = [move]
            elif score == beta:
                best_moves.append(move)
        if legal_moves.count() == 0:
            raise ValueError("No legal moves!")
        if len(best_moves) == 0:
            return beta, rand_elem_count(legal_moves)
        return beta, random.choice(best_moves)


    def maxi(self, board, depth):
        if depth == 0:
            return eval_board(board, SCORE_MAP), board.peek()
        max_score = NEG_INF
        max_moves = []
        for move in board.legal_moves:
            self.do_move(move, board)
            score, _ = self.mini(board, depth - 1)
            board.pop()
            if score > max_score:
                max_score = score
                max_moves = [move]
            elif score == max_score:
                max_moves.append(move)
        return max_score, random.choice(max_moves)


    def mini(self, board, depth):
        if depth == 0:
            return -1 * eval_board(board, SCORE_MAP), board.peek()
        min_score = INF
        min_moves = []
        for move in board.legal_moves:
            self.do_move(move, board)
            score, _ = self.maxi(board, depth - 1)
            board.pop()
            if score < min_score:
                min_score = score
                min_moves = [move]
            elif score == min_score:
                min_moves.append(move)
        return min_score, random.choice(min_move)


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
                    r = random.randint(0,1)
                    if r == 0:
                        best_move = move
                return alpha
            else:
#                best_score = 9_999
                if new_score < best_score:
                    best_move = move
                    best_score = new_score
                elif new_score == best_score:
                    r = random.randint(0,1)
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
            return random.choice(opt_moves)
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
    if board.is_checkmate():
        if board.turn:
            return NEG_INF
        else:
            return INF
    elif board.is_seventyfive_moves() or board.is_insufficient_material() or  board.is_stalemate() or board.is_fivefold_repetition():
            return 0
        
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
    board


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
    board
    p1 = MinMaxAgent(True, 4)
    p2 = RandomAiAgent(False)
    play_game(board, p1, p2, console)
    return board


play_rand_ai_game(True)



