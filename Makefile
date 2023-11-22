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

PYTHON	= python3

PIP		= pip3

OPTI		=	-Ofast -march=native -mtune=native -flto \
				-pipe -fomit-frame-pointer \
				-fno-stack-protector -fno-ident -fno-asynchronous-unwind-tables

all: $(NAME)

$(NAME):
	@$(ECHO) $(BOLD) $(GREEN)"\n► Gomoku 📦 !\n"$(DEFAULT)
	@gcc -o minmax ./src/ai/minmax.c $(OPTI)
	@cp ./src/main.py $(NAME)
	@chmod +x $(NAME)

clean:
	@$(RM) __pycache__
	@find . -name ".pytest_cache" -delete
	@find . -name ".mypy_cache" -delete
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "*~" -delete
	@find . -name "requirements.txt" -delete
	@(find . -type d -name "__pycache__" -exec rm -rf {} + 2> /dev/null || true)
	@-$(ECHO) $(BOLD) $(GREEN)✓$(LIGHT_BLUE)" CLEAN Gomoku 💨"$(DEFAULT)

fclean: clean
	@$(RM) $(NAME)
	@$(RM) minmax
	@-$(ECHO) $(BOLD) $(GREEN)✓$(LIGHT_BLUE)" FCLEAN Gomoku 🧻"$(DEFAULT)

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
