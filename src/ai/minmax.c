#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <limits.h>

typedef unsigned char u_my_type;

#define MAX_DEPTH 1
#define EMPTY (u_my_type)'0'
#define PLAYER (u_my_type)'1'
#define OPPONENT (u_my_type)'2'

typedef struct {
    unsigned size[2];
    u_my_type *board;
} board_t;

#define HEIGHT board->size[0]
#define WIDTH board->size[1]
#define AT(_board) _board->board[i * WIDTH + j]
#define AT_H(_offset) board->board[i * WIDTH + j + _offset]
#define AT_V(_offset) board->board[(i + _offset) * WIDTH + j]
#define AT_D(_offset) board->board[(i + _offset) * WIDTH + j + _offset]
#define AT_A(_offset) board->board[(i + _offset) * WIDTH + j - _offset]

// Define min, max functions
#define min(a,b) ((a) < (b) ? (a) : (b))
#define max(a,b) ((a) > (b) ? (a) : (b))

// Count consecutive pieces
int count_consecutive(board_t *board, unsigned i, unsigned j, u_my_type player, int di, int dj) {
    int count = 0;
    while (i >= 0 && i < HEIGHT && j >= 0 && j < WIDTH && AT(board) == player) {
        count++;
        i += di;
        j += dj;
    }
    return count;
}

// Check for a near-win condition for a player
bool is_near_win(board_t *board, u_my_type player) {
    for (unsigned i = 0; i < HEIGHT; i++) {
        for (unsigned j = 0; j < WIDTH; j++) {
            if (AT(board) == EMPTY) {
                // Check for horizontal win
                if (count_consecutive(board, i, j, player, 0, 1) >= 3) {
                    return true;
                }

                // Check for vertical win
                if (count_consecutive(board, i, j, player, 1, 0) >= 3) {
                    return true;
                }

                // Check for diagonal win
                if (count_consecutive(board, i, j, player, 1, 1) >= 3) {
                    return true;
                }

                // Check for anti-diagonal win
                if (count_consecutive(board, i, j, player, 1, -1) >= 3) {
                    return true;
                }
            }
        }
    }
    return false;
}

// Evaluation function
// Evaluation function
int evaluate(board_t *board) {
    int score = 0;
    const int WIN_SCORE = 1000000;
    const int FOUR_IN_A_ROW_SCORE = 500000;
    const int THREE_IN_A_ROW_SCORE = 10000;
    const int TWO_IN_A_ROW_SCORE = 100;

    for (unsigned i = 0; i < HEIGHT; i++) {
        for (unsigned j = 0; j < WIDTH; j++) {
            if (AT(board) == EMPTY)
                continue;

            // Check for immediate win for the player if so return win score
            if (is_near_win(board, PLAYER)) {
                return WIN_SCORE;
            }

            // Check for four in a row
            if ((j + 3 < WIDTH && AT(board) == AT_H(1) && AT(board) == AT_H(2) && AT(board) == AT_H(3)) ||
                (i + 3 < HEIGHT && AT(board) == AT_V(1) && AT(board) == AT_V(2) && AT(board) == AT_V(3)) ||
                (i + 3 < HEIGHT && j + 3 < WIDTH && AT(board) == AT_D(1) && AT(board) == AT_D(2) && AT(board) == AT_D(3)) ||
                (i + 3 < HEIGHT && j - 3 >= 0 && AT(board) == AT_A(1) && AT(board) == AT_A(2) && AT(board) == AT_A(3))) {
                score += (AT(board) == PLAYER ? FOUR_IN_A_ROW_SCORE : -FOUR_IN_A_ROW_SCORE);
            }

            // Check for three in a row
            if ((j + 2 < WIDTH && AT(board) == AT_H(1) && AT(board) == AT_H(2)) ||
                (i + 2 < HEIGHT && AT(board) == AT_V(1) && AT(board) == AT_V(2)) ||
                (i + 2 < HEIGHT && j + 2 < WIDTH && AT(board) == AT_D(1) && AT(board) == AT_D(2)) ||
                (i + 2 < HEIGHT && j - 2 >= 0 && AT(board) == AT_A(1) && AT(board) == AT_A(2))) {
                score += (AT(board) == PLAYER ? THREE_IN_A_ROW_SCORE : -THREE_IN_A_ROW_SCORE);
            }

            // Check for two in a row
            if ((j + 1 < WIDTH && AT(board) == AT_H(1)) ||
                (i + 1 < HEIGHT && AT(board) == AT_V(1)) ||
                (i + 1 < HEIGHT && j + 1 < WIDTH && AT(board) == AT_D(1)) ||
                (i + 1 < HEIGHT && j - 1 >= 0 && AT(board) == AT_A(1))) {
                score += (AT(board) == PLAYER ? TWO_IN_A_ROW_SCORE : -TWO_IN_A_ROW_SCORE);
            }

        }
    }

    return score;
}

