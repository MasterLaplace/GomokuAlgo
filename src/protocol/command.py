#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: command.py
# Author: MasterLaplace
# Created on: 2023-11-6

from src.game.game import Game
from src.ai.brain import Brain

import re
from random import randint

class Command:
    """_summary_ Parse the command from the protocol and call the corresponding function
    _description_ The command is parsed and the corresponding function is called
    """

    @staticmethod
    def manage_command(game: Game, brain: Brain, command: str) -> int:
        command_tab = [item for item in re.split(r'[ \t,=]', command) if item != '']

        try:
            if not command_tab:
                return
            match command_tab[0]:
                # Mandatory commands
                case "HELP":
                    print("HELP: Display this help")
                    print("START [size]: Start a new game with a board of size [size]x[size]")
                    print("TURN [x] [y]: Play on the case [x] [y]")
                    print("BEGIN: Let the brain play")
                    print("BOARD: Display the board")
                    print("INFO [key] [value]: Set the info [key] to [value]")
                    print("END: End the game")
                    print("ABOUT: Display information about the brain")
                    print("RECTSTART [width] [height]: Start a new game with a board of size [width]x[height]")
                    print("RESTART: Restart the game")
                    print("TAKEBACK: Takeback the last move")
                    print("PLAY: Play a move")
                    print("SWAP2BOARD: Swap the board")
                    print("DEBUG_BOARD: Display the board in debug mode")
                case "START": # [size]
                    Command.start(game, brain, int(command_tab[1]))
                case "TURN": # [x] [y]
                    Command.turn(game, brain, int(command_tab[1]), int(command_tab[2]))
                case "BEGIN":
                    Command.begin(game)
                case "BOARD":
                    Command.board(game, brain)
                case "INFO": # [key] [value]
                    Command.info(command_tab[1], command_tab[2])
                case "END":
                    Command.end(game, brain)
                case "ABOUT":
                    Command.about(brain)
                # Optional commands
                case "RECTSTART":
                    Command.rectstart(game, brain, int(command_tab[1]), int(command_tab[2]))
                case "RESTART":
                    Command.restart(game, brain)
                case "TAKEBACK":
                    Command.takeback(game)
                case "PLAY":
                    print("PLAY")
                case "SWAP2BOARD":
                    print("SWAP2BOARD")
                # Error commands
                case _:
                    print("UNKNOWN - HELP to get more information")
        except IndexError:
            print("ERROR Invalid command - HELP to get more information")
        except ValueError:
            print("ERROR Invalid command - HELP to get more information")
        except Game.Error as error:
            print(f"ERROR message - {error.message}")

    @staticmethod
    def start(game: Game, brain: Brain, size: int):
        if 4 < size < 31:
            try:
                game.start(size)
                brain.start()
            except Game.Error as error:
                print(f"ERROR message - {error.message}")
        else:
            print("ERROR message - unsupported size or other error")

    @staticmethod
    def turn(game: Game, brain: Brain, x: int, y: int) -> tuple[int, int]:
        try:
            game.turn(x, y)
        except Game.Error as error:
            print(f"ERROR message - {error.message}")
            if error.error_type == Game.Error.ErrorType.FORBIDEN:
                raise Game.End("PLAYER 1", Game.End.EndType.LOSE)
            raise Game.Error(error.message)
        width, _ = game.getSize()
        if game.nb_turn > 8:
            if game.is_end(Game.CaseSate.PLAYER1):
                Command.end(game, brain)
                Command.start(game, brain, width)
                raise Game.End("PLAYER 1", Game.End.EndType.WIN)

        try:
            y, x = brain.findBestSolution(game.getCopyBoard(), game.getSize())
            game.turn(x, y)
            if game.nb_turn > 8:
                if game.is_end(Game.CaseSate.PLAYER2):
                    Command.end(game, brain)
                    Command.start(game, brain, width)
                    raise Game.End("PLAYER 1", Game.End.EndType.LOSE)
            return x, y
        except Game.Error as error:
            print(f"ERROR message - {error.message}")
            if error.error_type == Game.Error.ErrorType.FORBIDEN:
                raise Game.End("PLAYER 1", Game.End.EndType.WIN)
            raise Game.Error(error.message)

    @staticmethod
    def begin(game: Game):
        try:
            width, height = game.getSize()
            x = randint(0, width - 1)
            y = randint(0, height - 1)
            game.begin(x, y)
            print(f"{x},{y}")
        except Game.Error as error:
            print(f"ERROR message - {error.message}")

    @staticmethod
    def board(game: Game, brain: Brain):
        try:
            board = game.getCopyBoard()
            player = Game.CaseSate.EMPTY
            while True:
                command = input()
                if command == "DONE":
                    game.setBoard(board)
                    if player == Game.CaseSate.PLAYER2:
                        Command.begin(game, brain)
                    break
                command_tab = [item for item in re.split(r'[ \t,=]', command) if item != '']
                try:
                    player = Game.CaseSate(int(command_tab[2]))
                    if player == Game.CaseSate.EMPTY or player != game.getTurn():
                        raise ValueError
                    board[int(command_tab[1])][int(command_tab[0])] = player
                    game.setTurn(player)
                except IndexError:
                    print("ERROR Invalid command")
                    continue
                except ValueError:
                    print("ERROR Invalid value command")
                    continue
        except Game.Error as error:
            print(f"ERROR message - {error.message}")

    @staticmethod
    def info(key: str, value: str):
        if (key == "timeout_turn"):
            Game.timeout_turn = int(value) / 1000
        elif (key == "timeout_match"):
            Game.timeout_match = int(value)
        elif (key == "max_memory"):
            Game.max_memory = int(value)
        elif (key == "time_left"):
            Game.time_left = int(value)
        elif (key == "game_type"):
            Game.game_type = int(value)
        elif (key == "rule"):
            Game.rule = int(value)
        elif (key == "evaluate"):
            Game.evaluate = int(value)
        elif (key == "folder"):
            Game.folder = value
            
    @staticmethod
    def end(game: Game, brain: Brain):
        game.end()
        brain.end()
        quit()

    @staticmethod
    def about(brain: Brain):
        brain.about()

    @staticmethod
    def rectstart(game: Game, brain: Brain, width: int, height: int):
        if 4 < width != height < 31:
            try:
                game.rectstart(width, height)
                brain.start()
            except Game.Error as error:
                print(f"ERROR message - {error.message}")
        else:
            print("ERROR message - rectangular board is not supported or other error")

    @staticmethod
    def restart(game: Game, brain: Brain):
        game.restart()
        brain.restart()

    @staticmethod
    def takeback(game: Game):
        game.undo()
