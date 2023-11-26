/*
** EPITECH PROJECT, 2023
** B-AIA-500-REN-5-1-gomoku-enzo.monnier
** File description:
** Laplacian Expanded Tree (LET) AI
*/

#include <stdio.h> // printf
#include <stdlib.h> // atoi calloc
#include <string.h> // memcpy

typedef unsigned char uint8_t;

#define EMPTY (uint8_t)'0'
#define PLAYER (uint8_t)'1'
#define OPPONENT (uint8_t)'2'

// bool type and values
#define bool _Bool
#define false 0
#define true 1

#define AT(_board) _board[i * width + j]
#define AT_H(_n) board[i * width + j + _n]
#define AT_V(_n) board[(i + _n) * width + j]
#define AT_D(_n) board[(i + _n) * width + j + _n]
#define AT_A(_n) board[(i + _n) * width + j - _n]

#define DEBUG

/**
 * @brief  main function of the ai.
 *
 * @note   the best move is printed on stdout "x,y\n".
 * @note   complete log is written in let.log.
 * @note   complexity: O(n*rules) with n = height * width and rules = 4 * 8 * 2 = 64
 *
 * @example ./let_ai 5 5 00000 00000 00000 00000 00000
 *
 * @details 1. check if ai can win in 1 move
 *          2. check if ai can loose in 1 move (block)
 *          3. check if ai can loose in 2*2 moves (block)
 *          4. check if ai can loose in 2 moves (block) by block check
 *          5. check if ai can win in 2 moves do it
 *          6. check if ai can win in 3 moves do it
 *
 * @param ac  number of arguments (unused)
 * @param av  arguments {height, width, board}
 * @return int 0 if ok, 1 if error
 */
int main(int ac, const char *av[])
{
    int height = atoi(av[1]);
    int width = atoi(av[2]);
    uint8_t *board = calloc(height * width, sizeof(uint8_t));
#if defined(__STDC__) && defined(__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    register int i = 0;
    register int j = 0;
    register uint8_t me = 0;
    register uint8_t sum = 0;
    register uint8_t sum2 = 0;
#else
    int i = 0;
    int j = 0;
    uint8_t me = 0;
    uint8_t sum = 0;
    uint8_t sum2 = 0;
#endif

#ifdef DEBUG
    FILE * restrict log_file = fopen("let.log", "w+");
    if (log_file == NULL)
        return 1;
    fprintf(log_file, "[LOG]: Running LET AI\n");
    fprintf(log_file, "[LOG]: height: %d, width: %d\n", height, width);
#endif

    av = &av[3];
    for (; i < height; ++i)
        memcpy(&board[i * width], av[i], width);

    // if ai can win in 1 move do it
#ifdef DEBUG
    fprintf(log_file, "[LOG]: 1 (do it)\n[\n");
#endif
    for (i = 0; i < height; ++i) {
    #ifdef DEBUG
        fprintf(log_file, "    [ ");
    #endif
        for (j = 0; j < width; ++j) {
            me = AT(board);

            //* horizontal check *//
            // if 1 1 1 1 0
            if (j + 4 < width && me == OPPONENT && me == AT_H(1) && me == AT_H(2) && me == AT_H(3) && EMPTY == AT_H(4))
                return !printf("%d,%d\n", i, j + 4);

            // or 1 1 0 1 1
            if (j + 4 < width && me == OPPONENT && me == AT_H(1) && EMPTY == AT_H(2) && me == AT_H(3) && me == AT_H(4))
                return !printf("%d,%d\n", i, j + 2);

            // or 1 0 1 1 1
            if (j + 4 < width && me == OPPONENT && EMPTY == AT_H(1) && me == AT_H(2) && me == AT_H(3) && me == AT_H(4))
                return !printf("%d,%d\n", i, j + 1);

            // or 1 1 1 0 1
            if (j + 4 < width && me == OPPONENT && me == AT_H(1) && me == AT_H(2) && EMPTY == AT_H(3) && me == AT_H(4))
                return !printf("%d,%d\n", i, j + 3);

            // or 0 1 1 1 1
            if (j + 4 < width && EMPTY == me && OPPONENT == AT_H(1) && OPPONENT == AT_H(2) && OPPONENT == AT_H(3) && OPPONENT == AT_H(4))
                return !printf("%d,%d\n", i, j);

            //* vertical check *//
            // if 1 1 1 1 0
            if (i + 4 < height && me == OPPONENT && me == AT_V(1) && me == AT_V(2) && me == AT_V(3) && EMPTY == AT_V(4))
                return !printf("%d,%d\n", i + 4, j);

            // or 1 1 0 1 1
            if (i + 4 < height && me == OPPONENT && me == AT_V(1) && EMPTY == AT_V(2) && me == AT_V(3) && me == AT_V(4))
                return !printf("%d,%d\n", i + 2, j);

            // or 1 0 1 1 1
            if (i + 4 < height && me == OPPONENT && EMPTY == AT_V(1) && me == AT_V(2) && me == AT_V(3) && me == AT_V(4))
                return !printf("%d,%d\n", i + 1, j);

            // or 1 1 1 0 1
            if (i + 4 < height && me == OPPONENT && me == AT_V(1) && me == AT_V(2) && EMPTY == AT_V(3) && me == AT_V(4))
                return !printf("%d,%d\n", i + 3, j);

            // or 0 1 1 1 1
            if (i + 4 < height && EMPTY == me && OPPONENT == AT_V(1) && OPPONENT == AT_V(2) && OPPONENT == AT_V(3) && OPPONENT == AT_V(4))
                return !printf("%d,%d\n", i, j);

            //* diagonal check *//
            // if 1 1 1 1 0
            if (i + 4 < height && j + 4 < width && me == OPPONENT && me == AT_D(1) && me == AT_D(2) && me == AT_D(3) && EMPTY == AT_D(4))
                return !printf("%d,%d\n", i + 4, j + 4);

            // or 1 1 0 1 1
            if (i + 4 < height && j + 4 < width && me == OPPONENT && me == AT_D(1) && EMPTY == AT_D(2) && me == AT_D(3) && me == AT_D(4))
                return !printf("%d,%d\n", i + 2, j + 2);

            // or 1 0 1 1 1
            if (i + 4 < height && j + 4 < width && me == OPPONENT && EMPTY == AT_D(1) && me == AT_D(2) && me == AT_D(3) && me == AT_D(4))
                return !printf("%d,%d\n", i + 1, j + 1);

            // or 1 1 1 0 1
            if (i + 4 < height && j + 4 < width && me == OPPONENT && me == AT_D(1) && me == AT_D(2) && EMPTY == AT_D(3) && me == AT_D(4))
                return !printf("%d,%d\n", i + 3, j + 3);

            // or 0 1 1 1 1
            if (i + 4 < height && j + 4 < width && EMPTY == me && OPPONENT == AT_D(1) && OPPONENT == AT_D(2) && OPPONENT == AT_D(3) && OPPONENT == AT_D(4))
                return !printf("%d,%d\n", i, j);

            //* anti-diagonal check *//
            // if 1 1 1 1 0
            if (i + 4 < height && j - 4 >= 0 && me == OPPONENT && me == AT_A(1) && me == AT_A(2) && me == AT_A(3) && EMPTY == AT_A(4))
                return !printf("%d,%d\n", i + 4, j - 4);

            // or 1 1 0 1 1
            if (i + 4 < height && j - 4 >= 0 && me == OPPONENT && me == AT_A(1) && EMPTY == AT_A(2) && me == AT_A(3) && me == AT_A(4))
                return !printf("%d,%d\n", i + 2, j - 2);

            // or 1 0 1 1 1
            if (i + 4 < height && j - 4 >= 0 && me == OPPONENT && EMPTY == AT_A(1) && me == AT_A(2) && me == AT_A(3) && me == AT_A(4))
                return !printf("%d,%d\n", i + 1, j - 1);

            // or 1 1 1 0 1
            if (i + 4 < height && j - 4 >= 0 && me == OPPONENT && me == AT_A(1) && me == AT_A(2) && EMPTY == AT_A(3) && me == AT_A(4))
                return !printf("%d,%d\n", i + 3, j - 3);

            // or 0 1 1 1 1
            if (i + 4 < height && j - 4 >= 0 && EMPTY == me && OPPONENT == AT_A(1) && OPPONENT == AT_A(2) && OPPONENT == AT_A(3) && OPPONENT == AT_A(4))
                return !printf("%d,%d\n", i, j);

#ifdef DEBUG
            fprintf(log_file, "%c ", me);
        }
        fprintf(log_file, "]\n");
    }
    fprintf(log_file, "]\n");
#else
        }
    } // end of for loops
