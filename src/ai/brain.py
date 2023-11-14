#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: brain.py
# Author: MasterLaplace;Enzotekrennes
# Created on: 2023-11-7

from enum import Enum
from game.game import Game

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


    def findBestSolution(self, board: list[list[Game.CaseSate]], size: tuple[int, int]) -> tuple[int, int]:
        """_summary_ Find the best solution for the next turn

        __description__ Find the best solution for the next turn by using the minimax algorithm

        __param__ board: The board of the game (list[list[PLAYER1, PLAYER2, EMPTY]])
        __param__ size: The size of the board (tuple(x, y))

        __return__ tuple[int, int]: The best solution for the next turn
        """
        board_data = ""
        for i in range(size[0]):
            for j in range(size[1]):
                board_data += str(board[i][j].value)
            board_data += " "
        result = subprocess.run(
            ['./minmax', str(size[0]), str(size[1])] + board_data.split(),
            capture_output=True,
            timeout=5,
            text=True
        )

        # Parse the output
        bestMove = tuple(map(int, result.stdout.split(',')))
        print(f"{bestMove[0]},{bestMove[1]}")
        return bestMove

    def sendCommand(self):
        # TODO: Send command to the protocol
        pass

    def end(self):
        # TODO: Terminate the brain
        pass
