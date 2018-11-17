from abc import ABC, abstractmethod
import random
import pprint

from pieces import *

pp = pprint.PrettyPrinter(indent=4)

class Player(object):
    def __init__(self, cpu, n):
        if n == 1:
            self.front_i = 6
            self.back_i = 7
            self.pon_i = 0
        else:
            self.front_i = 1
            self.back_i = 0
            self.pon_i = 7
        self.n = n
        self.cpu = cpu

    def __eq__(self, other):
        #TODO fix
        if not isinstance(other, Player):
            return False
        return self.n == other.n

    
    def __str__(self):
        return str(self.n)


class Board(object):
    def __init__(self):
        self.board = [[None for i in range(8)] for j in range(8)]


    def __str__(self):
        self.print()


    def is_on_board(self, coord):
        nums = [coord.i, coord.j]
        for num in nums:
            if num > 7 or num < 0:
                return False
        return True


    def is_clear(self, coord):
        return self.board[coord.i][coord.j] is None


    def is_friend(self, coord, player):
        if self.is_clear(coord):
            return False
        return self.board[coord.i][coord.j].owner == player


    def is_enemy(self, coord, player):
        if self.is_clear(coord):
            return False
        return (self.board[coord.i][coord.j].owner.n) == (player.n * -1)


    def sync_piece(self, piece, coord, player):
        self.board[coord.i][coord.j] = piece(coord, player, self)


    def print(self):
        for i in range(8):
            for j in range(8):
                x = self.board[i][j]
                if isinstance(x, Piece) and x.owner.n == 1:
                    print(" {}".format(str(x).capitalize()), end="")
                elif x is None:
                    print(" .", end="")
                else:
                    print(" {}".format(str(x)), end="")

            print("")
        print("")


    def movement(self, i, j, k, l):
        # Check for queen rule
        x = self.board[i][j]
        if x.i == x.owner.pon_i and isinstance(x, Pon):
            self.sync_piece(Queen, Coord(k,l), x.owner)
            self.board[i][j] = None
        else:
            self.board[i][j].move_to(Coord(k,l))
            #self.board[k][l] = x
            #self.board[k][l].coord = Coord(k,l)
            #self.board[i][j] = None


    def get_all_pieces_for_player(self, player):
        result = set()
        for i in range(8):
            for j in range(8):
                if not isinstance(self.board[i][j], Piece):
                    continue
                if self.board[i][j].owner == player:
                    result.add(self.board[i][j])
        return result


    def get_all_possible_moves_for_player(self, player):
        pieces = self.get_all_pieces_for_player(player)
        result = {piece:piece.get_possible_moves() for piece in pieces}
        return result

"""
SIMPLE BOARD KEY
positive = white
negative = black
1 = pon
2 = knight
3 = bishop
4 = rook
5 = queen
6 = king
"""

class Game(object):
    def __init__(self):
        self.white = Player(True, 1)
        self.black = Player(True, -1)
        self.board = Board()
        self.init_players()
        self.board.print()


    def init_players(self):
        self.init_player(self.white)
        self.init_player(self.black)


    def init_player(self, player):
        for i in range(8):
            self.board.sync_piece(Pon, Coord(player.front_i,i), player)
        self.board.sync_piece(Rook, Coord(player.back_i,0), player)
        self.board.sync_piece(Rook, Coord(player.back_i,7), player)
        self.board.sync_piece(Knight, Coord(player.back_i,1), player)
        self.board.sync_piece(Knight, Coord(player.back_i,6), player)
        self.board.sync_piece(Bishop, Coord(player.back_i,2), player)
        self.board.sync_piece(Bishop, Coord(player.back_i,5), player)
        self.board.sync_piece(Queen, Coord(player.back_i,3), player)
        self.board.sync_piece(King, Coord(player.back_i,4), player)


    def play(self):
        game = True
        while game:
            self.random_turn(Player(True, 1))
            self.random_turn(Player(True, -1))


    def human_turn(self, player):
        print("Player move: ", end="")
        i = input()
        if i == "p":
            print("Turn passed")
            return
        i = str(i)
        j = int(input())
        k = int(input())
        l = int(input())
        if self.board.board[i][j].owner == player:
            if Coord(k,l) in board.board[i][j].get_possible_moves():
                self.board.movement(i,j,k,l)
                self.board.print()
            else:
                print("Move not allowed!")
        else:
            print("You do not own that piece!")


    def random_turn(self, player):
        possibles = self.board.get_all_possible_moves_for_player(player)
        total = 0
        for key, val in possibles.items():
            total += len(val)
        print("possible moves for player {}: {}".format(player, total))
        pp.pprint(possibles)
        r = random.randint(0,total-1)
        total = 0 
        end = False
        for key, val in possibles.items():
            for coord in val:
                total += 1
                if total > r:
                    spot = key
                    result = coord
                    end = True
                    break
            if end:
                break
        self.board.movement(spot.i,spot.j,coord.i,coord.j)
        print("Computer moves:")
        self.board.print()


if __name__ == "__main__":
    game = Game()
    game.play()

