# mode_selector.py
import tkinter as tk
from tkinter import ttk
from gameplay import gamePlay
from gomoku_gui import GomokuGUI

class ModeSelector:
    def __init__(self, master):
        self.master = master
        self.master.title("Gomoku - Select Mode")
        self.mode_var = tk.StringVar(value="human_vs_ai")
        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        ttk.Label(main_frame, text="Select Game Mode:", font=('Arial', 12)).pack(pady=10)
        modes = [("Human vs AI (Alpha-Beta)", "human_vs_ai"), ("AI (Minimax) vs AI (Alpha-Beta)", "ai_vs_ai")]
        for text, mode in modes:
            ttk.Radiobutton(main_frame, text=text, variable=self.mode_var, value=mode).pack(anchor=tk.W, pady=5)
        ttk.Button(main_frame, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        self.master.destroy()
        root = tk.Tk()
        game = gamePlay()
        GomokuGUI(root, game, self.mode_var.get())
        root.mainloop()
