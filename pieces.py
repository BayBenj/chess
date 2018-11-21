
from collections import namedtuple

Coord = namedtuple('Coord', ['i', 'j'])

DIAG_DIRS = {Coord(1,1), Coord(-1,-1), Coord(-1,1), Coord(1,-1)}
ORTH_DIRS = {Coord(0,1), Coord(1,0), Coord(0,-1), Coord(-1,0)}
ALL_DIRS = DIAG_DIRS | ORTH_DIRS
KNIGHT_DIRS = {Coord(-1,2), Coord(1,2), Coord(1,-2), Coord(-1,-2), Coord(-2,1), Coord(2,1), Coord(2,-1), Coord(-2,-1)}


class Piece(object):
    def __init__(self, coord, owner, board):
        self.i = coord.i
        self.j = coord.j
        self.owner = owner
        self.board = board
        self.threat = self.get_threatened()


#    @abstractmethod
    def __str__(self):
        return "({},{})".format(self.i,self.j)


#    @abstractmethod
    def get_threatened(self):
        raise NotImplementedError("Must override")


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


    #def move_to(self, coord):
    #    self.board.board[self.i][self.j] = None
    #    self.i = coord.i
    #    self.j = coord.j
    #    self.board.board[self.i][self.j] = self

    def straight_moves(self, dirs, line, threat):
        moves = []
        for dir_ in dirs:
            good = True
            pos = Coord(self.i, self.j)
            while good:
                candidate_pos = Coord(pos.i+dir_.i, pos.j+dir_.j)
                if not self.board.is_on_board(candidate_pos):
                    break
                if self.board.is_clear(candidate_pos):
                    moves.append(candidate_pos)
                    pos = candidate_pos
                elif self.board.is_enemy(candidate_pos, self.owner):
                    moves.append(candidate_pos)
                    break
                elif self.board.is_friend(candidate_pos, self.owner):
                    if threat:
                        moves.append(candidate_pos)
                    break
                if not line:
                    break
        return set(moves)


class Pon(Piece):
    def __init__(self, coord, owner, board):
        super().__init__(coord, owner, board)
        self.THREAT = False

    def __str__(self):
        return "p"


    def get_threatened(self):
        self.THREAT = True
        self.threat = self.get_possible_moves()
        self.THREAT = False


    def get_possible_moves(self):
        result = []
        diags = []
        diag1 = Coord(self.i-1*self.owner.n,self.j+1)
        diag2 = Coord(self.i-1*self.owner.n,self.j-1)
        if self.board.is_on_board(diag1):
            if self.THREAT: 
                diags.append(diag1)
            elif self.board.is_enemy(diag1, self.owner):
                diags.append(diag1)
        if self.board.is_on_board(diag2):
            if self.THREAT: 
                diags.append(diag2)
            elif self.board.is_enemy(diag2, self.owner):
                diags.append(diag2)
        result += diags
        up1 = Coord(self.i-1*self.owner.n,self.j)
        if self.board.is_on_board(up1) and self.board.is_clear(up1):
            result.append(up1)
            if self.i == self.owner.front_i:
                up2 = Coord(self.i+2*self.owner.n*-1,self.j)
                if self.board.is_on_board(up2) and self.board.is_clear(up2):
                    result.append(up2)
        return set(result)


class Bishop(Piece):
    def __str__(self):
        return "b"


    def get_threatened(self):
        return self.straight_moves(DIAG_DIRS, True, True)


    def get_possible_moves(self):
        return self.straight_moves(DIAG_DIRS, True, False)


class Knight(Piece):
    def __str__(self):
        return "h"


    def get_threatened(self):
        return self.straight_moves(KNIGHT_DIRS, False, True)


    def get_possible_moves(self):
        return self.straight_moves(KNIGHT_DIRS, False, False)


class Rook(Piece):
    def __str__(self):
        return "r"


    def get_threatened(self):
        return self.straight_moves(ORTH_DIRS, True, True)


    def get_possible_moves(self):
        return self.straight_moves(ORTH_DIRS, True, False)


class Queen(Piece):
    def __str__(self):
        return "q"


    def get_threatened(self):
        return self.straight_moves(ALL_DIRS, True, True)


    def get_possible_moves(self):
        return self.straight_moves(ALL_DIRS, True, False)


class King(Piece):
    def __str__(self):
        return "k"


    def get_threatened(self):
        return self.straight_moves(ALL_DIRS, False, True)


    def get_possible_moves(self):
        return self.straight_moves(ALL_DIRS, False, False)