#endif

    // if ai can loose in 1 move (block)
#ifdef DEBUG
    fprintf(log_file, "[LOG]: 1 (block)\n[\n");
#endif
    for (i = 0; i < height; ++i) {
    #ifdef DEBUG
        fprintf(log_file, "    [ ");
    #endif
        for (j = 0; j < width; ++j) {
            me = AT(board);

            //* horizontal check *//
            // if 1 1 1 1 0
            if (j + 4 < width && me == PLAYER && me == AT_H(1) && me == AT_H(2) && me == AT_H(3) && EMPTY == AT_H(4))
                return !printf("%d,%d\n", i, j + 4);

            // or 1 1 0 1 1
            if (j + 4 < width && me == PLAYER && me == AT_H(1) && EMPTY == AT_H(2) && me == AT_H(3) && me == AT_H(4))
                return !printf("%d,%d\n", i, j + 2);

            // or 1 0 1 1 1
            if (j + 4 < width && me == PLAYER && EMPTY == AT_H(1) && me == AT_H(2) && me == AT_H(3) && me == AT_H(4))
                return !printf("%d,%d\n", i, j + 1);

            // or 1 1 1 0 2
            if (j + 4 < width && me == PLAYER && me == AT_H(1) && me == AT_H(2) && EMPTY == AT_H(3) && me == AT_H(4))
                return !printf("%d,%d\n", i, j + 3);

            // or 0 1 1 1 1
            if (j + 4 < width && EMPTY == me && PLAYER == AT_H(1) && PLAYER == AT_H(2) && PLAYER == AT_H(3) && PLAYER == AT_H(4))
                return !printf("%d,%d\n", i, j);

            //* vertical check *//
            // if 1 1 1 1 0
            if (i + 4 < height && me == PLAYER && me == AT_V(1) && me == AT_V(2) && me == AT_V(3) && EMPTY == AT_V(4))
                return !printf("%d,%d\n", i + 4, j);

            // or 1 1 0 1 1
            if (i + 4 < height && me == PLAYER && me == AT_V(1) && EMPTY == AT_V(2) && me == AT_V(3) && me == AT_V(4))
                return !printf("%d,%d\n", i + 2, j);

            // or 1 0 1 1 1
            if (i + 4 < height && me == PLAYER && EMPTY == AT_V(1) && me == AT_V(2) && me == AT_V(3) && me == AT_V(4))
                return !printf("%d,%d\n", i + 1, j);

            // or 1 1 1 0 2
            if (i + 4 < height && me == PLAYER && me == AT_V(1) && me == AT_V(2) && EMPTY == AT_V(3) && me == AT_V(4))
                return !printf("%d,%d\n", i + 3, j);

            // or 0 1 1 1 1
            if (i + 4 < height && EMPTY == me && PLAYER == AT_V(1) && PLAYER == AT_V(2) && PLAYER == AT_V(3) && PLAYER == AT_V(4))
                return !printf("%d,%d\n", i, j);

            //* diagonal check *//
            // if 1 1 1 1 0
            if (i + 4 < height && j + 4 < width && me == PLAYER && me == AT_D(1) && me == AT_D(2) && me == AT_D(3) && EMPTY == AT_D(4))
                return !printf("%d,%d\n", i + 4, j + 4);

            // or 1 1 0 1 1
            if (i + 4 < height && j + 4 < width && me == PLAYER && me == AT_D(1) && EMPTY == AT_D(2) && me == AT_D(3) && me == AT_D(4))
                return !printf("%d,%d\n", i + 2, j + 2);

            // or 1 0 1 1 1
            if (i + 4 < height && j + 4 < width && me == PLAYER && EMPTY == AT_D(1) && me == AT_D(2) && me == AT_D(3) && me == AT_D(4))
                return !printf("%d,%d\n", i + 1, j + 1);

            // or 1 1 1 0 2
            if (i + 4 < height && j + 4 < width && me == PLAYER && me == AT_D(1) && me == AT_D(2) && EMPTY == AT_D(3) && me == AT_D(4))
                return !printf("%d,%d\n", i + 3, j + 3);

            // or 0 1 1 1 1
            if (i + 4 < height && j + 4 < width && EMPTY == me && PLAYER == AT_D(1) && PLAYER == AT_D(2) && PLAYER == AT_D(3) && PLAYER == AT_D(4))
                return !printf("%d,%d\n", i, j);

            //* anti-diagonal check *//
            // if 1 1 1 1 0
            if (i + 4 < height && j - 4 >= 0 && me == PLAYER && me == AT_A(1) && me == AT_A(2) && me == AT_A(3) && EMPTY == AT_A(4))
                return !printf("%d,%d\n", i + 4, j - 4);

            // or 1 1 0 1 1
            if (i + 4 < height && j - 4 >= 0 && me == PLAYER && me == AT_A(1) && EMPTY == AT_A(2) && me == AT_A(3) && me == AT_A(4))
                return !printf("%d,%d\n", i + 2, j - 2);

            // or 1 0 1 1 1
            if (i + 4 < height && j - 4 >= 0 && me == PLAYER && EMPTY == AT_A(1) && me == AT_A(2) && me == AT_A(3) && me == AT_A(4))
                return !printf("%d,%d\n", i + 1, j - 1);

            // or 1 1 1 0 2
            if (i + 4 < height && j - 4 >= 0 && me == PLAYER && me == AT_A(1) && me == AT_A(2) && EMPTY == AT_A(3) && me == AT_A(4))
                return !printf("%d,%d\n", i + 3, j - 3);

            // or 0 1 1 1 1
            if (i + 4 < height && j - 4 >= 0 && EMPTY == me && PLAYER == AT_A(1) && PLAYER == AT_A(2) && PLAYER == AT_A(3) && PLAYER == AT_A(4))
                return !printf("%d,%d\n", i, j);

#ifdef DEBUG
            fprintf(log_file, "%c ", me);
        }
        fprintf(log_file, "]\n");
    }
    fprintf(log_file, "]\n");
