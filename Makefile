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

all: $(NAME)

$(NAME):
	@$(ECHO) $(BOLD) $(GREEN)"\n► Gomoku 📦 !\n"$(DEFAULT)
	@ln -sf ./src/main.py $(NAME)

clean:
	@$(RM) __pycache__
	@find -type f -name ".pytest_cache" -delete
	@find -type f -name ".mypy_cache" -delete
	@find -type f -name "*.pyc" -delete
	@find -type f -name "*.pyo" -delete
	@find -type f -name "*~" -delete
	@find -type f -name "requirements.txt" -delete
	@-$(ECHO) $(BOLD) $(GREEN)✓$(LIGHT_BLUE)" CLEAN Gomoku 💨"$(DEFAULT)

fclean: clean
	@$(RM) $(NAME)
	@-$(ECHO) $(BOLD) $(GREEN)✓$(LIGHT_BLUE)" FCLEAN Gomoku 🧻"$(DEFAULT)

re: clean all

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