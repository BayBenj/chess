from abc import ABC, abstractmethod

def init_board():
    board = [[0 for i in range(8)] for j in range(8)]
    board[1] = [1 for i in range(8)]
    board[0][0] = 4
    board[0][7] = 4
    board[0][1] = 2
    board[0][6] = 2
    board[0][2] = 3
    board[0][5] = 3
    board[0][3] = 6
    board[0][4] = 5
    board[6] = [-1 for i in range(8)]
    board[7][0] = -4
    board[7][7] = -4
    board[7][1] = -2
    board[7][6] = -2
    board[7][2] = -3
    board[7][5] = -3
    board[7][3] = -5
    board[7][4] = -6
    return board


class Board():
    def __init__(self):
        self.board = init_board()

    
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


"""
class Piece():
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.owner = player
    
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
        return "P"

        def get_possible_moves(self):
                return check_board({()})
    

class Bishop(Piece):
    pass

class Knight(Piece):
    pass

class Rook(Piece):
    pass

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