#else
        }
    } // end of for loops
#endif

    // if ai can loose in 2*2 moves (block)
#ifdef DEBUG
    fprintf(log_file, "[LOG]: 2 (block)\n[\n");
#endif
    for (i = 0; i < height; ++i) {
    #ifdef DEBUG
        fprintf(log_file, "    [ ");
    #endif
        for (j = 0; j < width; ++j) {
            me = AT(board);
            int tmp_y = i;
            int tmp_x = j;

            // board[(i - 2) * width + j + (-2|0|2)]
            // board[(i + 2) * width + j + (-2|0|2)]
            #define DIAGONAL_LEFT_UP board[(tmp_y - 2) * width + tmp_x - 2] + board[(tmp_y - 1) * width + tmp_x - 1] % 48
            #define VERTICAL_UP board[(tmp_y - 2) * width + tmp_x] + board[(tmp_y - 1) * width + tmp_x] % 48
            #define DIAGONAL_RIGHT_UP board[(tmp_y - 2) * width + tmp_x + 2] + board[(tmp_y - 1) * width + tmp_x + 1] % 48
            #define HORIZONTAL_LEFT board[tmp_y * width + tmp_x - 2] + board[tmp_y * width + tmp_x - 1] % 48
            #define HORIZONTAL_RIGHT board[tmp_y * width + tmp_x + 2] + board[tmp_y * width + tmp_x + 1] % 48
            #define DIAGONAL_LEFT_DOWN board[(tmp_y + 2) * width + tmp_x - 2] + board[(tmp_y + 1) * width + tmp_x - 1] % 48
            #define VERTICAL_DOWN board[(tmp_y + 2) * width + tmp_x] + board[(tmp_y + 1) * width + tmp_x] % 48
            #define DIAGONAL_RIGHT_DOWN board[(tmp_y + 2) * width + tmp_x + 2] + board[(tmp_y + 1) * width + tmp_x + 1] % 48

            uint8_t lines[8] = {0};

            //* horizontal check *//
            // if 0 1 1 1 0
            if (j + 4 < width && EMPTY == me && PLAYER == AT_H(1) && PLAYER == AT_H(2) && PLAYER == AT_H(3) && EMPTY == AT_H(4)) {
                if (i + 2 < height && i - 2 >= 0 && j - 2 >= 0) {
                    memcpy(lines, (uint8_t [8]){
                        DIAGONAL_LEFT_UP,   VERTICAL_UP,   DIAGONAL_RIGHT_UP,
                        HORIZONTAL_LEFT,                   HORIZONTAL_RIGHT,
                        DIAGONAL_LEFT_DOWN, VERTICAL_DOWN, DIAGONAL_RIGHT_DOWN
                    }, 8);
                }
                tmp_x += 4;

                uint8_t lines_h[8]= {0};

                if (tmp_y + 2 < height && tmp_x + 2 < width && tmp_x - 2 >= 0) {
                    memcpy(lines_h, (uint8_t [8]){
                        DIAGONAL_LEFT_UP,   VERTICAL_UP,   DIAGONAL_RIGHT_UP,
                        HORIZONTAL_LEFT,                   HORIZONTAL_RIGHT,
                        DIAGONAL_LEFT_DOWN, VERTICAL_DOWN, DIAGONAL_RIGHT_DOWN
                    }, 8);
                }

                // compare without the lines[HORIZONTAL_RIGHT] and lines_h[HORIZONTAL_LEFT]
                // find max in lines_h
                int max = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines_h[k] > max && k != HORIZONTAL_LEFT)
                        max = lines_h[k];

                // find max in lines
                int max2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines[k] > max2 && k != HORIZONTAL_RIGHT)
                        max2 = lines[k];

                if (max > max2)
                    return !printf("%d,%d\n", i, j + 4);
                else if (max < max2)
                    return !printf("%d,%d\n", i, j);

                // find how many max in lines_h
                int sum = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines_h[k] == max && k != HORIZONTAL_LEFT)
                        sum++;

                // find how many max in lines
                int sum2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines[k] == max2 && k != HORIZONTAL_RIGHT)
                        sum2++;

                if (sum > sum2)
                    return !printf("%d,%d\n", i, j + 4);
                else if (sum < sum2)
                    return !printf("%d,%d\n", i, j);

                // sum all lines_h
                sum = 0;
                for (int k = 0; k < 8; ++k)
                    if (k != HORIZONTAL_LEFT)
                        sum += lines_h[k];

                // sum all lines
                sum2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (k != HORIZONTAL_RIGHT)
                        sum2 += lines[k];

                if (sum > sum2)
                    return !printf("%d,%d\n", i, j + 4);
                else if (sum < sum2)
                    return !printf("%d,%d\n", i, j);

                return !printf("%d,%d\n", i, j);
            }

            //* vertical check *//
            // if 0 1 1 1 0
            if (i + 4 < height && EMPTY == me && PLAYER == AT_V(1) && PLAYER == AT_V(2) && PLAYER == AT_V(3) && EMPTY == AT_V(4)) {
                if (j + 2 < width && j - 2 >= 0 && i - 2 >= 0) {
                    memcpy(lines, (uint8_t [8]){
                        DIAGONAL_LEFT_UP,   VERTICAL_UP,   DIAGONAL_RIGHT_UP,
                        HORIZONTAL_LEFT,                   HORIZONTAL_RIGHT,
                        DIAGONAL_LEFT_DOWN, VERTICAL_DOWN, DIAGONAL_RIGHT_DOWN
                    }, 8);
                }

                tmp_y += 4;

                uint8_t lines_v[8]= {0};

                if (tmp_x + 2 < width && tmp_x - 2 >= 0 && tmp_y - 2 >= 0) {
                    memcpy(lines_v, (uint8_t [8]){
                        DIAGONAL_LEFT_UP,   VERTICAL_UP,   DIAGONAL_RIGHT_UP,
                        HORIZONTAL_LEFT,                   HORIZONTAL_RIGHT,
                        DIAGONAL_LEFT_DOWN, VERTICAL_DOWN, DIAGONAL_RIGHT_DOWN
                    }, 8);
                }

                // compare without the lines[VERTICAL_DOWN] and lines_v[VERTICAL_UP]
                // find max in lines_v
                int max = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines_v[k] > max && k != VERTICAL_UP)
                        max = lines_v[k];

                // find max in lines
                int max2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines[k] > max2 && k != VERTICAL_DOWN)
                        max2 = lines[k];

                if (max > max2)
                    return !printf("%d,%d\n", i + 4, j);
                else if (max < max2)
                    return !printf("%d,%d\n", i, j);

                // find how many max in lines_v
                int sum = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines_v[k] == max && k != VERTICAL_UP)
                        sum ++;

                // find how many max in lines
                int sum2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines[k] == max2 && k != VERTICAL_DOWN)
                        sum2 ++;

                if (sum > sum2)
                    return !printf("%d,%d\n", i + 4, j);
                else if (sum < sum2)
                    return !printf("%d,%d\n", i, j);

                // sum all lines_v
                sum = 0;
                for (int k = 0; k < 8; ++k)
                    if (k != VERTICAL_UP)
                        sum += lines_v[k];

                // sum all lines
                sum2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (k != VERTICAL_DOWN)
                        sum2 += lines[k];

                if (sum > sum2)
                    return !printf("%d,%d\n", i + 4, j);
                else if (sum < sum2)
                    return !printf("%d,%d\n", i, j);

                return !printf("%d,%d\n", i, j);
            }

            //* diagonal check *//
            // if 0 1 1 1 0
            if (i + 4 < height && EMPTY == me && j + 4 < width && PLAYER == AT_D(1) && PLAYER == AT_D(2) && PLAYER == AT_D(3) && EMPTY == AT_D(4)) {
                if (i + 2 < height && j + 2 < width && i - 2 >= 0 && j - 2 >= 0) {
                    memcpy(lines, (uint8_t [8]){
                        DIAGONAL_LEFT_UP,   VERTICAL_UP,   DIAGONAL_RIGHT_UP,
                        HORIZONTAL_LEFT,                   HORIZONTAL_RIGHT,
                        DIAGONAL_LEFT_DOWN, VERTICAL_DOWN, DIAGONAL_RIGHT_DOWN
                    }, 8);
                }

                tmp_y += 4;
                tmp_x += 4;

                uint8_t lines_d[8]= {0};

                if (tmp_y + 2 < height && tmp_x + 2 < width && tmp_y - 2 >= 0 && tmp_x - 2 >= 0) {
                    memcpy(lines_d, (uint8_t [8]){
                        DIAGONAL_LEFT_UP,   VERTICAL_UP,   DIAGONAL_RIGHT_UP,
                        HORIZONTAL_LEFT,                   HORIZONTAL_RIGHT,
                        DIAGONAL_LEFT_DOWN, VERTICAL_DOWN, DIAGONAL_RIGHT_DOWN
                    }, 8);
                }

                // compare without the lines[DIAGONAL_RIGHT_DOWN] and lines_d[DIAGONAL_LEFT_UP]
                // find max in lines_d
                int max = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines_d[k] > max && k != DIAGONAL_LEFT_UP)
                        max = lines_d[k];

                // find max in lines
                int max2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines[k] > max2 && k != DIAGONAL_RIGHT_DOWN)
                        max2 = lines[k];

                if (max > max2)
                    return !printf("%d,%d\n", i + 4, j + 4);
                else if (max < max2)
                    return !printf("%d,%d\n", i, j);

                // find how many max in lines_d
                int sum = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines_d[k] == max && k != DIAGONAL_LEFT_UP)
                        sum ++;

                // find how many max in lines
                int sum2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines[k] == max2 && k != DIAGONAL_RIGHT_DOWN)
                        sum2 ++;

                if (sum > sum2)
                    return !printf("%d,%d\n", i + 4, j + 4);
                else if (sum < sum2)
                    return !printf("%d,%d\n", i, j);

                // sum all lines_d
                sum = 0;
                for (int k = 0; k < 8; ++k)
                    if (k != DIAGONAL_LEFT_UP)
                        sum += lines_d[k];

                // sum all lines
                sum2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (k != DIAGONAL_RIGHT_DOWN)
                        sum2 += lines[k];

                if (sum > sum2)
                    return !printf("%d,%d\n", i + 4, j + 4);
                else if (sum < sum2)
                    return !printf("%d,%d\n", i, j);

                return !printf("%d,%d\n", i, j);
            }

            //* anti-diagonal check *//
            // if 0 1 1 1 0
            if (i + 4 < height && EMPTY == me && j - 4 >= 0 && PLAYER == AT_A(1) && PLAYER == AT_A(2) && PLAYER == AT_A(3) && EMPTY == AT_A(4)) {
                if (i + 2 < height && j + 2 < width && i - 2 >= 0 && j - 2 >= 0) {
                    memcpy(lines, (uint8_t [8]){
                        DIAGONAL_LEFT_UP,   VERTICAL_UP,   DIAGONAL_RIGHT_UP,
                        HORIZONTAL_LEFT,                   HORIZONTAL_RIGHT,
                        DIAGONAL_LEFT_DOWN, VERTICAL_DOWN, DIAGONAL_RIGHT_DOWN
                    }, 8);
                }

                tmp_y = i + 4;
                tmp_x = j - 4;

                uint8_t lines_a[8]= {0};

                if (tmp_y + 2 < height && tmp_x + 2 < width && tmp_y - 2 >= 0 && tmp_x - 2 >= 0) {
                    memcpy(lines_a, (uint8_t [8]){
                        DIAGONAL_LEFT_UP,   VERTICAL_UP,   DIAGONAL_RIGHT_UP,
                        HORIZONTAL_LEFT,                   HORIZONTAL_RIGHT,
                        DIAGONAL_LEFT_DOWN, VERTICAL_DOWN, DIAGONAL_RIGHT_DOWN
                    }, 8);
                };

                // compare without the lines[DIAGONAL_LEFT_DOWN] and lines_a[DIAGONAL_RIGHT_UP]
                // find max in lines_a
                int max = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines_a[k] > max && k != DIAGONAL_RIGHT_UP)
                        max = lines_a[k];

                // find max in lines
                int max2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines[k] > max2 && k != DIAGONAL_LEFT_DOWN)
                        max2 = lines[k];

                if (max > max2)
                    return !printf("%d,%d\n", i + 4, j - 4);
                else if (max < max2)
                    return !printf("%d,%d\n", i, j);

                // find how many max in lines_a
                int sum = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines_a[k] == max && k != DIAGONAL_RIGHT_UP)
                        sum ++;

                // find how many max in lines
                int sum2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (lines[k] == max2 && k != DIAGONAL_LEFT_DOWN)
                        sum2 ++;

                if (sum > sum2)
                    return !printf("%d,%d\n", i + 4, j - 4);
                else if (sum < sum2)
                    return !printf("%d,%d\n", i, j);

                // sum all lines_a
                sum = 0;
                for (int k = 0; k < 8; ++k)
                    if (k != DIAGONAL_RIGHT_UP)
                        sum += lines_a[k];

                // sum all lines
                sum2 = 0;
                for (int k = 0; k < 8; ++k)
                    if (k != DIAGONAL_LEFT_DOWN)
                        sum2 += lines[k];

                if (sum > sum2)
                    return !printf("%d,%d\n", i + 4, j - 4);
                else if (sum < sum2)
                    return !printf("%d,%d\n", i, j);

                return !printf("%d,%d\n", i, j);
            }

