from games import *
from agents import *


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


def confusion_matrix(ais,game=TicTacToeBoard,n=1000,mirror=False):
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
                if ai1 != ai2 or mirror:
                    ratio = duel_ais(ai1,ai2,n,game,False)
                    ratios[pair] = ratio
                    pairs.add(pair)
                    precision = int(log10(n))
                    print(f"{ratio:.{int(log10(n))}}", end="\t\t")
                else:
                    print(f"n/a", end="\t\t")
            else:
                print("", end="\t\t")
        print("")
    return ratios


if __name__ == "__main__":
    #board = ChessBoard()
    #board.play(NegamaxAgent(1), RandomAgent(), True)

    #duel_ais(NegamaxAgent(2), RandomAgent(), 100, Connect4Board)

    confusion_matrix([RandomAgent(), NegamaxAgent(1)], ChessBoard, 10)

