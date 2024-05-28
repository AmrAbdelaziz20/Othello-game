# George issa - Amr Abdelaziz - mohamed hany (section IS 5 - 6 )
# 20211027    - 20210277      - 20210358
import tkinter as tk
from tkinter import messagebox
import random
import time 
# Constants
GRID_SIZE = 8

class Othello_game:
    def __init__(self, master):
        self.master = master
        self.master.title("King Othello Game")
        self.current_player = 2  # Player 2 (Black) starts first
        self.skip_counter = 0

        # Create menu
        self.create_menu()

    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        play_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Play", menu=play_menu)
        play_menu.add_command(label="Play against Human", command=self.start_human_game)
        play_menu.add_command(label="Play against Computer", command=self.choose_difficulty)

    def start_human_game(self):
        # Start the game against another human
        self.game = Othello_grid(self.master, computer_mode=False)

    def choose_difficulty(self):
        # Ask for difficulty level
        difficulty_menu = tk.Toplevel(self.master)
        difficulty_menu.title("Choose Difficulty")

        label = tk.Label(difficulty_menu, text="Select AI Difficulty:")
        label.pack(pady=10)

        easy_button = tk.Button(difficulty_menu, text="Easy", command=lambda: self.start_computer_game("Easy"))
        easy_button.pack()

        medium_button = tk.Button(difficulty_menu, text="Medium", command=lambda: self.start_computer_game("Medium"))
        medium_button.pack()

        hard_button = tk.Button(difficulty_menu, text="Hard", command=lambda: self.start_computer_game("Hard"))
        hard_button.pack()

    def start_computer_game(self, difficulty):
        # Start the game against the computer with the chosen difficulty
        self.game = Othello_grid(self.master, computer_mode=True, difficulty=difficulty)