#ifdef DEBUG
            fprintf(log_file, "%c ", me);
        }
        fprintf(log_file, "]\n");
    }
    fprintf(log_file, "]\n");
#else
        }
    } // end of for loops
#endif


    // if ai can loose in 2 moves (block) by block check
#ifdef DEBUG
    fprintf(log_file, "[LOG]: 2 (block) by block check\n[\n");
#endif
    for (i = 0; i < height; ++i) {
    #ifdef DEBUG
        fprintf(log_file, "    [ ");
    #endif
        for (j = 0; j < width; ++j) {
            me = AT(board);

            //* block check *//
            //  1 1
            //  1 0
            if (j + 2 < width && i + 2 < height && PLAYER == me && PLAYER == AT_H(1) && PLAYER == AT_V(1) && EMPTY == AT_D(1))
                return !printf("%d,%d\n", i + 1, j + 1);

            //  1 1
            //  0 1
            if (j + 2 < width && i + 2 < height && PLAYER == me && PLAYER == AT_H(1) && EMPTY == AT_V(1) && PLAYER == AT_D(1))
                return !printf("%d,%d\n", i + 1, j);

            //  1 0
            //  1 1
            if (j + 2 < width && i + 2 < height && PLAYER == me && EMPTY == AT_H(1) && PLAYER == AT_V(1) && PLAYER == AT_D(1))
                return !printf("%d,%d\n", i, j + 1);

            //  0 1
            //  1 1
            if (j + 2 < width && i + 2 < height && EMPTY == me && PLAYER == AT_H(1) && PLAYER == AT_V(1) && PLAYER == AT_D(1))
                return !printf("%d,%d\n", i, j);
#ifdef DEBUG
            fprintf(log_file, "%c ", me);
        }
        fprintf(log_file, "]\n");
    }
    fprintf(log_file, "]\n");
