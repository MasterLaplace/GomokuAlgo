#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: main.py
# Author: MasterLaplace
# Created on: 2023-11-6

from src.protocol.command import Command
from src.game.game import Game
from src.ai.brain import Brain

import sys

if __name__ == "__main__":
    game = Game()
    brain = Brain()

    if len(sys.argv) == 2 and sys.argv[1] == "debug":
        try:
            from src.board.board import BoardGame
            BoardGame(game, brain, auto_train=True)
        except KeyboardInterrupt:
            print("\nMESSAGE Unplugging the brain")
    else:
        while True:
            try:
                Command.manage_command(game, brain, input())
            except Game.End as e:
                print(f"MESSAGE {e.message}")
                game.end()
                brain.end()
            except KeyboardInterrupt:
                print("\nMESSAGE Unplugging the brain")
                quit()
            except EOFError:
                quit()
