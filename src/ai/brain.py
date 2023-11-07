#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: brain.py
# Author: MasterLaplace
# Created on: 2023-11-7

from random import randint
from enum import Enum
from game.game import Game

class Brain:
    """_summary_ The brain of the client
    """

    class CommandType(Enum):
        """_summary_ Enum for command type
        """
        UNKNOWN = 0
        ERROR = 1
        MESSAGE = 2
        DEBUG = 3
        SUGGEST = 4

    def __init__(self):
        self.name = "MinMaxBrain"
        self.version = "0.1.0"
        self.author = "Enzotekrennes;MasterLaplace"
        self.country = "France"

    def start(self):
        print("OK - everything is good")
        # TODO: Initialize the brain

    def restart(self):
        # TODO: Restart the brain
        pass

    def about(self):
        print(f"name=\"{self.name}\", version=\"{self.version}\", author=\"{self.author}\", country=\"{self.country}\"")

    @staticmethod
    def isMovesLeft(board: list[list[str]], size: tuple[int, int]) -> bool:
        """_summary_ Check if there are moves left on the board

        Args:
            board (list[list[str]]): _description_ The board of the game
            size (tuple[int, int]): _description_ The size of the board

        Returns:
            bool: _description_ True if there are moves left, False otherwise
        """

        for i in range(0, size[0]) :
            for j in range(0, size[1]) :
                if board[i][j] == Game.CaseSate.EMPTY:
                    return True
        return False

    @staticmethod
    def evaluate(board: list[list[str]], size: tuple[int, int]) -> Game.CaseSate:
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                # check horizontal
                if j + 4 < size[1]:
                    if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == board[i][j + 4]:
                        return Game.CaseSate.PLAYER1 if board[i][j] == Game.CaseSate.PLAYER1 else Game.CaseSate.PLAYER2
                # check vertical
                if i + 4 < size[0]:
                    if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == board[i + 4][j]:
                        return Game.CaseSate.PLAYER1 if board[i][j] == Game.CaseSate.PLAYER1 else Game.CaseSate.PLAYER2
                # check diagonal
                if i + 4 < size[0] and j + 4 < size[1]:
                    if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == board[i + 4][j + 4]:
                        return Game.CaseSate.PLAYER1 if board[i][j] == Game.CaseSate.PLAYER1 else Game.CaseSate.PLAYER2
        # Else if none of them have won then return EMPTY
        return Game.CaseSate.EMPTY

    @staticmethod
    def minimax(board: list[list[str]], size: tuple[int, int], depth: int, isMax: bool) -> int:
        """_summary_ Minimax algorithm to find the best solution

        Args:
            board (list[list[str]]): _description_ The board of the game
            size (tuple[int, int]): _description_ The size of the board
            depth (int): _description_ The depth of the algorithm (0 at the beginning)
            isMax (bool): _description_ True if the algorithm is in the maximizer state, False otherwise

        Returns:
            int: _description_ The best score for the next turn
        """
        score = Brain.evaluate(board, size)

        # If Maximizer has won the game return his/her
        # evaluated score
        if score == Game.CaseSate.PLAYER1:
            return 10

        # If Minimizer has won the game return his/her
        # evaluated score
        if score == Game.CaseSate.PLAYER2:
            return -10

        # If there are no more moves and no winner then
        # it is a tie
        if Brain.isMovesLeft(board, size) == False:
            return 0

        # If this maximizer's move
        if isMax:
            best = -1000

            # Traverse all cells
            for i in range(0, size[0]):
                for j in range(0, size[1]):

                    # Check if cell is empty
                    if board[i][j] == Game.CaseSate.EMPTY:

                        # Make the move
                        board[i][j] = Game.CaseSate.PLAYER1

                        # Call minimax recursively and choose
                        # the maximum value
                        best = max(best, Brain.minimax(board, size, depth + 1, not isMax))

                        # Undo the move
                        board[i][j] = Game.CaseSate.EMPTY
            return best

        # If this minimizer's move
        else :
            best = 1000

            # Traverse all cells
            for i in range(0, size[0]):
                for j in range(0, size[1]):

                    # Check if cell is empty
                    if board[i][j] == Game.CaseSate.EMPTY:

                        # Make the move
                        board[i][j] = Game.CaseSate.PLAYER2

                        # Call minimax recursively and choose
                        # the minimum value
                        best = min(best, Brain.minimax(board, size, depth + 1, not isMax))

                        # Undo the move
                        board[i][j] = Game.CaseSate.EMPTY
            return best

    def findBestSolution(self, board: list[list[Game.CaseSate]], size: tuple[int, int]) -> tuple[int, int]:
        """_summary_ Find the best solution for the next turn

        __description__ Find the best solution for the next turn by using the minimax algorithm

        __param__ board: The board of the game (list[list[PLAYER1, PLAYER2, EMPTY]])
        __param__ size: The size of the board (tuple(x, y))

        __return__ tuple[int, int]: The best solution for the next turn
        """
        bestVal = -1000
        bestMove = (-1, -1)

        # Traverse all cells, evaluate minimax function for
        # all empty cells. And return the cell with optimal
        # value.
        for i in range(0, size[0]):
            for j in range(0, size[1]):

                # Check if cell is empty
                if board[i][j] == Game.CaseSate.EMPTY:

                    # Make the move
                    board[i][j] = Game.CaseSate.PLAYER1

                    # compute evaluation function for this
                    # move.
                    moveVal = Brain.minimax(board, size, 0, False)

                    # Undo the move
                    board[i][j] = Game.CaseSate.EMPTY

                    # If the value of the current move is
                    # more than the best value, then update
                    # best
                    if moveVal > bestVal:
                        bestMove = (i, j)
                        bestVal = moveVal

        print(f"{bestMove[0]},{bestMove[1]}")
        return bestMove

    def sendCommand(self):
        # TODO: Send command to the protocol
        pass

    def end(self):
        # TODO: Terminate the brain
        pass