#else
        }
    } // end of for loops
#endif

    // if ai can win in 2 moves do it
#ifdef DEBUG
    fprintf(log_file, "[LOG]: 2 (do it)\n[\n");
#endif
    for (i = 0; i < height; ++i) {
    #ifdef DEBUG
        fprintf(log_file, "    [ ");
    #endif
        for (j = 0; j < width; ++j) {
            me = AT(board);

            //* horizontal check *//
            // if 0 2 2 2 0
            if (j + 4 < width && EMPTY == me && OPPONENT == AT_H(1) && OPPONENT == AT_H(2) && OPPONENT == AT_H(3) && EMPTY == AT_H(4))
                return !printf("%d,%d\n", i, j);

            // or 0 0 2 2 2
            if (j + 4 < width && EMPTY == me && EMPTY == AT_H(1) && OPPONENT == AT_H(2) && OPPONENT == AT_H(3) && OPPONENT == AT_H(4))
                return !printf("%d,%d\n", i, j);

            // or 2 2 2 0 0
            if (j + 4 < width && me == OPPONENT && me == AT_H(1) && me == AT_H(2) && EMPTY == AT_H(3) && EMPTY == AT_H(4))
                return !printf("%d,%d\n", i, j + 3);

            //* vertical check *//
            // if 0 2 2 2 0
            if (i + 4 < height && EMPTY == me && OPPONENT == AT_V(1) && OPPONENT == AT_V(2) && OPPONENT == AT_V(3) && EMPTY == AT_V(4))
                return !printf("%d,%d\n", i, j);

            // or 0 0 2 2 2
            if (i + 4 < height && EMPTY == me && EMPTY == AT_V(1) && OPPONENT == AT_V(2) && OPPONENT == AT_V(3) && OPPONENT == AT_V(4))
                return !printf("%d,%d\n", i, j);

            // or 2 2 2 0 0
            if (i + 4 < height && me == OPPONENT && me == AT_V(1) && me == AT_V(2) && EMPTY == AT_V(3) && EMPTY == AT_V(4))
                return !printf("%d,%d\n", i + 3, j);

            //* diagonal check *//
            // if 0 2 2 2 0
            if (i + 4 < height && j + 4 < width && EMPTY == me && OPPONENT == AT_D(1) && OPPONENT == AT_D(2) && OPPONENT == AT_D(3) && EMPTY == AT_D(4))
                return !printf("%d,%d\n", i, j);

            // or 0 0 2 2 2
            if (i + 4 < height && j + 4 < width && EMPTY == me && EMPTY == AT_D(1) && OPPONENT == AT_D(2) && OPPONENT == AT_D(3) && OPPONENT == AT_D(4))
                return !printf("%d,%d\n", i, j);

            // or 2 2 2 0 0
            if (i + 4 < height && j + 4 < width && me == OPPONENT && me == AT_D(1) && me == AT_D(2) && EMPTY == AT_D(3) && EMPTY == AT_D(4))
                return !printf("%d,%d\n", i + 3, j + 3);

            //* anti-diagonal check *//
            // if 0 2 2 2 0
            if (i + 4 < height && j - 4 >= 0 && EMPTY == me && OPPONENT == AT_A(1) && OPPONENT == AT_A(2) && OPPONENT == AT_A(3) && EMPTY == AT_A(4))
                return !printf("%d,%d\n", i, j);

            // or 0 0 2 2 2
            if (i + 4 < height && j - 4 >= 0 && EMPTY == me && EMPTY == AT_A(1) && OPPONENT == AT_A(2) && OPPONENT == AT_A(3) && OPPONENT == AT_A(4))
                return !printf("%d,%d\n", i, j);

            // or 2 2 2 0 0
            if (i + 4 < height && j - 4 >= 0 && me == OPPONENT && me == AT_A(1) && me == AT_A(2) && EMPTY == AT_A(3) && EMPTY == AT_A(4))
                return !printf("%d,%d\n", i + 3, j - 3);

            //* block check *//
            //  1 1
            //  1 0
            if (j + 2 < width && i + 2 < height && OPPONENT == me && OPPONENT == AT_H(1) && OPPONENT == AT_V(1) && EMPTY == AT_D(1))
                return !printf("%d,%d\n", i + 1, j + 1);

            //  1 1
            //  0 1
            if (j + 2 < width && i + 2 < height && OPPONENT == me && OPPONENT == AT_H(1) && EMPTY == AT_V(1) && OPPONENT == AT_D(1))
                return !printf("%d,%d\n", i + 1, j);

            //  1 0
            //  1 1
            if (j + 2 < width && i + 2 < height && OPPONENT == me && EMPTY == AT_H(1) && OPPONENT == AT_V(1) && OPPONENT == AT_D(1))
                return !printf("%d,%d\n", i, j + 1);

            //  0 1
            //  1 1
            if (j + 2 < width && i + 2 < height && EMPTY == me && OPPONENT == AT_H(1) && OPPONENT == AT_V(1) && OPPONENT == AT_D(1))
                return !printf("%d,%d\n", i, j);

#ifdef DEBUG
            fprintf(log_file, "%c ", me);
        }
        fprintf(log_file, "]\n");
    }
    fprintf(log_file, "]\n");
