from abc import ABC, abstractmethod
from collections import namedtuple

Coord = namedtuple('Coord', ['i', 'j'])

def init_board():
    player = 1
    board = [[0 for i in range(8)] for j in range(8)]
    board[1] = [Pon() for i in range(8)]
    board[0][0] = Rook(Coord(0,0), 1, )
    board[0][7] = Rook()
    board[0][1] = Knight()
    board[0][6] = Knight()
    board[0][2] = Bishop()
    board[0][5] = Bishop()
    board[0][3] = 6
    board[0][4] = 5
    player = -1
    board[6] = [Pon() for i in range(8)]
    board[7][0] = Rook()
    board[7][7] = Rook()
    board[7][1] = Knight()
    board[7][6] = Knight()
    board[7][2] = Bishop()
    board[7][5] = Bishop()
    board[7][3] = -5
    board[7][4] = -6
    return board

def sync_piece(board, piece, coord, player):
    board[coord.i][coord.j] = piece(coord, player)

def init_player(player):
    if player == 1:
        back_row = 0
        front_row = 1
    else:
        back_row = 7
        front_row = 6
    for i in range(8):
        sync_piece(board, Pon, Coord(fonrt_row,i), player)
    sync_piece(board, Rook, Coord(back_row,0), player)
    sync_piece(board, Rook, Coord(back_row,7), player)
    sync_piece(board, Knight, Coord(back_row,1), player)
    sync_piece(board, Knight, Coord(back_row,6), player)
    sync_piece(board, Bishop, Coord(back_row,2), player)
    sync_piece(board, Bihsop, Coord(back_row,5), player)
    sync_piece(board, Queen, Coord(back_row,3), player)
    sync_piece(board, King, Coord(back_row,4), player)


class Board():
    def __init__(self):
        self.board = init_board()

    def is_clear(self, coord):
        return self.board[coord.i][coord,j] == 0

    def is_friend(self, coord, player):
        if self.is_clear(coord):
            return False
        return self.board[coord.i][coord,j].owner == player


    def is_enemy(self, coord, player):
        if self.is_clear(coord):
            return False
        return self.board[coord.i][coord,j].owner == player * -1


    def print(self):
        for i in range(8):
            for j in range(8):
                n = self.board[i][j]
                if n >= 0:
                    print(" {}".format(self.board[i][j]), end="")
                else:
                    print(self.board[i][j], end="")

            print("")

    def movement(self, i, j, k, l):
        self.board[k][l] = self.board[i][j]
        self.board[i][j] = 0

    
    def possible_moves(self, piece, location):
        typ = math.abs(piece)
        player = piece / typ
        if typ == 1:
            pass
        elif typ == 2:
            pass
        elif typ == 3:
            pass
        elif typ == 4:
            pass
        elif typ == 5:
            pass
        elif typ == 6:
            pass
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
if __name__ == "__main__":
    board = Board()
    board.print()



class Piece():
    def __init__(self, coord, player, board):
        self.coord = coord
        self.owner = player
        self.board = board
   
    @abstractmethod
    def __str__(self):
        return ""

    @abstractmethod
    def get_possible_moves(self):
        return []

    @abstractmethod
    @staticmethod
    def get_value(self):
        return -1

    @abstractmethod
    def get_positional_value(self):
        return -1

class Pon(Piece):
    def __str__():
        return "1"

    def get_possible_moves(self):
        return check_board({()})
    

class Bishop(Piece):
    pass

class Knight(Piece):
    pass

class Rook(Piece):
    def get_possible_moves(self):
        moves = []
        pos = Coord(self.coord.i, self.coord.j)
        dirs = [Coord(1,0), Coord(0,1), Coord(-1,0), Coord(0,-1)]
        for dir_ in dirs:
            good = True
            while good:
                candidate_pos = Coord(pos.i+dir_.i, pos.j+dir_.j)
                if self.board.is_clear(candidate_pos):
                    moves.append(candidate_pos)
                    pos = candidate_pos
                elif self.board.is_enemy(candidate_pos, self.owner):
                    moves.append(candidate_pos)
                    good = False
                elif self.board.is_friend(candidate_pos, self.owner):
                    good = False
        return moves


class Queen(Piece):
    pass

class King(Piece):
    pass

class Board(list):
    def __init__():
        self.dims = 2
        self.size = 8
        for i in xrange(BOARD_SIZE):
                board.append([])
                for j in xrange(BOARD_SIZE):
                        if i == 0:
                                if j == 0 or j == 7:
                                        board[i].append(Rook(i,j,"W"))
                                if j == 1 or j == 6:
                                        board[i].append(Knight(i,j,"W"))
                                if j == 2 or j == 5:
                                        board[i].append(Bishop(i,j,"W"))
                                if j == 3:
                                        board[i].append(Queen(i,j,"W"))
                    if j == 4:
                        board[i].append(King(i,j,"W"))
                if i == 1:
                                    board[i].append(Pon(i,j,"W"))
                            if i == 6:
                                    board[i].append(Pon(i,j,"B"))
                            if i == 7:
                                    if j == 0 or j == 7:
                                            board[i].append(Rook(i,j,"B"))
                                    if j == 1 or j == 6:
                                            board[i].append(Knight(i,j,"B"))
                                    if j == 2 or j == 5:
                                            board[i].append(Bishop(i,j,"B"))
                                    if j == 3:
                                            board[i].append(Queen(i,j,"B"))
                                if j == 4:
                                            board[i].append(King(i,j,"B"))
    def print():
        for i in xrange(BOARD_SIZE):
                for j in xrange(BOARD_SIZE):
                print(self[i][j], end="")

        def has_enemy(x,y,my_color):
                return board[x][y].owner == my_color


if __name__ == "__main__":
    board = Board()
    board.print()

"""
