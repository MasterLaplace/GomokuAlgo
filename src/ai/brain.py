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
        return Game.CaseSate.EMPTY

    @staticmethod
    def minimax(board: list[list[str]], size: tuple[int, int], depth: int, isMax: bool, opponent: Game.CaseSate) -> int:
        score = Brain.evaluate(board, size)

        if score == Game.CaseSate.PLAYER1:
            return 10
        if score == Game.CaseSate.PLAYER2:
            return -10
        if not Brain.isMovesLeft(board, size):
            return 0

        opponent_positions = Brain.getOpponentPositions(board, size, opponent)

        if isMax:
            best = -1000
            for i in range(0, size[0]):
                for j in range(0, size[1]):
                    if board[i][j] == Game.CaseSate.EMPTY:
                        board[i][j] = Game.CaseSate.PLAYER2
                        moveVal = Brain.minimax(board, size, depth + 1, not isMax, opponent)

                        for pos in opponent_positions:
                            if pos[0] == i or pos[1] == j or abs(pos[0] - i) == abs(pos[1] - j):
                                moveVal += 1

                        board[i][j] = Game.CaseSate.EMPTY
                        best = max(best, moveVal)
            return best
        else:
            best = 1000
            for i in range(0, size[0]):
                for j in range(0, size[1]):
                    if board[i][j] == Game.CaseSate.EMPTY:
                        board[i][j] = Game.CaseSate.PLAYER2
                        moveVal = Brain.minimax(board, size, depth + 1, not isMax, opponent)

                        for pos in opponent_positions:
                            if pos[0] == i or pos[1] == j or abs(pos[0] - i) == abs(pos[1] - j):
                                moveVal -= 1

                        board[i][j] = Game.CaseSate.EMPTY
                        best = min(best, moveVal)
            return best

    def findBestSolution(self, board: list[list[Game.CaseSate]], size: tuple[int, int]) -> tuple[int, int]:
        bestVal = -1000
        bestMove = (-1, -1)

        opponent = Game.CaseSate.PLAYER2

        for i in range(size[0]):
            for j in range(size[1]):
                if board[i][j] == Game.CaseSate.EMPTY:
                    board[i][j] = Game.CaseSate.PLAYER1
                    moveVal = Brain.minimax(board, size, 0, False, opponent)
                    board[i][j] = Game.CaseSate.EMPTY

                    if moveVal > bestVal:
                        bestMove = (i, j)
                        bestVal = moveVal

        print(f"{bestMove[0]},{bestMove[1]}")
        return bestMove

    @staticmethod
    def getOpponentPositions(board: list[list[Game.CaseSate]], size: tuple[int, int], opponent: Game.CaseSate) -> list[tuple[int, int]]:
        positions = []
        for i in range(size[0]):
            for j in range(size[1]):
                if board[i][j] == opponent:
                    positions.append((i, j))
        return positions
    
    def sendCommand(self):
        # TODO: Send command to the protocol
        pass

    def end(self):
        # TODO: Terminate the brain
        pass