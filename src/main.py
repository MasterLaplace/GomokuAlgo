#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: main.py
# Author: MasterLaplace
# Created on: 2023-11-6

from protocol.command import Command
from game.game import Game
from ai.brain import Brain


if __name__ == "__main__":
    game = Game()
    brain = Brain()

    while True:
        try:
            Command.manage_command(game, brain, input("Please input command: "))
        except KeyboardInterrupt:
            print("\nUnplugging the brain")
            break
        except EOFError:
            print("")
