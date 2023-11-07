#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: game.py
# Author: MasterLaplace
# Created on: 2023-11-7

from enum import Enum

class Game:
    """_summary_ The game
    """

    class CaseSate(Enum):
        """_summary_ Enum for case state
        """
        EMPTY = 0
        PLAYER1 = 1
        PLAYER2 = 2

    class Error(Exception):
        """_summary_ Base class for other exceptions
        """

        def __init__(self, message: str):
            self.message = message
            super().__init__(self.message)

    def __init__(self):
        self.__board: list[list[Game.CaseSate]] = []
        self.__turn: Game.CaseSate = Game.CaseSate.PLAYER1
        self.__started: bool = False
        self.__size: tuple[int, int] = (0, 0)
        self.nb_turn: int = 0
        self.logs: list[tuple(int, Game.CaseSate, int, int)] = []

    def getCopyBoard(self) -> list[list[int]]:
        if not self.__started:
            raise Game.Error("Game is not started")
        return self.__board.copy()

    def getSize(self) -> tuple[int, int]:
        if not self.__started:
            raise Game.Error("Game is not started")
        return self.__size

    def getTurn(self) -> CaseSate:
        if not self.__started:
            raise Game.Error("Game is not started")
        return self.__turn

    def getInfo(self, key: str, value: str):
        pass

    def setBoard(self, board: list[list[int]]):
        if not self.__started:
            raise Game.Error("Game is not started")
        self.__board = board

    def setTurn(self, turn: CaseSate):
        if not self.__started:
            raise Game.Error("Game is not started")
        self.nb_turn += 1
        self.__turn = turn

    def start(self, size: int):
        if  self.__started:
            raise Game.Error("Game is already started")
        self.__size = (size, size)
        self.__board = [[Game.CaseSate.EMPTY for _ in range(size)] for _ in range(size)]
        self.__started = True

    def rectstart(self, width: int, height: int):
        if  self.__started:
            raise Game.Error("Game is already started")
        self.__size = width
        self.__board = [[Game.CaseSate.EMPTY for _ in range(width)] for _ in range(height)]
        self.__started = True

    def restart(self):
        if not self.__started:
            raise Game.Error("Game is not started")
        self.__board = [[Game.CaseSate.EMPTY for _ in range(self.__size[0])] for _ in range(self.__size[1])]
        self.__turn = Game.CaseSate.PLAYER1
        self.nb_turn = 0
        self.logs = []

    def turn(self, x: int, y: int):
        if not self.__started:
            raise Game.Error("Game is not started")
        if self.__board[x][y] == Game.CaseSate.EMPTY:
            self.__board[x][y] = self.__turn
            self.logs.append((self.nb_turn, self.__turn, x, y))
            self.nb_turn += 1
            self.__turn = Game.CaseSate.PLAYER1 if self.__turn == Game.CaseSate.PLAYER2 else Game.CaseSate.PLAYER2
        else:
            print("ERROR message - field is not empty")
            raise Game.Error("Field is not empty")

    def begin(self, x: int, y: int):
        if self.nb_turn == 0:
            self.__board[x][y] = Game.CaseSate.PLAYER2
            self.logs.append((self.nb_turn, Game.CaseSate.PLAYER2, x, y))
            self.nb_turn = 1
            self.__turn = Game.CaseSate.PLAYER1
        else:
            print("ERROR message - game has already started")
            raise Game.Error("Game has already started")

    def is_end(self) -> CaseSate:
        """_summary_ Check if the game is ended

        __desciption__ Check if the game is ended by checking if there is a 5-in-a-row

        __return__ CaseSate: The state of the game (EMPTY, PLAYER1, PLAYER2)
        EMPTY: The game is not ended
        PLAYER1: The game is ended and the player 1 won
        PLAYER2: The game is ended and the player 2 won
        """
        for i in range(0, self.__size[0] - 4):
            for j in range(0, self.__size[1] - 4):
                # check horizontal
                if self.__board[i][j] != Game.CaseSate.EMPTY:
                    if self.__board[i][j] == self.__board[i][j + 1] == self.__board[i][j + 2] == self.__board[i][j + 3] == self.__board[i][j + 4]:
                        return Game.CaseSate.PLAYER1 if self.__board[i][j] == 1 else Game.CaseSate.PLAYER2
                # check vertical
                if self.__board[i][j] != Game.CaseSate.EMPTY:
                    if self.__board[i][j] == self.__board[i + 1][j] == self.__board[i + 2][j] == self.__board[i + 3][j] == self.__board[i + 4][j]:
                        return Game.CaseSate.PLAYER1 if self.__board[i][j] == 1 else Game.CaseSate.PLAYER2
                # check diagonal
                if self.__board[i][j] != Game.CaseSate.EMPTY:
                    if self.__board[i][j] == self.__board[i + 1][j + 1] == self.__board[i + 2][j + 2] == self.__board[i + 3][j + 3] == self.__board[i + 4][j + 4]:
                        return Game.CaseSate.PLAYER1 if self.__board[i][j] == 1 else Game.CaseSate.PLAYER2
        return Game.CaseSate.EMPTY

    def undo(self):
        if self.nb_turn == 0:
            raise Game.Error("Game has not started")
        self.nb_turn -= 1
        self.__turn = Game.CaseSate.PLAYER1 if self.__turn == Game.CaseSate.PLAYER2 else Game.CaseSate.PLAYER2
        self.__board[self.logs[self.nb_turn][2]][self.logs[self.nb_turn][3]] = Game.CaseSate.EMPTY
        self.logs.pop()

    def end(self):
        """_summary_ End the game
        """
        self.__started = False
        self.__board = []
        self.__turn = Game.CaseSate.PLAYER1
        self.nb_turn = 0
        self.logs = []
