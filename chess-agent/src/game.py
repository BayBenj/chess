
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
    
 
def play_game(board, p1, p2, console):
    while not board.is_game_over():
        if console:
            print("WHITE TURN:")
        p1.turn(board)
        if console:
            print_state(board)
        if not board.is_game_over():
            if console:
                print("BLACK TURN:")
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
    p1 = RandomAiAgent(1)
    p2 = RandomAiAgent(2)
    play_game(board, p1, p2, console)
    return board


#play_rand_ai_game(True)

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
