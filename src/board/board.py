#!/usr/bin/env python3
import pygame
import sys

class BoardGame:
    def __init__(self):
        pygame.init()

        self.cell_size = 40  # Size for each cell on the board
        self.board_color = (255, 255, 255)
        self.player_colors = [(255, 0, 0), (0, 0, 255)]  # Player 1: Red, Player 2: Blue
        self.current_player = 0  # Start with player 0

        self.log_width = 400  # Width for the log space
        self.game_width, self.game_height = 800, 600  # Initial game window size
        self.total_width = self.game_width + self.log_width  # Total window width including log
        self.screen = pygame.display.set_mode((self.total_width, self.game_height))
        pygame.display.set_caption("GOMOKU Setup")

        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)  # Smaller font for more text
        self.bg_color = (30, 30, 30)
        self.font_color = (255, 255, 255)
        self.welcome_message = "Welcome to GOMOKU!"
        self.input_box = pygame.Rect(self.game_width // 2 - 100, 300, 200, 50)
        self.input_text = ''
        self.clock = pygame.time.Clock()
        self.board_size = None
        self.game_started = False
        self.start_button = pygame.Rect(self.game_width // 2 - 50, 400, 100, 50)
        self.start_button_active = False
        self.game_matrix = []
        self.move_history = []  # To store move history for the log
        self.log_scroll_pos = 0  # Initial log scroll position
        self.move = 0

        self.frame_count = 0
        self.frame_rate = 60
        self.start_time = 5

    def run(self):
        while not self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                self.handle_setup_event(event)

            self.draw_setup_screen()

        self.prepare_game()
        self.run_game()

    def prepare_game(self):
        # Initialize game board matrix with None values to represent empty cells
        self.game_matrix = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        # Set up a window size based on board size including the log width
        self.game_width = self.board_size * self.cell_size
        self.total_width = self.game_width + self.log_width  # Update total width
        self.game_height = self.game_width  # Making the window square
        self.screen = pygame.display.set_mode((self.total_width, self.game_height))  # Use total_width to consider the log space
        pygame.display.set_caption("GOMOKU Game")
        self.visible_count = self.game_height // (self.small_font.get_height() + 5)  # Calculate the number of moves that can be visible at once

    def handle_setup_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if event.unicode.isdigit() and len(self.input_text) < 3:
                    self.input_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                if self.input_text.isdigit() and 4 < int(self.input_text) <= 20:
                    self.board_size = int(self.input_text)
                    self.game_started = True  # Start the game
                else:
                    self.start_button_active = False  # Disable the start button
                    print("Please enter a valid board size (5-20).")  # Or show this message in the GUI

    def draw_error_message(self):
        if not self.start_button_active and self.input_text:
            # Assume that if the start button isn't active but there's input, it's an error
            error_msg = "Enter a board size between 5-20"
            self.draw_text_centered(error_msg, self.small_font, (255, 0, 0), pygame.Rect(0, 350, self.total_width, 50))

    def run_game(self):
        self.game_width = self.board_size * self.cell_size
        self.total_width = self.game_width + self.log_width  # Update total width
        self.game_height = self.game_width + self.cell_size  # Making the height equal to the game width for a square board
        self.screen = pygame.display.set_mode((self.total_width, self.game_height))
        self.log_scroll_pos = max(0, len(self.move_history) - self.visible_count)  # Update scroll position on new game
        while self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                self.handle_game_event(event)
            self.draw_board_screen()

    def handle_game_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if event.button == 1 and mouse_x < self.game_width + self.cell_size:
                board_x, board_y = mouse_x - self.cell_size, mouse_y - self.cell_size # subtract offset here before calculating x and y
                if board_x >= 0 and board_y >= 0:  # Check if the click is within the positive index range
                    x, y = board_x // self.cell_size, board_y // self.cell_size
                    if 0 <= x < self.board_size and 0 <= y < self.board_size: # Check for valid board indices
                        self.play_a_turn(x, y)
            elif event.button == 4:  # Mouse wheel up
                self.update_log_scroll(-1)
                self.log_scroll_pos = max(self.log_scroll_pos - 1, 0)
            elif event.button == 5:  # Mouse wheel down
                self.update_log_scroll(1)
                max_scroll_pos = max(0, len(self.move_history) - (self.game_height // (self.small_font.get_height() + 5)))
                self.log_scroll_pos = min(self.log_scroll_pos + 1, max_scroll_pos)

    def play_a_turn(self, x, y):
        if self.game_matrix[y][x] is None:
            self.game_matrix[y][x] = self.current_player
            # Log the move with a shifted position because the visual offset doesn't change matrix coordinates
            self.move_history.append(f"- {self.move} : p{self.current_player + 1}: ({x}, {y})")
            self.current_player = (self.current_player + 1) % 2  # Switch players
            self.move += 1

    def draw_setup_screen(self):
        self.screen.fill(self.bg_color)
        # Draw welcome message
        # Adjust to use the center of the total_width, not just the game width
        self.draw_text_centered("Welcome to GOMOKU!", self.small_font, self.font_color, pygame.Rect(0, 50, self.total_width, 50))
        # Input box
        # Center the input box based on the total_width, not just game_width
        input_box_x = self.total_width // 2 - self.input_box.width // 2  # Update the x-coordinate for the input box
        self.input_box.topleft = (input_box_x, self.input_box.top)  # Update the input box to new position
        pygame.draw.rect(self.screen, self.font_color, self.input_box, 2)
        self.draw_text_centered(self.input_text, self.font, self.font_color, self.input_box)
        # Start button
        # Center the start button based on the total_width, not just game_width
        start_button_x = self.total_width // 2 - self.start_button.width // 2  # Update the x-coordinate for the start button
        self.start_button.topleft = (start_button_x, self.start_button.top)  # Update the start button to new position
        pygame.draw.rect(self.screen, (0, 255, 0) if self.start_button_active else (100, 100, 100), self.start_button)
        self.draw_text_centered("Start", self.small_font, self.font_color, self.start_button)
        self.draw_error_message()
        pygame.display.flip()
        self.clock.tick(self.frame_rate)

    def draw_board_screen(self):
        # Draw the game board and the log side by side
        self.screen.fill(self.bg_color)

        # Make the background for the indices
        index_background_color = (0, 0, 0) # Darker than bg_color for contrast
        index_background_rect = pygame.Rect(0, 0, self.game_width, self.cell_size)
        pygame.draw.rect(self.screen, index_background_color, index_background_rect)

        # Draw the board on its own part of the screen
        board_surf = pygame.Surface((self.game_width, self.game_height))
        board_surf.fill(self.board_color)
        # Adjust to draw indices
        # Adjusted code within draw_board_screen method
        for y in range(self.board_size):
            for x in range(self.board_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size) # Removed the additional offset here
                pygame.draw.rect(board_surf, self.bg_color, rect, 1)
                if self.game_matrix[y][x] is not None:
                    pygame.draw.circle(board_surf, self.player_colors[self.game_matrix[y][x]], rect.center, self.cell_size // 3)

        # Blit the board surface onto the screen with an offset for indices
        self.screen.blit(board_surf, (self.cell_size, self.cell_size))

        # Draw indices
        self.draw_indices()

        # Draw the log on its own part of the screen
        log_surf = pygame.Surface((self.log_width, self.game_height))
        log_surf.fill(self.bg_color)
        self.draw_log(log_surf)
        self.screen.blit(log_surf, (self.game_width + self.cell_size, self.cell_size))  # Position the log surface to the right of the board with offset

        # Draw the timer
        timer_surf = pygame.Surface((self.log_width, self.cell_size))
        timer_surf.fill(self.bg_color)
        self.draw_timer(timer_surf)
        self.screen.blit(timer_surf, (self.game_width + self.cell_size, 0))

        pygame.display.flip()
        self.clock.tick(self.frame_rate)

    def draw_timer(self, surface):
        # --- Timer going down ---
        # --- Timer going up ---
        # Calculate total seconds
        if self.current_player == 0:
            self.frame_count = 0
        total_seconds = self.start_time - (self.frame_count // self.frame_rate)
        if total_seconds < 0:
            total_seconds = 0
        elif self.current_player == 1 and total_seconds > 0:
            self.frame_count += 1

        # Divide by 60 to get total minutes
        minutes = total_seconds // 60

        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60

        # Use python string formatting to format in leading zeros
        output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)

        # Blit to the screen
        text = self.small_font.render(output_string, True, self.font_color)
        surface.blit(text, (10, 0))

    def draw_indices(self):
        # Adjust the offset to align with the board offset
        index_offset_x = self.cell_size
        index_offset_y = self.cell_size

        # Draw row indices along the left edge
        for y in range(self.board_size):
            text_surface = self.small_font.render(str(y), True, self.font_color)
            text_rect = text_surface.get_rect(left=5, centery=(y * self.cell_size + index_offset_y + self.cell_size // 2))
            self.screen.blit(text_surface, text_rect)

        # Draw column indices along the top edge
        for x in range(self.board_size):
            text_surface = self.small_font.render(str(x), True, self.font_color)
            text_rect = text_surface.get_rect(centerx=(x * self.cell_size + index_offset_x + self.cell_size // 2), top=5)
            self.screen.blit(text_surface, text_rect)

    def draw_text_centered(self, text, font, color, rect):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def update_log_scroll(self, amount):
        # This method updates the log_scroll_pos based on the amount of scroll steps (lines), not pixels
        scroll_steps = amount  # Here amount is in terms of steps or lines, not pixels
        self.log_scroll_pos += scroll_steps
        self.log_scroll_pos = max(0, min(self.log_scroll_pos, len(self.move_history) - self.visible_count))

    def draw_log(self, surface):
        # Define how many moves can be visible at once based on your surface height
        log_label = self.small_font.render('Move Log', True, self.font_color)
        surface.blit(log_label, (10, 0))  # Draw the log label at the top

        start_index = self.log_scroll_pos
        end_index = start_index + self.visible_count

        reversed_move_history = list(reversed(self.move_history))  # Reverse the entire move history
        visible_moves = reversed_move_history[start_index:end_index]  # Make sure you get the right slice of the move history to display

        # Draw each of the visible moves
        for i, text in enumerate(reversed(visible_moves)):
            move_surf = self.small_font.render(text, True, self.font_color)
            y_position = 30 + (self.visible_count - i) * (self.small_font.get_height())  # Calculate y position
            surface.blit(move_surf, (10, y_position))

game = BoardGame()
game.run()