// Minimax function with Alpha-Beta pruning
int minmax(board_t *board, unsigned depth, bool isMax, int alpha, int beta) {
    if (depth == 0) {
        return evaluate(board);
    }

    if (isMax) {
        int best = INT_MIN;
        for (unsigned i = 0; i < HEIGHT; i++) {
            for (unsigned j = 0; j < WIDTH; j++) {
                if (AT(board) == EMPTY) {
                    AT(board) = PLAYER; // Make the move
                    int val = minmax(board, depth - 1, false, alpha, beta);
                    AT(board) = EMPTY; // Undo the move
                    best = max(best, val);
                    alpha = max(alpha, val);
                    if (beta <= alpha) {
                        return best; // Prune the remaining branch
                    }
                }
            }
        }
        return best;
    } else {
        int best = INT_MAX;
        for (unsigned i = 0; i < HEIGHT; i++) {
            for (unsigned j = 0; j < WIDTH; j++) {
                if (AT(board) == EMPTY) {
                    AT(board) = OPPONENT; // Make the move
                    int val = minmax(board, depth - 1, true, alpha, beta);
                    AT(board) = EMPTY; // Undo the move
                    best = min(best, val);
                    beta = min(beta, val);
                    if (beta <= alpha) {
                        return best; // Prune the remaining branch
                    }
                }
            }
        }
        return best;
    }
}

int main(int ac, const char *av[]) {
    board_t *board = &(board_t) {
        .size = {(unsigned)atoi(av[1]), (unsigned)atoi(av[2])},
        .board = NULL
    };
    board->board = calloc(HEIGHT * WIDTH, sizeof(u_my_type));

    av = &av[3];
    for (unsigned i = 0; i < HEIGHT; i++)
        memcpy(&board->board[i * WIDTH], av[i], WIDTH);

    int best_move[2] = {-1, -1};
    int best_score = INT_MIN;
    int alpha = INT_MIN;
    int beta = INT_MAX;

    for (unsigned i = 0; i < HEIGHT; i++) {
        for (unsigned j = 0; j < WIDTH; j++) {
            if (AT(board) == EMPTY) {
                AT(board) = PLAYER; // AI makes a move
                int score = minmax(board, MAX_DEPTH, false, alpha, beta);
                AT(board) = EMPTY; // Undo the move
                if (score > best_score) {
                    best_score = score;
                    best_move[0] = (int)i;
                    best_move[1] = (int)j;
                }
            }
        }
    }

    if (best_move[0] == -1 && best_move[1] == -1) {
        for (unsigned i = 0; i < HEIGHT; i++) {
            for (unsigned j = 0; j < WIDTH; j++) {
                if (AT(board) == EMPTY) {
                    best_move[0] = (int)i;
                    best_move[1] = (int)j;
                    break;
                }
            }
            if (best_move[0] != -1) {
                break;
            }
        }
    }

    printf("%d,%d\n", best_move[0], best_move[1]);

    free(board->board);
    return 0;
}
