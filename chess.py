from abc import ABC, abstractmethod
import random
import sys
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
        self.in_check = False
        self.in_checkmate = False


    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.n == other.n

    
    def __str__(self):
        return str(self.n)


Movement = namedtuple('Movement', ['i', 'j', 'k', 'l'])


class Board(object):
    def __init__(self, *args, **kwargs):
        self.board = [[None for i in range(8)] for j in range(8)]
        if len(args) == 2:
            #self.board = board #try this
            for i,x in enumerate(args[0].board):
                for j,y in enumerate(x):
                    self.board[i][j] = y
            self.movement(args[1])


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


    def movement(self, m):
        # Check for queen rule
        x = self.board[m.i][m.j]
        if m.k == x.owner.pon_i and isinstance(x, Pon):
            self.sync_piece(Queen, Coord(m.k,m.l), x.owner)
            self.board[m.i][m.j] = None
        else:
            self.board[m.i][m.j].move_to(Coord(m.k,m.l))


    def get_all_pieces_for_player(self, player):
        result = set()
        for i in range(8):
            for j in range(8):
                if not isinstance(self.board[i][j], Piece):
                    continue
                if self.board[i][j].owner == player:
                    result.add(self.board[i][j])
        return result


class Game(object):
    
    STALEMATE = False

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


    def get_all_possible_moves_for_player(self, player, opponent, board):
        """
            Get all possible moves for a player, excluding moves into check.
        """
        pieces = board.get_all_pieces_for_player(player)
        all_possibles = {piece:piece.get_possible_moves() for piece in pieces}
        result = dict(all_possibles)
        for piece, moves in all_possibles.items():
            for move in moves:
                possible_movement = Movement(piece.i,piece.j,move.i,move.j)
                possible_board = Board(board, possible_movement)
                if not self.is_in_check(player, opponent, possible_board):
                    result[piece] = result[piece].add(possible_movement)
        return result


    def is_in_check(self, player, opponent, board):
        possibles = self.get_all_possible_moves_for_player(opponent, player, board)
        for piece, coords in possibles.items():
            for coord in coords:
                if isinstance(board.board[coord.i][coord.j], King) and board.board[coord.i][coord.j].owner is opponent:
                    return True
        return False
        

    def update_check_status(self, player, opponent):
        player.in_check = self.is_in_check(player, opponent, self.board)
        if player.in_check:
            print("Player {} in check!".format(player.n))
        return player.in_check
        

    def play(self):
        game = True
        white = Player(True, 1)
        black = Player(True, -1)
        while white.in_checkmate == False and black.in_checkmate == False:
            self.update_check_status(white, black)
            self.random_turn(white, black)
            self.update_check_status(black, white)
            self.random_turn(black, white)
        print("CHECKMATE!")


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
                self.board.movement(Movement(i,j,k,l))
                self.board.print()
            else:
                print("Move not allowed!")
        else:
            print("You do not own that piece!")


    def random_turn(self, player, opponent):
        possibles = self.get_all_possible_moves_for_player(player, opponent, self.board)
        total = 0
        for key, val in possibles.items():
            total += len(val)
        #print("possible moves for player {}: {}".format(player, total))
        #pp.pprint(possibles)
        if total == 0 and not player.in_check:
            STALEMATE = True
            print("Stalemate!")
            sys.exit(0)
        elif total == 0 and player.in_check:
            player.in_checkmate = True
            print("Player {} is in CHECKMATE!".format(player.n))
            sys.exit(0)
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
        self.board.movement(Movement(spot.i,spot.j,coord.i,coord.j))
        print("Player {} (AI) moves:".format(player.n))
        self.board.print()


if __name__ == "__main__":
    game = Game()
    sys.exit(game.play())

