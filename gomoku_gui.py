import tkinter as tk
from tkinter import ttk, messagebox


class GomokuGUI:
    def __init__(self, master, game, mode, ai1_algo=None, ai2_algo=None):
        self.master = master
        self.game = game
        self.mode = mode
        self.ai1_algo = ai1_algo or "alphabeta"
        self.ai2_algo = ai2_algo or "minimax"
        max_dimension = max(self.game.width, self.game.height)
        self.cell_size = min(40, 600 // max_dimension)
        self.canvas_size = self.game.width * self.cell_size
        self.stone_size = self.cell_size // 3
        self.ai_delay = 500
        self.current_ai = "ai1"
        self.paused = False
        self.bg_color = '#2D2D2D'
        self.light_square = '#3D3D3D'
        self.dark_square = '#2D2D2D'
        self.text_color = '#FFFFFF'
        self.master.title(self.get_window_title())
        self.master.resizable(False, False)
        self.master.configure(bg=self.bg_color)
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TButton', background=self.light_square, foreground=self.text_color, padding=5, font=('Arial', 10))
        self.canvas = tk.Canvas(
            self.master,
            width=self.canvas_size,
            height=self.canvas_size,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        self.status_label = ttk.Label(
            self.master,
            text=self.get_status_text(),
            font=('Arial', 12, 'bold')
        )
        self.status_label.pack()
        control_frame = ttk.Frame(self.master)
        control_frame.pack(pady=10)
        ttk.Button(
            control_frame,
            text="New Game",
            command=self.reset_game
        ).pack(side=tk.LEFT, padx=5)

        if self.mode == "ai_vs_ai":
            self.pause_btn = ttk.Button(
                control_frame,
                text="Pause",
                command=self.toggle_pause
            )
            self.pause_btn.pack(side=tk.LEFT, padx=5)
        self.draw_board()
        if self.mode == "human_vs_ai":
            self.canvas.bind("<Button-1>", self.human_move)
            self.ai_turn()
        elif self.mode == "ai_vs_ai":
            self.master.after(self.ai_delay, self.ai_vs_ai_turn)
        else:
            self.canvas.bind("<Button-1>", self.human_move)
        self.switch_btn = ttk.Button(
            control_frame,
            text="Switch to AI vs AI",
            command=self.switch_to_ai_vs_ai
        )
        if self.mode != "ai_vs_ai":
            self.switch_btn.pack(side=tk.LEFT, padx=5)

    def switch_to_ai_vs_ai(self):
        self.ai1_algo = "alphabeta"
        self.ai2_algo = "minimax"
        if self.mode == "human_vs_human":
            if self.game.curr_player == self.game.HUMAN:
                self.current_ai = "ai2"
            else:
                self.current_ai = "ai1"
        else:
            if self.game.curr_player == self.game.HUMAN:
                self.current_ai = "ai1"
            else:
                self.current_ai = "ai2"
        self.mode = "ai_vs_ai"
        self.paused = False
        self.status_label.config(text=f"AI ({self.ai1_algo.title()}) Turn")
        self.ai_vs_ai_turn()
        self.switch_btn.pack_forget()

    def get_window_title(self):
        titles = {
            "human_vs_ai": f"Human vs AI ({self.ai1_algo.title()})",
            "ai_vs_ai": f"AI ({self.ai1_algo.title()}) vs AI ({self.ai2_algo.title()})",
            "human_vs_human": "Human vs Human"
        }
        return titles[self.mode]

    def get_status_text(self):
        if self.mode == "human_vs_human":
            return "Player 1's Turn" if self.game.curr_player == self.game.AI else "Player 2's Turn"
        elif self.mode == "human_vs_ai":
            return "Player's Turn"
        else:
            current_algo = self.ai1_algo if self.current_ai == "ai1" else self.ai2_algo
            return f"AI ({current_algo.title()}) Turn"

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.game.width):
            x = i * self.cell_size + self.cell_size // 2
            self.canvas.create_line(
                x, self.cell_size // 2,
                x, self.canvas_size - self.cell_size // 2
            )
        for i in range(self.game.height):
            y = i * self.cell_size + self.cell_size // 2
            self.canvas.create_line(
                self.cell_size // 2, y,
                self.canvas_size - self.cell_size // 2, y
            )
        for i in range(self.game.height):
            for j in range(self.game.width):
                if self.game.board[i][j] != 0:
                    self.draw_stone(i, j)

    def draw_stone(self, row, col):
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        color = 'black' if self.game.board[row][col] == self.game.AI else 'white'
        self.canvas.create_oval(
            x - self.stone_size,
            y - self.stone_size,
            x + self.stone_size,
            y + self.stone_size,
            fill=color,
            outline='black'
        )
    def human_move(self, event):
        if self.game.checkWinner() != 0 or self.paused:
            return
        col = (event.x - self.cell_size // 2) // self.cell_size
        row = (event.y - self.cell_size // 2) // self.cell_size

        if self.game.checkValidation(row, col) and self.game.board[row][col] == 0:
            if self.mode == "human_vs_human":
                player = self.game.curr_player
                self.game.curr_player = 3 - player
                self.status_label.config(text=self.get_status_text())
            else:
                player = self.game.HUMAN
            self.game.playround((row, col), player)
            self.draw_stone(row, col)
            self.check_game_status()
            if self.mode == "human_vs_ai":
                self.ai_turn()

    def ai_turn(self):
        if not self.master.winfo_exists():
            return
        if not self.master.winfo_exists():
            return

        if self.game.checkWinner() != 0 or self.paused:
            return
        try:
            if self.status_label.winfo_exists():
                self.status_label.config(text="AI is thinking...")
                self.master.update()
        except tk.TclError:
            return

        try:
            _, best_move = self.game.alphabeta(3, -float('inf'), float('inf'), True)
        except Exception as e:
            print(f"Error during AI move: {e}")
            return

        if best_move:
            row, col = best_move
            self.game.playround(best_move, self.game.AI)
            self.draw_stone(row, col)
            self.check_game_status()
            try:
                if (self.game.checkWinner() == 0 and
                        not self.paused and
                        self.status_label.winfo_exists()):
                    self.status_label.config(text="Player's Turn")
            except tk.TclError:
                pass

    def ai_vs_ai_turn(self):
        if not self.master.winfo_exists() or self.paused or self.game.checkWinner() != 0:
            return
        if self.paused or self.game.checkWinner() != 0:
            return
        if self.current_ai == "ai1":
            algorithm = self.ai1_algo
            player = self.game.AI
            next_ai = "ai2"
        else:
            algorithm = self.ai2_algo
            player = self.game.HUMAN
            next_ai = "ai1"

        self.status_label.config(text=f"AI ({algorithm.title()}) is thinking...")
        self.master.update()

        if algorithm == "alphabeta":
            _, best_move = self.game.alphabeta(2, -float('inf'), float('inf'), True)
        else:
            _, best_move = self.game.minimax(2, True)

        if best_move:
            row, col = best_move
            self.game.playround(best_move, player)
            self.draw_stone(row, col)
            self.current_ai = next_ai
            self.check_game_status()
        if self.master.winfo_exists():
            self.master.after(self.ai_delay, self.ai_vs_ai_turn)

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.config(text="Resume" if self.paused else "Pause")
        if not self.paused and self.mode == "ai_vs_ai":
            self.ai_vs_ai_turn()

    def check_game_status(self):
        if not self.master.winfo_exists():
            return
        winner = self.game.checkWinner()
        try:
            if winner != 0:
                winner_text = {
                    self.game.AI: f"AI ({self.ai1_algo.title()})" if self.mode == "ai_vs_ai" else "AI",
                    self.game.HUMAN: f"AI ({self.ai2_algo.title()})" if self.mode == "ai_vs_ai" else "Player"
                }.get(winner, "Unknown")

                if self.master.winfo_exists():
                    messagebox.showinfo("Game Over", f"{winner_text} Wins!")
                    self.reset_game()
            elif all(cell != 0 for row in self.game.board for cell in row):
                if self.master.winfo_exists():
                    messagebox.showinfo("Game Over", "It's a Tie!")
                    self.reset_game()
        except tk.TclError:
            return

    def reset_game(self):
        if self.master.winfo_exists():
            self.master.destroy()
        from mode_selector import ModeSelector
        root = tk.Tk()
        ModeSelector(root)
        root.mainloop()
