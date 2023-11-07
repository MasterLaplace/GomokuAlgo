#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: brain.py
# Author: MasterLaplace
# Created on: 2023-11-7

from random import randint
from enum import Enum

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
        self.name = "SomeBrain"
        self.version = "0.0.1"
        self.author = "MasterLaplace;M7T5M3P"
        self.country = "France"

    def start(self):
        print("OK - everything is good")
        # TODO: Initialize the brain

    def restart(self):
        # TODO: Restart the brain
        pass

    def about(self):
        print(f"name=\"{self.name}\", version=\"{self.version}\", author=\"{self.author}\", country=\"{self.country}\"")

    def findBestSolution(self, board: list[list[int]], size: tuple[int, int]) -> tuple[int, int]:
        """_summary_ Find the best solution for the next turn

        __description__ Find the best solution for the next turn by using the minimax algorithm

        __param__ board: The board of the game (list[list[PLAYER1, PLAYER2, EMPTY]])
        __param__ size: The size of the board (tuple(x, y))

        __return__ tuple[int, int]: The best solution for the next turn
        """
        x, y = randint(0, size[0] - 1), randint(0, size[1] - 1)
        print(f"{x},{y}")
        return (x, y)

    def sendCommand(self):
        # TODO: Send command to the protocol
        pass

    def end(self):
        # TODO: Terminate the brain
        pass