#else
        }
    } // end of for loops
#endif

    // if ai can win in 3 moves do it
#ifdef DEBUG
    fprintf(log_file, "[LOG]: 3 (do it)\n[\n");
#endif
    for (i = 0; i < height; ++i) {
    #ifdef DEBUG
        fprintf(log_file, "    [ ");
    #endif
        for (j = 0; j < width; ++j) {
            me = AT(board);

            //* horizontal check *//

            // if 0 0 0 1 1
            if (j + 4 < width && EMPTY == me && PLAYER != AT_H(1) && PLAYER != AT_H(2) && OPPONENT == AT_H(3) && OPPONENT == AT_H(4))
                return !printf("%d,%d\n", i, j);
            // or 0 0 1 1 0
            if (j + 4 < width && EMPTY == me && PLAYER != AT_H(1) && OPPONENT == AT_H(2) && OPPONENT == AT_H(3) && PLAYER != AT_H(4))
                return !printf("%d,%d\n", i, j);
            // or 0 1 1 0 0
            if (j + 4 < width && EMPTY == me && OPPONENT == AT_H(1) && OPPONENT == AT_H(2) && PLAYER != AT_H(3) && PLAYER != AT_H(4))
                return !printf("%d,%d\n", i, j);
            // or 1 1 0 0 0
            if (j + 4 < width && OPPONENT == me && OPPONENT == AT_H(1) && PLAYER != AT_H(2) && PLAYER != AT_H(3) && EMPTY == AT_H(4))
                return !printf("%d,%d\n", i, j + 4);
            // or 0 1 0 1 0
            if (j + 4 < width && EMPTY == me && OPPONENT == AT_H(1) && PLAYER != AT_H(2) && OPPONENT == AT_H(3) && PLAYER != AT_H(4))
                return !printf("%d,%d\n", i, j);
            // or 0 0 1 0 1
            if (j + 4 < width && EMPTY == me && PLAYER != AT_H(1) && OPPONENT == AT_H(2) && PLAYER != AT_H(3) && OPPONENT == AT_H(4))
                return !printf("%d,%d\n", i, j);
            // or 1 0 1 0 0
            if (j + 4 < width && OPPONENT == me && PLAYER != AT_H(1) && OPPONENT == AT_H(2) && PLAYER != AT_H(3) && EMPTY == AT_H(4))
                return !printf("%d,%d\n", i, j + 4);
            // or 1 0 0 0 1
            if (j + 4 < width && OPPONENT == me && PLAYER != AT_H(1) && PLAYER != AT_H(2) && EMPTY == AT_H(3) && OPPONENT == AT_H(4))
                return !printf("%d,%d\n", i, j + 3);
            // or 0 1 0 0 1
            if (j + 4 < width && EMPTY == me && OPPONENT == AT_H(1) && PLAYER != AT_H(2) && PLAYER != AT_H(3) && OPPONENT == AT_H(4))
                return !printf("%d,%d\n", i, j);
            // or 1 0 0 1 0
            if (j + 4 < width && OPPONENT == me && PLAYER != AT_H(1) && PLAYER != AT_H(2) && OPPONENT == AT_H(3) && EMPTY == AT_H(4))
                return !printf("%d,%d\n", i, j + 4);

            //* vertical check *//

            // if 0 0 0 1 1
            if (i + 4 < height && EMPTY == me && PLAYER != AT_V(1) && PLAYER != AT_V(2) && OPPONENT == AT_V(3) && OPPONENT == AT_V(4))
                return !printf("%d,%d\n", i, j);
            // or 0 0 1 1 0
            if (i + 4 < height && EMPTY == me && PLAYER != AT_V(1) && OPPONENT == AT_V(2) && OPPONENT == AT_V(3) && PLAYER != AT_V(4))
                return !printf("%d,%d\n", i, j);
            // or 0 1 1 0 0
            if (i + 4 < height && EMPTY == me && OPPONENT == AT_V(1) && OPPONENT == AT_V(2) && PLAYER != AT_V(3) && PLAYER != AT_V(4))
                return !printf("%d,%d\n", i, j);
            // or 1 1 0 0 0
            if (i + 4 < height && OPPONENT == me && OPPONENT == AT_V(1) && PLAYER != AT_V(2) && PLAYER != AT_V(3) && EMPTY == AT_V(4))
                return !printf("%d,%d\n", i + 4, j);
            // or 0 1 0 1 0
            if (i + 4 < height && EMPTY == me && OPPONENT == AT_V(1) && PLAYER != AT_V(2) && OPPONENT == AT_V(3) && PLAYER != AT_V(4))
                return !printf("%d,%d\n", i, j);
            // or 0 0 1 0 1
            if (i + 4 < height && EMPTY == me && PLAYER != AT_V(1) && OPPONENT == AT_V(2) && PLAYER != AT_V(3) && OPPONENT == AT_V(4))
                return !printf("%d,%d\n", i, j);
            // or 1 0 1 0 0
            if (i + 4 < height && OPPONENT == me && PLAYER != AT_V(1) && OPPONENT == AT_V(2) && PLAYER != AT_V(3) && EMPTY == AT_V(4))
                return !printf("%d,%d\n", i + 4, j);
            // or 1 0 0 0 1
            if (i + 4 < height && OPPONENT == me && PLAYER != AT_V(1) && PLAYER != AT_V(2) && EMPTY == AT_V(3) && OPPONENT == AT_V(4))
                return !printf("%d,%d\n", i + 3, j);
            // or 0 1 0 0 1
            if (i + 4 < height && EMPTY == me && OPPONENT == AT_V(1) && PLAYER != AT_V(2) && PLAYER != AT_V(3) && OPPONENT == AT_V(4))
                return !printf("%d,%d\n", i, j);
            // or 1 0 0 1 0
            if (i + 4 < height && OPPONENT == me && PLAYER != AT_V(1) && PLAYER != AT_V(2) && OPPONENT == AT_V(3) && EMPTY == AT_V(4))
                return !printf("%d,%d\n", i + 4, j);

            //* diagonal check *//

            // if 0 0 0 1 1
            if (i + 4 < height && j + 4 < width && EMPTY == me && PLAYER != AT_D(1) && PLAYER != AT_D(2) && OPPONENT == AT_D(3) && OPPONENT == AT_D(4))
                return !printf("%d,%d\n", i, j);
            // or 0 0 1 1 0
            if (i + 4 < height && j + 4 < width && EMPTY == me && PLAYER != AT_D(1) && OPPONENT == AT_D(2) && OPPONENT == AT_D(3) && PLAYER != AT_D(4))
                return !printf("%d,%d\n", i, j);
            // or 0 1 1 0 0
            if (i + 4 < height && j + 4 < width && EMPTY == me && OPPONENT == AT_D(1) && OPPONENT == AT_D(2) && PLAYER != AT_D(3) && PLAYER != AT_D(4))
                return !printf("%d,%d\n", i, j);
            // or 1 1 0 0 0
            if (i + 4 < height && j + 4 < width && OPPONENT == me && OPPONENT == AT_D(1) && PLAYER != AT_D(2) && PLAYER != AT_D(3) && EMPTY == AT_D(4))
                return !printf("%d,%d\n", i + 4, j + 4);
            // or 0 1 0 1 0
            if (i + 4 < height && j + 4 < width && EMPTY == me && OPPONENT == AT_D(1) && PLAYER != AT_D(2) && OPPONENT == AT_D(3) && PLAYER != AT_D(4))
                return !printf("%d,%d\n", i, j);
            // or 0 0 1 0 1
            if (i + 4 < height && j + 4 < width && EMPTY == me && PLAYER != AT_D(1) && OPPONENT == AT_D(2) && PLAYER != AT_D(3) && OPPONENT == AT_D(4))
                return !printf("%d,%d\n", i, j);
            // or 1 0 1 0 0
            if (i + 4 < height && j + 4 < width && OPPONENT == me && PLAYER != AT_D(1) && OPPONENT == AT_D(2) && PLAYER != AT_D(3) && EMPTY == AT_D(4))
                return !printf("%d,%d\n", i + 4, j + 4);
            // or 1 0 0 0 1
            if (i + 4 < height && j + 4 < width && OPPONENT == me && PLAYER != AT_D(1) && PLAYER != AT_D(2) && EMPTY == AT_D(3) && OPPONENT == AT_D(4))
                return !printf("%d,%d\n", i + 3, j + 3);
            // or 0 1 0 0 1
            if (i + 4 < height && j + 4 < width && EMPTY == me && OPPONENT == AT_D(1) && PLAYER != AT_D(2) && PLAYER != AT_D(3) && OPPONENT == AT_D(4))
                return !printf("%d,%d\n", i, j);
            // or 1 0 0 1 0
            if (i + 4 < height && j + 4 < width && OPPONENT == me && PLAYER != AT_D(1) && PLAYER != AT_D(2) && OPPONENT == AT_D(3) && EMPTY == AT_D(4))
                return !printf("%d,%d\n", i + 4, j + 4);

            //* anti-diagonal check *//

            // if 0 0 0 1 1
            if (i + 4 < height && j - 4 >= 0 && EMPTY == me && PLAYER != AT_A(1) && PLAYER != AT_A(2) && OPPONENT == AT_A(3) && OPPONENT == AT_A(4))
                return !printf("%d,%d\n", i, j);
            // or 0 0 1 1 0
            if (i + 4 < height && j - 4 >= 0 && EMPTY == me && PLAYER != AT_A(1) && OPPONENT == AT_A(2) && OPPONENT == AT_A(3) && PLAYER != AT_A(4))
                return !printf("%d,%d\n", i, j);
            // or 0 1 1 0 0
            if (i + 4 < height && j - 4 >= 0 && EMPTY == me && OPPONENT == AT_A(1) && OPPONENT == AT_A(2) && PLAYER != AT_A(3) && PLAYER != AT_A(4))
                return !printf("%d,%d\n", i, j);
            // or 1 1 0 0 0
            if (i + 4 < height && j - 4 >= 0 && OPPONENT == me && OPPONENT == AT_A(1) && PLAYER != AT_A(2) && PLAYER != AT_A(3) && EMPTY == AT_A(4))
                return !printf("%d,%d\n", i + 4, j - 4);
            // or 0 1 0 1 0
            if (i + 4 < height && j - 4 >= 0 && EMPTY == me && OPPONENT == AT_A(1) && PLAYER != AT_A(2) && OPPONENT == AT_A(3) && PLAYER != AT_A(4))
                return !printf("%d,%d\n", i, j);
            // or 0 0 1 0 1
            if (i + 4 < height && j - 4 >= 0 && EMPTY == me && PLAYER != AT_A(1) && OPPONENT == AT_A(2) && PLAYER != AT_A(3) && OPPONENT == AT_A(4))
                return !printf("%d,%d\n", i, j);
            // or 1 0 1 0 0
            if (i + 4 < height && j - 4 >= 0 && OPPONENT == me && PLAYER != AT_A(1) && OPPONENT == AT_A(2) && PLAYER != AT_A(3) && EMPTY == AT_A(4))
                return !printf("%d,%d\n", i + 4, j - 4);
            // or 1 0 0 0 1
            if (i + 4 < height && j - 4 >= 0 && OPPONENT == me && PLAYER != AT_A(1) && PLAYER != AT_A(2) && EMPTY == AT_A(3) && OPPONENT == AT_A(4))
                return !printf("%d,%d\n", i + 3, j - 3);
            // or 0 1 0 0 1
            if (i + 4 < height && j - 4 >= 0 && EMPTY == me && OPPONENT == AT_A(1) && PLAYER != AT_A(2) && PLAYER != AT_A(3) && OPPONENT == AT_A(4))
                return !printf("%d,%d\n", i, j);
            // or 1 0 0 1 0
            if (i + 4 < height && j - 4 >= 0 && OPPONENT == me && PLAYER != AT_A(1) && PLAYER != AT_A(2) && OPPONENT == AT_A(3) && EMPTY == AT_A(4))
                return !printf("%d,%d\n", i + 4, j - 4);

#ifdef DEBUG
            fprintf(log_file, "%c ", me);
        }
        fprintf(log_file, "]\n");
    }
    fprintf(log_file, "]\n");
