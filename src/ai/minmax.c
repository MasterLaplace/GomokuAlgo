/*
** EPITECH PROJECT, 2023
** B-AIA-500-REN-5-1-gomoku-enzo.monnier
** File description:
** minmax
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>

typedef unsigned char u_my_type;

#define MAX_DEPTH 2
#define EMPTY (u_my_type)'0'
#define PLAYER (u_my_type)'1'
#define OPPONENT (u_my_type)'2'

#define HEIGHT board->size[0]
#define WIDTH board->size[1]

typedef struct {
    unsigned size[2];
    u_my_type *board;
} board_t;

// bool type and values
#define bool _Bool
#define false 0
#define true 1

// min, max functions
#define typeof __typeof__
#define max(a,b) (a > b ? a : b)
#define min(a,b) (a < b ? a : b)

#define AT(_board) _board->board[i * WIDTH + j]
#define AT_H(_n) board->board[i * WIDTH + j + _n]
#define AT_V(_n) board->board[(i + _n) * WIDTH + j]
#define AT_D(_n) board->board[(i + _n) * WIDTH + j + _n]
#define AT_A(_n) board->board[(i + _n) * WIDTH + j - _n]
#define RET (10 << (AT(board) == PLAYER)) - (10 << (AT(board) == OPPONENT))

static bool isMovesLeft(board_t *board)
{
    for (unsigned i = 0; i < HEIGHT; i++)
        for (unsigned j = 0; j < WIDTH; j++)
            if (AT(board) == EMPTY)
                return true;
    return false;
}

static int evaluate(board_t *board) {
    for (int i = 0; i < (int)HEIGHT; i++) {
        for (int j = 0; j < (int)WIDTH; j++) {
            if (AT(board) == EMPTY)
                continue;

            if (j + 4 < (int)WIDTH && AT(board) == AT_H(1) && AT(board) == AT_H(2) && AT(board) == AT_H(3) && AT(board) == AT_H(4))
                return (AT(board) == PLAYER)?10:-10;

            if (i + 4 < (int)HEIGHT && AT(board) == AT_V(1) && AT(board) == AT_V(2) && AT(board) == AT_V(3) && AT(board) == AT_V(4))
                return (AT(board) == PLAYER)?10:-10;

            if (i + 4 < (int)HEIGHT && j + 4 < (int)WIDTH && AT(board) == AT_D(1) && AT(board) == AT_D(2) && AT(board) == AT_D(3) && AT(board) == AT_D(4))
                return (AT(board) == PLAYER)?10:-10;

            if (i + 4 < (int)HEIGHT && j - 4 >= 0 && AT(board) == AT_A(1) && AT(board) == AT_A(2) && AT(board) == AT_A(3) && AT(board) == AT_A(4))
                return (AT(board) == PLAYER)?10:-10;
        }
    }
    return 0;
}

static int minmax(board_t *board, unsigned depth, bool isMax, int albe[])
{
    int score = evaluate(board);

    if (!depth || score)
        return score;
    if (!isMovesLeft(board))
        return 0;
    int best = isMax ? -1000 : 1000;

    if (isMax) {
        for (unsigned i = 0; i < HEIGHT; i++)
            for (unsigned j = 0; j < WIDTH; j++)
                if (AT(board) == EMPTY) {
                    AT(board) = PLAYER;
                    best = max(best, minmax(board, depth - 1, !isMax, albe));
                    AT(board) = EMPTY;
                    albe[0] = max(albe[0], best);
                    if (albe[1] <= albe[0])
                        break;
                }
    } else {
        for (unsigned i = 0; i < HEIGHT; i++)
            for (unsigned j = 0; j < WIDTH; j++)
                if (AT(board) == EMPTY) {
                    AT(board) = OPPONENT;
                    best = min(best, minmax(board, depth - 1, !isMax, albe));
                    AT(board) = EMPTY;
                    albe[1] = min(albe[1], best);
                    if (albe[1] <= albe[0])
                        break;
                }
    }
    return best;
}

int main(int ac, const char *av[])
{
    board_t *board = &(board_t) {
        .size = {(unsigned)atoi(av[1]), (unsigned)atoi(av[2])},
        .board = NULL
    };
    board->board = calloc(HEIGHT * WIDTH, sizeof(u_my_type));

    av = &av[3];
    for (unsigned i = 0; i < HEIGHT; i++)
        memcpy(&board->board[i * WIDTH], av[i], WIDTH);
    board->board[WIDTH * HEIGHT] = '\0';

    int best_move[2] = {-1, -1};
    int best_score = -1000;
    int albe[2] = {-1000, 1000};

    for (unsigned i = 0; i < HEIGHT; i++)
        for (unsigned j = 0; j < WIDTH; j++) {
            if (AT(board) != EMPTY)
               continue;
            AT(board) = PLAYER;
            int score = minmax(board, MAX_DEPTH, false, albe);
            AT(board) = EMPTY;
            if (score > best_score) {
                best_score = score;
                best_move[0] = (int)i;
                best_move[1] = (int)j;
            }
        }

    if (best_move[0] == -1 && best_move[1] == -1)
        for (unsigned i = 0; i < HEIGHT; i++)
            for (unsigned j = 0; j < WIDTH; j++)
                if (AT(board) == EMPTY) {
                    best_move[0] = (int)i;
                    best_move[1] = (int)j;
                }

    printf("%d,%d\n", best_move[0], best_move[1]);
    return 0;
}
