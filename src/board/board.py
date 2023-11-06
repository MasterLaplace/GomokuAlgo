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

    def run(self):
        while not self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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

    def handle_setup_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not self.start_button_active:
                if self.input_text.isdigit() and 0 < int(self.input_text) <= 20:
                    self.board_size = int(self.input_text)
                    self.start_button_active = True
                else:
                    print("Please enter a valid board size (1-20).")
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if event.unicode.isdigit() and len(self.input_text) < 3:
                    self.input_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN and self.start_button_active:
            if self.start_button.collidepoint(event.pos):
                self.game_started = True

    def run_game(self):
        self.game_width = self.board_size * self.cell_size
        self.total_width = self.game_width + self.log_width  # Update total width
        self.game_height = self.game_width  # Making the height equal to the game width for a square board
        self.screen = pygame.display.set_mode((self.total_width, self.game_height))
        while self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_game_event(event)

            self.draw_board_screen()
        
    def handle_game_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if event.pos[0] < self.game_width:
                    x, y = event.pos[0] // self.cell_size, event.pos[1] // self.cell_size
                    # Add point if the cell is empty
                    if self.game_matrix[y][x] is None:
                        self.game_matrix[y][x] = self.current_player
                        self.move_history.append(f"- {self.move} : p{self.current_player + 1}: ({x}, {y})")
                        self.current_player = (self.current_player + 1) % 2  # Switch players
                        self.move += 1
            elif event.button == 4:  # Mouse wheel up
                self.log_scroll_pos = max(self.log_scroll_pos - 1, 0)
            elif event.button == 5:  # Mouse wheel down
                max_scroll_pos = max(0, len(self.move_history) - (self.game_height // (self.small_font.get_height() + 5)))
                self.log_scroll_pos = min(self.log_scroll_pos + 1, max_scroll_pos)
                
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

        pygame.display.flip()
        self.clock.tick(30)

    def draw_board_screen(self):
        # Draw the game board and the log side by side
        self.screen.fill(self.bg_color)
        
        # Draw the board on its own part of the screen
        board_surf = pygame.Surface((self.game_width, self.game_height))
        board_surf.fill(self.bg_color)
        for y in range(self.board_size):
            for x in range(self.board_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(board_surf, self.board_color, rect, 1)
                if self.game_matrix[y][x] is not None:
                    # Draw the player's piece on the board
                    pygame.draw.circle(board_surf, self.player_colors[self.game_matrix[y][x]], rect.center, self.cell_size // 3)

        # Blit the board surface onto the screen
        self.screen.blit(board_surf, (0, 0))
        
        # Draw the log on its own part of the screen
        log_surf = pygame.Surface((self.log_width, self.game_height))
        log_surf.fill(self.bg_color)
        self.draw_log(log_surf)
        self.screen.blit(log_surf, (self.game_width, 0))  # Position the log surface to the right of the board

        pygame.display.flip()
        self.clock.tick(30)
        
    def draw_text_centered(self, text, font, color, rect):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_log(self, surface):
        # Method to draw the log of moves
        log_label = self.small_font.render('Move Log', True, self.font_color)
        surface.blit(log_label, (10, 5))  # Draw the log label at the top
        start_index = self.log_scroll_pos
        end_index = start_index + (self.game_height // (self.small_font.get_height() + 5))
        
        for i, text in enumerate(self.move_history[start_index:end_index]):  # Show only visible moves
            move_surf = self.small_font.render(text, True, self.font_color)
            surface.blit(move_surf, (10, 30 + i * (self.small_font.get_height() + 5)))

game = BoardGame()
game.run()