#else
        }
    } // end of for loops
#endif

    // if ai can win in 4 moves (block)
#ifdef DEBUG
    fprintf(log_file, "[LOG]: 4 (block)\n[\n");
#endif
    for (i = 0; i < height; ++i) {
    #ifdef DEBUG
        fprintf(log_file, "    [ ");
    #endif
        for (j = 0; j < width; ++j) {
            me = AT(board);
            if (j + 4 < width && me == PLAYER && EMPTY == AT_H(1))
                return !printf("%d,%d\n", i, j + 1);
            if (me + 4 < height &&  me == PLAYER && EMPTY == AT_V(1))
                return !printf("%d,%d\n", i + 1, j);
            if (i + 4 < height && j + 4 < width && me == PLAYER && EMPTY == AT_D(1))
                return !printf("%d,%d\n", i + 1, j + 1);
            if (i + 4 < height && j - 4 >= 0 && me == PLAYER && EMPTY == AT_A(1))
                return !printf("%d,%d\n", i + 1, j - 1);

#ifdef DEBUG
            fprintf(log_file, "%c ", me);
        }
        fprintf(log_file, "]\n");
    }
    fprintf(log_file, "]\n");
#else
        }
    } // end of for loops
#endif

    // play in the first empty case between 4 and max-4
#ifdef DEBUG
    fprintf(log_file, "[LOG]: 4 (first empty case between 4 and max-4)\n[\n");
#endif
    for (i = 4; i < height-4; ++i)
        for (j = 4; j < width-4; ++j) {
            if (AT(board) == EMPTY)
                return !printf("%d,%d\n", i, j);
        }

    // play in the first empty case
    for (i = 0; i < height; ++i)
        for (j = 0; j < width; ++j) {
            if (AT(board) == EMPTY)
                return !printf("%d,%d\n", i, j);
        }

#ifdef DEBUG
    fprintf(log_file, "[ERROR]: (-1, -1)\n");
    fclose(log_file);
#endif
    printf("-1,-1\n");
    return 1;
}
