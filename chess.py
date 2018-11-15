from abc import ABC, abstractmethod
from collections import namedtuple

Coord = namedtuple('Coord', ['i', 'j'])


DIAG_DIRS = {Coord(1,1), Coord(-1,-1), Coord(-1,1), Coord(1,-1)}
ORTH_DIRS = {Coord(0,1), Coord(1,0), Coord(0,-1), Coord(-1,0)}
ALL_DIRS = DIAG_DIRS | ORTH_DIRS
KNIGHT_DIRS = {Coord(-1,2), Coord(1,2), Coord(1,-2), Coord(-1,-2), Coord(-2,1), Coord(2,1), Coord(2,-1), Coord(-2,-1)}


class Piece():
    def __init__(self, coord, owner, board):
        self.coord = coord
        self.owner = owner
        self.board = board


#    @abstractmethod
    def __str__(self):
        return ""


#    @abstractmethod
    def get_possible_moves(self):
        return []


#    @abstractmethod
#    @staticmethod
    def get_value(self):
        return -1


#    @abstractmethod
    def get_positional_value(self):
        return -1


    def straight_moves(self, dirs, line):
        moves = []
        for dir_ in dirs:
            good = True
            pos = Coord(self.coord.i, self.coord.j)
            while good:
                candidate_pos = Coord(pos.i+dir_.i, pos.j+dir_.j)
                if not self.board.is_on_board(candidate_pos):
                    break
                if self.board.is_clear(candidate_pos):
                    print("!")
                    moves.append(candidate_pos)
                    pos = candidate_pos
                elif self.board.is_enemy(candidate_pos, self.owner):
                    print("enemy")
                    moves.append(candidate_pos)
                    break
                elif self.board.is_friend(candidate_pos, self.owner):
                    print("friend")
                    break
                if not line:
                    break
        return set(moves)


class Pon(Piece):
    def __str__(self):
        return "1"

    def get_possible_moves(self):
        if self.owner == 1:
            front_row = 1
        else:
            front_row = 6
        result = []
        diags = []
        diag1 = Coord(self.coord.i+1*self.owner,self.coord.j+1)
        diag2 = Coord(self.coord.i+1*self.owner,self.coord.j-1)
        if self.board.is_on_board(diag1) and self.board.is_enemy(diag1, self.owner):
            diags.append(diag1)
        if self.board.is_on_board(diag2) and self.board.is_enemy(diag2, self.owner):
            diags.append(diag2)
        result += diags
        up1 = Coord(self.coord.i+1*self.owner,self.coord.j)
        if self.board.is_on_board(up1) and self.board.is_clear(up1):
            result.append(up1)
            if self.coord.i == front_row:
                up2 = Coord(self.coord.i+2*self.owner,self.coord.j)
                if self.board.is_on_board(up2) and self.board.is_clear(up2):
                    result.append(up2)
        return set(result)
    

class Bishop(Piece):
    def __str__(self):
        return "3"
    
    
    def get_possible_moves(self):
        return self.straight_moves(DIAG_DIRS, True)


class Knight(Piece):
    def __str__(self):
        return "2"
    
    
    def get_possible_moves(self):
        return self.straight_moves(KNIGHT_DIRS, False)


class Rook(Piece):
    def __str__(self):
        return "4"
    
    
    def get_possible_moves(self):
        return self.straight_moves(ORTH_DIRS, True)


class Queen(Piece):
    def __str__(self):
        return "5"

    
    def is_on_board(self):
        super.is_on_board()

    
    def get_possible_moves(self):
        return self.straight_moves(ALL_DIRS, True)


class King(Piece):
    def __str__(self):
        return "6"
    
    
    def get_possible_moves(self):
        return self.straight_moves(ALL_DIRS, False)


class Board():
    def __init__(self):
        self.init_board()


    def __str__(self):
        self.print()


    def is_on_board(self, coord):
        nums = [coord.i, coord.j]
        for num in nums:
            if num > 7 or num < 0:
                return False
        return True


    def is_clear(self, coord):
        return self.board[coord.i][coord.j] == 0


    def is_friend(self, coord, player):
        if self.is_clear(coord):
            return False
        return self.board[coord.i][coord.j].owner == player


    def is_enemy(self, coord, player):
        if self.is_clear(coord):
            return False
        return (self.board[coord.i][coord.j].owner) == (player * -1)


    def init_board(self):
        self.board = [[0 for i in range(8)] for j in range(8)]
        self.init_player(1)
        self.init_player(-1)


    def sync_piece(self, piece, coord, player):
        self.board[coord.i][coord.j] = piece(coord, player, self)


    def init_player(self, player):
        if player == 1:
            back_row = 0
            front_row = 1
            queen = 3
            king = 4
        else:
            back_row = 7
            front_row = 6
            queen = 3
            king = 4
        for i in range(8):
            self.sync_piece(Pon, Coord(front_row,i), player)
        self.sync_piece(Rook, Coord(back_row,0), player)
        self.sync_piece(Rook, Coord(back_row,7), player)
        self.sync_piece(Knight, Coord(back_row,1), player)
        self.sync_piece(Knight, Coord(back_row,6), player)
        self.sync_piece(Bishop, Coord(back_row,2), player)
        self.sync_piece(Bishop, Coord(back_row,5), player)
        self.sync_piece(Queen, Coord(back_row,queen), player)
        self.sync_piece(King, Coord(back_row,king), player)

    
    def print(self):
        for i in range(8):
            for j in range(8):
                n = self.board[i][j]
                #if n >= 0:
                #    print(" {}".format(self.board[i][j]), end="")
                #else:
                print(self.board[i][j], end="")

            print("")


    def movement(self, i, j, k, l):
        self.board[k][l] = self.board[i][j]
        self.board[k][l].coord = Coord(k,l)
        self.board[i][j] = 0


    def get_all_pieces(self, player):
        result = {}
        for i in range(8):
            for j in range(8):
                if not isinstance(self.board[i][j], Piece):
                    continue
                if self.board[i][j].owner == player:
                    result[Coord(i,j)] = self.board[i][j]
        return result


    def get_all_possible_moves(self, player):
        pieces = self.get_all_pieces(player)
        result = [piece.get_possible_moves() for coord, piece in pieces.items()]
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

def human_turn(board, player):
    print("Player move: ", end="")
    i = int(input())
    j = int(input())
    k = int(input())
    l = int(input())
    if Coord(k,l) in board.board[i][j].get_possible_moves():
        board.movement(i,j,k,l)
        board.print()
    else:
        print("Move not allowed!")

if __name__ == "__main__":
    board = Board()
    board.print()
    #print("possible moves for pon: {}".format(board.board[6][0].get_possible_moves()))
    #print("possible moves for player 1: {}".format(board.get_all_possible_moves(1)))
    good = True
    while good:
        human_turn(board, -1)


