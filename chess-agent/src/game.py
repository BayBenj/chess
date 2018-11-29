
import chess
from random import randint


class Agent(object):
    def __init__(self, n):
        self.n = n


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

def print_state(board):
    print("-" * 16)
#    print("a b c d e f g h")
    print(board)
    print("")
    
 
def play_game(board, p1, p2):
    while not board.is_game_over():
        print("WHITE TURN:")
        p1.turn(board)
        print_state(board)
        if not board.is_game_over():
            print("BLACK TURN:")
            p2.turn(board)
            print_state(board)


def play_rand_ai_game():
    board = chess.Board()
    p1 = RandomAiAgent(1)
    p2 = RandomAiAgent(2)
    play_game(board, p1, p2)


play_rand_ai_game()

