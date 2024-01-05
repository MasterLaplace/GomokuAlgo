##
## EPITECH PROJECT, 2023
## Title: Gomoku v0.0.1
## Author: MasterLaplace
## Created: 2023-11-07
## File description:
## Makefile
##

-include .env
export

NAME	= pbrain-gomoku-ai
WIN_NAME = pbrain-gomoku-ai.exe

PYTHON	= python3
PIP		= pip3

CC_LINUX = gcc
CC_WIN   = x86_64-w64-mingw32-gcc

OPTI		=	-Ofast -march=native -mtune=native -flto \
				-pipe -fomit-frame-pointer \
				-fno-stack-protector -fno-ident -fno-asynchronous-unwind-tables

all: linux

linux:
	@echo "Building for Linux..."
	@$(CC_LINUX) -o let_ai ./src/ai/let_ai.c $(OPTI)
	@$(CC_LINUX) -o minmax_ai ./src/ai/minmax_ai.c $(OPTI)
	@cp ./src/main.py $(NAME)
	@chmod +x $(NAME)

windows:
	@$(PIP) install pyinstaller
	@sudo dnf install mingw64-gcc
	@echo "Building for Windows..."
	@$(CC_WIN) -o let_ai.exe ./src/ai/let_ai.c $(OPTI)
	@$(PYTHON) -m PyInstaller --onefile ./src/main.py --name $(WIN_NAME)

clean:
	@$(RM) __pycache__
	@find . -name ".pytest_cache" -delete
	@find . -name ".mypy_cache" -delete
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "*~" -delete
	@find . -name "requirements.txt" -delete
	@(find . -type d -name "__pycache__" -exec rm -rf {} + 2> /dev/null || true)
	@rm -rf build dist $(WIN_NAME).spec $(WIN_NAME)

fclean: clean
	@$(RM) $(NAME)
	@$(RM) let_ai
	@rm -f $(NAME) let_ai let_ai.exe

re: fclean all

## HELP MODE

help:
	@$(ECHO) $(BOLD) $(GREEN)"\n► GOMOKU HELP 📖 !\n"$(DEFAULT)
	@$(ECHO) $(BOLD) $(LIGHT_BLUE)"► make install 📦 !"$(DEFAULT)
	@$(ECHO) $(BOLD) $(LIGHT_BLUE)"► make lint 📦 !"$(DEFAULT)
	@$(ECHO) $(BOLD) $(LIGHT_BLUE)"► make type 📦 !"$(DEFAULT)
	@$(ECHO) $(BOLD) $(LIGHT_BLUE)"► make clean 🧹 !"$(DEFAULT)
	@$(ECHO) $(BOLD) $(LIGHT_BLUE)"► make fclean 🧹 !"$(DEFAULT)
	@$(ECHO) $(BOLD) $(LIGHT_BLUE)"► make re 🧹 !"$(DEFAULT)
	@$(ECHO) $(BOLD) $(LIGHT_BLUE)"► make help: Show this help 📜"$(DEFAULT)
	@$(ECHO) $(BOLD) $(LIGHT_BLUE)"► make version: Show the version of Gomoku 📜 !"$(DEFAULT)

version:
	@$(ECHO) $(BOLD) $(GREEN)"\n► GOMOKU VERSION 📜 !"$(DEFAULT)
	@$(ECHO) $(BOLD) $(LIGHT_BLUE)"\n► Gomoku: $(shell cat VERSION)"$(DEFAULT)

.PHONY: all clean
