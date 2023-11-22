#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: command.py
# Author: MasterLaplace
# Created on: 2023-11-6

from game.game import Game
from ai.brain import Brain

import re

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
                    print("HELP")
                case "START": # [size]
                    Command.start(game, brain, int(command_tab[1]))
                case "TURN": # [x] [y]
                    Command.turn(game, brain, int(command_tab[1]), int(command_tab[2]))
                case "BEGIN":
                    Command.begin(game, brain)
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
                    Command.rectstart(int(command_tab[1]), int(command_tab[2]))
                case "RESTART":
                    Command.restart(game, brain)
                case "TAKEBACK":
                    Command.takeback(game, brain)
                case "PLAY":
                    print("PLAY")
                case "SWAP2BOARD":
                    print("SWAP2BOARD")
                # Commands that are sent by the brain
                case "UNKNOWN":
                    print("UNKNOWN")
                case "ERROR":
                    print("ERROR")
                case "MESSAGE":
                    print("MESSAGE")
                case "DEBUG":
                    print("DEBUG")
                case "SUGGEST": # [x] [y]
                    print(f"SUGGEST {command_tab[1]},{command_tab[2]}")
                # Error commands
                case _:
                    print("ERROR Unknown command")
                    print("Please input HELP to get more information")
        except IndexError:
            print("ERROR Invalid command")
            print("Please input HELP to get more information")
        except ValueError:
            print("ERROR Invalid command")
            print("Please input HELP to get more information")
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
                raise Game.End("PLAYER 2", Game.End.EndType.WIN)
            raise Game.Error(error.message)
        width, height = game.getSize()
        if game.nb_turn > 8:
            if game.is_end() == Game.CaseSate.PLAYER1:
                Command.end(game, brain)
                Command.start(game, brain, width)
                raise Game.End("PLAYER 1", Game.End.EndType.WIN)

        try:
            x, y = brain.findBestSolution(game.getCopyBoard(), game.getSize())
            game.turn(x, y)
            if game.nb_turn > 8:
                if game.is_end() == Game.CaseSate.PLAYER2:
                    Command.end(game, brain)
                    Command.start(game, brain, width)
                    raise Game.End("PLAYER 2", Game.End.EndType.WIN)
            return x, y
        except Game.Error as error:
            print(f"ERROR message - {error.message}")
            if error.error_type == Game.Error.ErrorType.FORBIDEN:
                raise Game.End("PLAYER 1", Game.End.EndType.WIN)
            raise Game.Error(error.message)

    @staticmethod
    def begin(game: Game, brain: Brain):
        try:
            x, y = brain.findBestSolution(game.getCopyBoard(), game.getSize())
            game.begin(x, y)
        except Game.Error as error:
            print(f"ERROR message - {error.message}")

    @staticmethod
    def board(game: Game, brain: Brain):
        try:
            board = game.getCopyBoard()
            player = Game.CaseSate(0)
            while True:
                command = input("BOARD until DONE: ")
                if command == "DONE":
                    game.setBoard(board)
                    if player == Game.CaseSate.PLAYER1:
                        Command.turn(game, brain, 0, 0)
                    else:
                        Command.begin(game, brain)
                    break
                command_tab = [item for item in re.split(r'[ \t,]', command) if item != '']
                try:
                    player = Game.CaseSate(int(command_tab[2]))
                    if player == Game.CaseSate.EMPTY or player == game.getTurn():
                        raise ValueError
                    board[int(command_tab[0])][int(command_tab[1])] = player
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
        pass

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
    def takeback(game: Game, brain: Brain):
        game.undo()
