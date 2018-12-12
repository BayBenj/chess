
import numpy as np
from collections import namedtuple
import random
from abc import ABC, abstractmethod
from math import log10
import logging

import chess

"""
@TODO add determinism / probabalism to agent makeup.
"""


INF = float('inf')
NEG_INF = float('-inf')


class Agent(object):
    def __str__(self):
        return type(self).__name__ + "   "


    def __eq__(self, other):
        return type(self) is type(other)


    def __hash__(self):
        return hash(str(self))


    def do_move(self, move, board):
        board.push(move)


    def turn(self, board):
        """
        Given the current board, decide a move to make.
        """
        pass


class HumanAgent(Agent):
    def turn(self, board):
        """
        Prompt the user for a move, then return that move.
        """
        print("Player move: ", end="")
        col = 99
        while move not in board.legal_moves():
            col = str(int(input()))
        self.do_move(col)


class AiAgent(Agent):
    def turn(self, board):
        """
        Prompt the user for a move, then return that move.
        """
        pass


class RandomAgent(AiAgent):
    def turn(self, board):
        """
        Based on the board state, pick a random legal move.
        """
        legal_moves = board.legal_moves()
        self.do_move(random.choice(list(legal_moves)), board)


class NegamaxAgent(AiAgent):
    def __init__(self, ply):
        self.ply = ply


    def __str__(self):
        return type(self).__name__ + f"({self.ply})"


    def __hash__(self):
        return hash(self.ply)


    def __eq__(self, other):
        return type(self) is type(other) and self.ply == other.ply


    def turn(self, board):
        """
        """
        score, move = self.negamax(board, self.ply, NEG_INF, INF)
        self.do_move(move, board)


    def negamax(self, board, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            if board.turn:
                return board.eval(), board.peek()
            return -board.eval(), board.peek()

#        legal_moves = list(board.legal_moves())
        legal_moves = board.attacker_priority_sort()
#        random.shuffle(legal_moves)
        value = NEG_INF
        best_moves = []
        for move in legal_moves:
            self.do_move(move, board)
            new_value = max(value, -self.negamax(board, depth - 1, -beta, -alpha)[0])
            board.pop()
            if new_value > value:
                best_moves = [move]
            else:
                best_moves.append(move) #TODO: is this right?
            value = new_value
            alpha = max(alpha, value)
            if alpha >= beta:
                break #(* cut-off *)
        return value, random.choice(best_moves)

