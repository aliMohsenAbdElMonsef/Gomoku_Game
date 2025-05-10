import tkinter as tk
from tkinter import ttk


class GomokuGUI:
    def __init__(self, master, game, mode):
        self.master = master
        self.game = game
        self.mode = mode
        self.cell_size = 40
        self.canvas_size = self.game.width * self.cell_size
        self.stone_size = 15
        self.ai_delay = 500
        self.current_ai = "minimax" if mode == "ai_vs_ai" else None
        self.paused = False
        self.master.title(self.get_window_title())
        self.master.resizable(False, False)
        self.canvas = tk.Canvas(self.master, width=self.canvas_size, height=self.canvas_size, bg='#EECF6D')
        self.canvas.pack(pady=10)
        self.status_label = ttk.Label(self.master, text=self.get_status_text(), font=('Arial', 12))
        self.status_label.pack()
        control_frame = ttk.Frame(self.master)
        control_frame.pack(pady=10)
        ttk.Button(control_frame, text="New Game", command=self.reset_game).pack(side=tk.LEFT, padx=5)
        if self.mode == "ai_vs_ai":
            self.pause_btn = ttk.Button(control_frame, text="Pause" if not self.paused else "Resume", command=self.toggle_pause)
            self.pause_btn.pack(side=tk.LEFT, padx=5)
        self.draw_board()
        if self.mode == "human_vs_ai":
            self.canvas.bind("<Button-1>", self.human_move)
            self.ai_turn()
        else:
            self.master.after(self.ai_delay, self.ai_vs_ai_turn)

    def get_window_title(self):
        return {"human_vs_ai": "Human vs AI (Alpha-Beta)", "ai_vs_ai": "AI (Minimax) vs AI (Alpha-Beta)"}[self.mode]

    def get_status_text(self):
        if self.mode == "human_vs_ai":
            return "Player's Turn"
        return f"AI ({self.current_ai.title()}) Turn"

    def draw_board(self):
        for i in range(self.game.width):
            x = i * self.cell_size + self.cell_size//2
            self.canvas.create_line(x, self.cell_size//2, x, self.canvas_size - self.cell_size//2)
            self.canvas.create_line(self.cell_size//2, x, self.canvas_size - self.cell_size//2, x)
        for i in range(self.game.height):
            for j in range(self.game.width):
                if self.game.board[i][j] != 0:
                    self.draw_stone(i, j)

    def draw_stone(self, row, col):
        x = col * self.cell_size + self.cell_size//2
        y = row * self.cell_size + self.cell_size//2
        color = 'black' if self.game.board[row][col] == self.game.AI else 'white'
        self.canvas.create_oval(x - self.stone_size, y - self.stone_size, x + self.stone_size, y + self.stone_size, fill=color, outline='black')

    def human_move(self, event):
        if self.game.checkWinner() != 0 or self.paused:
            return
        col = (event.x - self.cell_size//2) // self.cell_size
        row = (event.y - self.cell_size//2) // self.cell_size
        if self.game.checkValidation(row, col) and self.game.board[row][col] == 0:
            self.game.playround((row, col), self.game.HUMAN)
            self.draw_stone(row, col)
            self.check_game_status()
            self.ai_turn()

    def ai_turn(self):
        if self.game.checkWinner() != 0 or self.paused:
            return
        self.status_label.config(text="AI is thinking...")
        self.master.update()
        _, best_move = self.game.alphabeta(3, -float('inf'), float('inf'), True)
        if best_move:
            row, col = best_move
            self.game.playround(best_move, self.game.AI)
            self.draw_stone(row, col)
            print("Board after AI turn in GUI:")
            self.game.print_board()
            self.check_game_status()
            self.status_label.config(text="Player's Turn")

    def ai_vs_ai_turn(self):
        if self.paused or self.game.checkWinner() != 0:
            return
        player = self.game.AI if self.current_ai == "minimax" else self.game.HUMAN
        algorithm = self.current_ai
        self.status_label.config(text=f"AI ({algorithm.title()}) is thinking...")
        self.master.update()
        if algorithm == "minimax":
            _, best_move = self.game.minimax(2, True)
        else:
            _, best_move = self.game.alphabeta(2, -float('inf'), float('inf'), True)
        if best_move:
            row, col = best_move
            self.game.playround(best_move, player)
            self.draw_stone(row, col)
            print(f"Board after {algorithm} move:")
            self.game.print_board()
            self.current_ai = "alphabeta" if self.current_ai == "minimax" else "minimax"
            self.check_game_status()
        self.master.after(self.ai_delay, self.ai_vs_ai_turn)

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.config(text="Resume" if self.paused else "Pause")
        if not self.paused and self.mode == "ai_vs_ai":
            self.ai_vs_ai_turn()

    def check_game_status(self):
        winner = self.game.checkWinner()
        if winner != 0:
            winner_text = {self.game.AI: "AI (Minimax)" if self.mode == "ai_vs_ai" else "AI", self.game.HUMAN: "AI (Alpha-Beta)" if self.mode == "ai_vs_ai" else "Player"}[winner]
            messagebox.showinfo("Game Over", f"{winner_text} Wins!")
            self.reset_game()
        elif all(cell != 0 for row in self.game.board for cell in row):
            messagebox.showinfo("Game Over", "It's a Tie!")
            self.reset_game()

    def reset_game(self):
        self.master.destroy()
        root = tk.Tk()
        ModeSelector(root)
        root.mainloop()