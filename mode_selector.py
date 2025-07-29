import tkinter as tk
from tkinter import ttk
from gameplay import gamePlay
from gomoku_gui import GomokuGUI
from console import Console

class ModeSelector(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Gomoku - Brilliant Settings")
        self.master.geometry("500x450")
        self.master.configure(bg='#1a1a1a')
        self.pack(expand=True, fill=tk.BOTH)
        self._apply_styles()
        self.create_widgets()

    def _apply_styles(self):
        style = ttk.Style(self.master)
        style.theme_use('clam')
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TLabel', background='#1a1a1a', foreground='#E0E0E0', font=('Helvetica', 12, 'bold'))
        style.configure('TButton', foreground='#FFFFFF', background='#5A5AEB', font=('Helvetica', 11, 'bold'), padding=8)
        style.map('TButton', background=[('active','#7F7FF1')])
        style.configure('TCombobox', fieldbackground='#2e2e4f', background='#2e2e4f', foreground='#FFFFFF', arrowcolor='#FFFFFF')
        style.configure('TRadiobutton', background='#1a1a1a', foreground='#FF9CDA', font=('Helvetica', 11))
        style.map('TRadiobutton', background=[('selected','#2e2e4f')])

    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Gomoku Configuration", font=('Helvetica', 16)).pack(pady=(0,10))
        ttk.Label(frame, text="Grid Size:").pack(anchor=tk.W)
        self.size_var = tk.StringVar(value="15")
        size_combo = ttk.Combobox(
            frame, textvariable=self.size_var,
            values=["5", "15", "19"], state="readonly", width=10
        )
        size_combo.pack(anchor=tk.W, pady=5)
        ttk.Label(frame, text="Game Mode:").pack(anchor=tk.W, pady=(10,0))
        self.mode_var = tk.StringVar(value="human_vs_ai")
        for text, mode in [("Human vs AI", "human_vs_ai"), ("AI vs AI", "ai_vs_ai"),("Human vs Human", "human_vs_human")]:
            ttk.Radiobutton(
                frame, text=text, variable=self.mode_var, value=mode
            ).pack(anchor=tk.W)
        self.ai_frame = ttk.Frame(frame)
        ttk.Label(self.ai_frame, text="AI 1 Algorithm:").pack(side=tk.LEFT)
        self.ai1_var = tk.StringVar(value="alphabeta")
        ttk.Combobox(
            self.ai_frame, textvariable=self.ai1_var,
            values=["alphabeta", "minimax"], width=12
        ).pack(side=tk.LEFT, padx=5)
        ttk.Label(self.ai_frame, text="AI 2 Algorithm:").pack(side=tk.LEFT, padx=(20,0))
        self.ai2_var = tk.StringVar(value="minimax")
        ttk.Combobox(
            self.ai_frame, textvariable=self.ai2_var,
            values=["alphabeta", "minimax"], width=12
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(frame, text="Interface:").pack(anchor=tk.W, pady=(10,0))
        self.interface_var = tk.StringVar(value="gui")
        for text, val in [("Graphical (GUI)", "gui"), ("Text (Console)", "console")]:
            ttk.Radiobutton(
                frame, text=text, variable=self.interface_var, value=val
            ).pack(anchor=tk.W)
        ttk.Button(
            frame, text="Start Game", command=self.start_game
        ).pack(pady=20, ipadx=10)
        self.mode_var.trace_add('write', self.toggle_ai_selection)
        self.toggle_ai_selection()

    def toggle_ai_selection(self, *args):
        if self.mode_var.get() == "ai_vs_ai":
            self.ai_frame.pack(pady=10, fill=tk.X)
        else:
            self.ai_frame.pack_forget()

    def start_game(self):
        size = int(self.size_var.get())
        interface = self.interface_var.get()
        game_mode = self.mode_var.get()
        ai1_algo = self.ai1_var.get() if game_mode == "ai_vs_ai" else None
        ai2_algo = self.ai2_var.get() if game_mode == "ai_vs_ai" else None
        self.master.destroy()
        game = gamePlay(size, size)
        if game_mode == "human_vs_human":
            game.curr_player = game.AI
        if interface == "gui":
            root = tk.Tk()
            GomokuGUI(root, game, game_mode, ai1_algo, ai2_algo)
            root.mainloop()
        else:
            Console(game, game_mode, ai1_algo, ai2_algo).run()


