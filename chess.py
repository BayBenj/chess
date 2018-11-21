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
            #self.board = board #try this after everything is working
            for i in range(8):
                for j,x in enumerate(args[0].board[i]):
                    if isinstance(x, Piece):
                        cls = type(x)
                        coord = Coord(x.i,x.j)
                        owner = x.owner
                        self.board[i][j] = cls(coord, owner, self)
                    else:
                        self.board[i][j] = x
#            print("\n\n~~~~~~~")
#            self.print("\t")
#            print(args[1])
            self.movement(args[1])
#            self.print("\t")


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


    def print(self, pre=None):
        for i in range(8):
            if pre is not None:
                print(pre, end="")
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


    def sync_piece(self, piece, dest, player):
        self.board[dest.i][dest.j] = piece(dest, player, self)


    def movement(self, m):
        if m.i == m.k and m.j == m.l:
            raise ValueError("Cannot move to current space!")
        x = self.board[m.i][m.j]
        # Check for queen rule
        if m.k == x.owner.pon_i and isinstance(x, Pon):
            cls = Queen #TODO: fix?
        else:
            cls = type(x)
#        print("moving from {},{} to {},{}".format(m.i,m.j,m.k,m.l))
        self.sync_piece(cls, Coord(m.k,m.l), x.owner)
        self.board[m.i][m.j] = None

    def get_all_pieces_for_player(self, player):
        result = set()
        for i in range(8):
            for j in range(8):
                if not isinstance(self.board[i][j], Piece):
                    continue
                if self.board[i][j].owner == player:
                    result.add(self.board[i][j])
        return result


    def get_all_threats_for_player(self, player):
        pieces = self.get_all_pieces_for_player(player)
        result = set()
        for piece in pieces:
            threats = piece.get_threatened()
            if threats is not None:
                result |= threats
        return result


    def get_king(self, player):
        for i in range(8):
            for j in range(8):
                if not isinstance(self.board[i][j], King):
                    continue
                if self.board[i][j].owner == player:
                    return self.board[i][j]


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
        result = dict()
        for piece, moves in all_possibles.items():
            for move in moves:
                possible_movement = Movement(piece.i,piece.j,move.i,move.j)
                possible_board = Board(board, possible_movement)
                if not self.is_in_check(player, opponent, possible_board):
                    if result.get(piece) is None:
                        result[piece] = {possible_movement}
                    else:
                        tmp = set(result[piece])
                        tmp.add(possible_movement)
                        result[piece] = tmp
#        print("possible moves:")
#        pp.pprint(result)
        return result


    def is_in_check(self, player, opponent, board):
        threatened_moves = board.get_all_threats_for_player(opponent)
        king = board.get_king(player)
        if Coord(king.i,king.j) in threatened_moves:
            return True
        return False
        

    def update_check_status(self, player, opponent):
        player.in_check = self.is_in_check(player, opponent, self.board)
        if player.in_check:
            print("Player {} in check!".format(player.n))
        return player.in_check


    def check_for_two_kings(self, p1, p2):
        if len(self.board.get_all_pieces_for_player(p1)) == 1 and len(self.board.get_all_pieces_for_player(p2)) == 1:
            STALEMATE = True
            print("Stalemate!")
            sys.exit(0)


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
            if val is not None:
                total += len(val)
#        print("(random_ turn) possible moves for player {}: {}".format(player, total))
#        pp.pprint(possibles)
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
                    src = key
                    dest = coord
                    end = True
                    break
            if end:
                break
        print(Movement(src.i,src.j,dest.k,dest.l))
        self.board.movement(Movement(src.i,src.j,dest.k,dest.l))
        print("Player {} (AI) moves:".format(player.n))
        self.board.print()


if __name__ == "__main__":
    game = Game()
    sys.exit(game.play())

