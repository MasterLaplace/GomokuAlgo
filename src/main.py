#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: main.py
# Author: MasterLaplace
# Created on: 2023-11-6

from protocol.command import Command
from game.game import Game
from ai.brain import Brain
import sys

if __name__ == "__main__":
    game = Game()
    brain = Brain()

    while True:
        try:
            command = input("Please input command: ")
            Command.manage_command(game, brain, command)
        except Game.End as e:
            print("END")
            print(e.message)
            game.end()
            brain.end()
        except KeyboardInterrupt:
            # print("\nUnplugging the brain")
            # break
            sys.exit(0)
        except EOFError:
            sys.exit(0)