class Othello_grid:
    def __init__(self, master, computer_mode=False, difficulty="Easy"):
        self.master = master
        self.computer_mode = computer_mode
        self.difficulty = difficulty
        self.current_player = 2  # Initialize current player (Player 2 starts first in Othello)
        self.move_counter = {1: 0, 2: 0}  # Initialize move counter for each player

        # Create canvas to display the game board
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        # Create label to display piece count
        self.piece_count_label = tk.Label(self.master, text="White: 2 | Black: 2", font=("Arial", 12))
        self.piece_count_label.pack(fill=tk.X, padx=10, pady=5)

        # Initialize game grid
        self.grid = self.create_grid()

        # Draw initial board
        self.draw_board()

        # Bind click event to canvas
        self.canvas.bind("<Button-1>", self.on_click)

        # Start AI if in computer mode and it's AI's turn
        if self.computer_mode and self.current_player == 2:
            self.ai_move()
        else:
            self.draw_valid_moves()
            
            
    def create_grid(self):
        grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        grid[3][3] = 1  # White
        grid[3][4] = 2  # Black
        grid[4][3] = 2  # Black
        grid[4][4] = 1  # White
        return grid

    def draw_board(self):
        self.canvas.delete("pieces")
        cell_size = 400 // GRID_SIZE

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1, y1 = col * cell_size, row * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size

                # Draw board cell
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#009067", outline="black")

                # Draw game pieces
                if self.grid[row][col] == 1:  # White piece
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white", outline="black", tags="pieces")
                elif self.grid[row][col] == 2:  # Black piece
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black", outline="black", tags="pieces")

        # Update piece count label
        white_count, black_count = self.black_white_sum()
        self.piece_count_label.config(text=f"White: {white_count} | Black: {black_count}")

        valid_moves_exist = any(self.if_moves_valid(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE))

        if not valid_moves_exist:
            # No valid moves for current player
            self.skip_counter += 1
            messagebox.showinfo("No Valid Moves", f"Player {'Black' if self.current_player == 2 else 'White'} has no valid moves!")
            
            # Switch player
            self.current_player = 3 - self.current_player

            # Check if both players have skipped
            if self.skip_counter == 2:
                self.game_end("No more Valid Moves")  # Game ends in draw
            else:
                # Redraw board for the other player
                self.draw_board()
            
                if self.computer_mode and self.current_player == 2:
                    
                    self.ai_move()
                                     # AI's turn
                # Redraw board for the other player
            return

        # Reset skip counter if valid moves exist
        self.skip_counter = 0

        if not self.computer_mode or (self.computer_mode and self.current_player == 1):
            self.draw_valid_moves()
     
    def draw_valid_moves(self):
        # Clear any existing X marks
        self.canvas.delete("valid_moves")

        cell_size = 400 // GRID_SIZE

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.if_moves_valid(row, col):
                    x1, y1 = col * cell_size, row * cell_size
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    # Draw faded X mark
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="X", font=("Arial", 20, "bold"), fill="gray", tags="valid_moves")

    def on_click(self, event):
        if self.computer_mode and self.current_player == 2:
            return  # Block human input during computer's turn

        cell_size = 400 // GRID_SIZE
        row = event.y // cell_size
        col = event.x // cell_size

        if self.if_moves_valid(row, col):
            self.game_move(row, col)
            self.move_counter[self.current_player] += 1  # Increment move counter
            self.current_player = 3 - self.current_player  # Switch player
            self.draw_board()

            # Update piece count label with remaining moves for each player
            white_moves_left = 30 - self.move_counter[1]
            black_moves_left = 30 - self.move_counter[2]
            
            # Check for end of game or max moves
            if not any(self.if_moves_valid(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
                self.game_end("No more Valid Moves")
            elif self.move_counter[1] >= 30 or self.move_counter[2] >= 30:
                self.game_end("Max moves reached")
            else:
                if self.computer_mode and self.current_player == 2:
                    self.delay_ai_move()
                    self.move_counter[self.current_player] += 1 


        else:
            messagebox.showinfo("Invalid Move", "This move is not valid. Please try again.")
        self.piece_count_label.config(text=f"White: {white_moves_left} moves left | Black: {black_moves_left} moves left") 

    def if_moves_valid(self, row, col):
        # Check if move is valid
        if self.grid[row][col] != 0:
            return False

        for row_index in range(-1, 2):
            for col_index in range(-1, 2):
                if row_index == 0 and col_index == 0 or abs(row_index) == abs(col_index):
                    continue
                r, c = row + row_index, col + col_index
                while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.grid[r][c] == 3 - self.current_player:
                    r += row_index
                    c += col_index
                    if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.grid[r][c] == self.current_player:
                        return True
        return False

    def game_move(self, row, col):
        self.grid[row][col] = self.current_player

        for row_index in range(-1, 2):
            for col_index in range(-1, 2):
                if row_index == 0 and col_index == 0 or abs(row_index) == abs(col_index):
                    continue
                r, c = row + row_index, col + col_index
                while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.grid[r][c] == 3 - self.current_player:
                    r += row_index
                    c += col_index
                    if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.grid[r][c] == self.current_player:
                        r, c = row + row_index, col + col_index
                        while self.grid[r][c] == 3 - self.current_player:
                            self.grid[r][c] = self.current_player
                            r += row_index
                            c += col_index

    def black_white_sum(self):
        white_count = sum(row.count(1) for row in self.grid)
        black_count = sum(row.count(2) for row in self.grid)
        return white_count, black_count

    def alfa_peta(self, grid, player, depth, alpha, beta):
        if depth == 0 or not any(self.if_moves_valid(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE)):
            white_count, black_count = self.black_white_sum()
            return None, black_count if player == 2 else white_count

        best_move = None

        if player == 2:  # Maximize for Black player (current_player = 2)
            value = float('-inf')
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if self.if_moves_valid(row, col):
                        grid_cpy = [row[:] for row in grid]
                        _, new_value = self.alfa_peta(grid_cpy, 3 - player, depth - 1, alpha, beta)
                        if new_value > value:
                            value = new_value
                            best_move = (row, col)
                        alpha = max(value, alpha)
                        if alpha >= beta:
                            break
            return best_move, value

        else:  # Minimize for White player (current_player = 1)
            value = float('inf')
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if self.if_moves_valid(row, col):
                        grid_cpy = [row[:] for row in grid]
                        _, new_value = self.alfa_peta(grid_cpy, 3 - player, depth - 1, alpha, beta)
                        if new_value < value:
                            value = new_value
                            best_move = (row, col)
                        beta = min(value, beta)
                        if alpha >= beta:
                            break
            return best_move, value
    
    def delay_ai_move(self):
            self.master.after(1000, self.ai_move)

    def Easy_Ai(self, grid, player):
        return self.alfa_peta(grid, player, 1, float('-inf'), float('inf'))

    def Medium_Ai(self, grid, player):
        return self.alfa_peta(grid, player, 3, float('-inf'), float('inf'))

    def Expert_Ai(self, grid, player):
        return self.alfa_peta(grid, player, 5, float('-inf'), float('inf'))

    def ai_move(self):
        if self.difficulty == "Easy":
            move, _ = self.Easy_Ai(self.grid, self.current_player)
        elif self.difficulty == "Medium":
            move, _ = self.Medium_Ai(self.grid, self.current_player)
        elif self.difficulty == "Hard":
            move, _ = self.Expert_Ai(self.grid, self.current_player)

        if move:
            self.game_move(move[0], move[1])
            self.current_player = 3 - self.current_player  # Switch player
            
            self.draw_board()
            # Check for end of game
            if not any(self.if_moves_valid(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
                self.game_end("No more Valid Moves")
                #messagebox.showinfo("check2")
            
    def game_end(self, result):
        white_count, black_count = self.black_white_sum()
        if black_count>white_count:
            messagebox.showinfo("Black wins")
        elif black_count<white_count:
            messagebox.showinfo("White wins")      
        else: 
            messagebox.showinfo("Draw")      
        #messagebox.showinfo("Game Over", f"Game Over!\n{result}\nWhite: {white_count} | Black: {black_count}")

def play():
    root = tk.Tk()
    game = Othello_game(root)
    root.mainloop()

if __name__ == "__main__":
    play()



