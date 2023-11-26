#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: brain.py
# Author: MasterLaplace, Enzotekrennes
# Created on: 2023-11-7

from enum import Enum
from src.game.game import Game

import subprocess

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
        self.name = "Laplacian Expanded Tree (LET) AI"
        self.version = "1.0.0"
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

        for i in range(size[0]) :
            for j in range(size[1]) :
                if board[i][j] == Game.CaseSate.EMPTY:
                    return True
        return False

    @staticmethod
    def evaluate(board: list[list[str]], size: tuple[int, int]) -> int:
        """_summary_ Evaluate the board and return the score
        Args:
            board (list[list[str]]): _description_ The board of the game
            size (tuple[int, int]): _description_ The size of the board
        Returns:
            int: _description_ The score of the board (10 if PLAYER1 wins, -10 if PLAYER2 wins, 0 otherwise)
        """
        for i in range(size[0]):
            for j in range(size[1]):
                if board[i][j] == Game.CaseSate.EMPTY:
                    continue
                # check horizontal
                if j + 4 < size[1]:
                    if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == board[i][j + 4]:
                        return 10 if board[i][j] == Game.CaseSate.PLAYER1 else -10
                # check vertical
                if i + 4 < size[0]:
                    if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == board[i + 4][j]:
                        return 10 if board[i][j] == Game.CaseSate.PLAYER1 else -10
                # check diagonal
                if i + 4 < size[0] and j + 4 < size[1]:
                    if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == board[i + 4][j + 4]:
                        return 10 if board[i][j] == Game.CaseSate.PLAYER1 else -10
                # check anti-diagonal
                if i + 4 < size[0] and j - 4 >= 0:
                    if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == board[i + 4][j - 4]:
                        return 10 if board[i][j] == Game.CaseSate.PLAYER1 else -10
        return 0

    @staticmethod
    def minimax(board: list[list[str]], size: tuple[int, int], depth: int, isMax: bool, alpha: int, beta: int) -> int:
        """_summary_ Minimax algorithm to find the best solution
        Args:
            board (list[list[str]]): _description_ The board of the game
            size (tuple[int, int]): _description_ The size of the board
            depth (int): _description_ The depth of the algorithm (number of moves to look ahead)
            isMax (bool): _description_ True if it's the turn of the player 1, False otherwise
            alpha (int): _description_ The alpha value for the alpha-beta pruning
            beta (int): _description_ The beta value for the alpha-beta pruning
        Returns:
            int: _description_ The score of the board (10 if PLAYER1 wins, -10 if PLAYER2 wins, best score otherwise)
        """
        score = Brain.evaluate(board, size)

        if depth == 0 or score != 0:
            return score

        if isMax:
            best = -1000

            for i in range(size[0]):
                for j in range(size[1]):
                    if board[i][j] == Game.CaseSate.EMPTY:
                        board[i][j] = Game.CaseSate.PLAYER1
                        best = max(best, Brain.minimax(board, size, depth - 1, not isMax, alpha, beta))
                        board[i][j] = Game.CaseSate.EMPTY

                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break  # Beta pruning

            return best
        else:
            best = 1000

            for i in range(size[0]):
                for j in range(size[1]):
                    if board[i][j] == Game.CaseSate.EMPTY:
                        board[i][j] = Game.CaseSate.PLAYER2
                        best = min(best, Brain.minimax(board, size, depth - 1, not isMax, alpha, beta))
                        board[i][j] = Game.CaseSate.EMPTY

                        beta = min(beta, best)
                        if beta <= alpha:
                            break  # Alpha pruning

            return best

    def findBestSolution(self, board: list[list[Game.CaseSate]], size: tuple[int, int], turn: Game.CaseSate=Game.CaseSate.PLAYER1) -> tuple[int, int]:
        """_summary_ Find the best solution for the next turn

        __description__ Find the best solution for the next turn by using the LET algorithm

        __param__ board: The board of the game (list[list[PLAYER1, PLAYER2, EMPTY]])
        __param__ size: The size of the board (tuple(x, y))

        __return__ tuple[int, int]: The best solution for the next turn
        """
###########################################################################################
        # bestVal: int = -1000
        # bestMove: tuple[int, int] = (-1, -1)
        # depth_limit: int = 2

        # for i in range(size[0]):
        #     for j in range(size[1]):
        #         if board[i][j] == Game.CaseSate.EMPTY:
        #             board[i][j] = Game.CaseSate.PLAYER1
        #             moveVal = Brain.minimax(board, size, depth_limit, False, -float('inf'), float('inf'))
        #             board[i][j] = Game.CaseSate.EMPTY

        #             if moveVal > bestVal:
        #                 bestMove = (i, j)
        #                 bestVal = moveVal

        # if (bestMove[0] == -1 and bestMove[1] == -1):
        #     for i in range(size[0]):
        #         for j in range(size[1]):
        #             if board[i][j] == Game.CaseSate.EMPTY:
        #                 bestMove = (i, j)
        #                 break
###########################################################################################
        board_data = ""
        for i in range(size[1]):
            for j in range(size[0]):
                board_data += str(board[i][j].value)
            board_data += " "
        try:
            result = subprocess.run(
                ['./let_ai', str(size[1]), str(size[0])] + board_data.split(),
                capture_output=True,
                timeout=Game.timeout_turn,
                text=True
            )
        except subprocess.TimeoutExpired:
            raise Game.End("PLAYER 1 - Brain Timeout", Game.End.EndType.LOSE)

        # Parse the output
        bestMove = tuple(map(int, result.stdout.split(',')))
###########################################################################################
        print(f"{bestMove[1]},{bestMove[0]}")
        return bestMove

    def sendCommand(self):
        # TODO: Send command to the protocol
        pass

    def end(self):
        # TODO: Terminate the brain
        pass
