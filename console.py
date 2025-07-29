class Console:
    def __init__(self, game, game_mode, ai1_algo=None, ai2_algo=None):
        self.game = game
        self.game_mode = game_mode
        self.ai1_algo = ai1_algo or "alphabeta"
        self.ai2_algo = ai2_algo or "minimax"
        self.ai1 = game.AI
        self.ai2 = game.HUMAN
    def run(self):
        if self.game_mode == "ai_vs_ai":
            self._run_ai_vs_ai()
        elif self.game_mode == "human_vs_human":
            self._run_human_vs_human()
        else:
            self._run_human_vs_ai()
    def _run_human_vs_human(self):
        print("Gomoku - Human vs Human")
        while True:
            self._print_board()
            winner = self.game.checkWinner()
            if winner != 0:
                self._print_result(winner)
                break
            if self.check_tie():
                print("Tie")
                break
            player = "Player 1" if self.game.curr_player == self.game.AI else "Player 2"
            print(f"{player}'s turn")
            self._human_turn()
    def _run_human_vs_ai(self):
        print(f"Gomoku - Human vs AI ({self.ai1_algo.title()})")
        print(f"You are playing as O on {self.game.width}x{self.game.height} board\n")
        while True:
            self._print_board()
            winner = self.game.checkWinner()
            if winner != 0:
                self._print_result(winner)
                break
            if self.check_tie():
                print("Tie")
                break
            if self.game.curr_player == self.game.HUMAN:
                self._human_turn()
            else:
                self._ai_turn()

    def check_tie(self):
        for i in range(self.game.width*self.game.height):
            tempi = i//self.game.height
            tempj = i%self.game.height
            if self.game.board[tempi][tempj] == 0:
                return False
        return True
    def _run_ai_vs_ai(self):
        print(f"Gomoku - AI ({self.ai1_algo.title()}) vs AI ({self.ai2_algo.title()})\n")
        print(f"Board size: {self.game.width}x{self.game.height}")
        while True:
            self._print_board()
            winner = self.game.checkWinner()
            if winner != 0:
                self._print_result(winner)
                break
            if self.check_tie():
                    print("Tie")
                    break
            if self.game.curr_player == self.ai1:
                algo = self.ai1_algo
                ai_name = f"AI 1 ({algo.title()})"
            else:
                algo = self.ai2_algo
                ai_name = f"AI 2 ({algo.title()})"

            print(f"{ai_name} is thinking...")
            if algo == "alphabeta":
                _, move = self.game.alphabeta(2, -float('inf'), float('inf'), True)
            else:
                _, move = self.game.minimax(2, True)

            self._make_ai_move(move, self.game.curr_player, ai_name)

    def _human_turn(self):
        max_index = self.game.width - 1
        while True:
            try:
                prompt = f"Enter your move (row,col 0-{max_index}): "
                move = input(prompt).strip().split(',')
                if len(move) != 2:
                    raise ValueError

                row, col = int(move[0]), int(move[1])
                if not self.game.checkValidation(row, col):
                    print(f"Coordinates must be between 0-{max_index}")
                    continue

                if self.game.board[row][col] != 0:
                    print("Position already occupied! Try again.")
                    continue

                if self.game_mode == "human_vs_ai":
                    self.game.makeMove((row, col), self.game.HUMAN)
                else:
                    self.game.makeMove((row, col), self.game.curr_player)
                break

            except (ValueError, IndexError):
                print(f"Invalid input! Use format: row,col (e.g., {max_index // 2},{max_index // 2})")
            except KeyboardInterrupt:
                print("\nGame interrupted. Exiting...")
                exit(0)  # Graceful

    def _ai_turn(self):
        print("\nAI is thinking...")
        _, best_move = self.game.alphabeta(3, -float('inf'), float('inf'), True)
        if best_move:
            self.game.makeMove(best_move, self.game.AI)
            print(f"AI plays at {best_move}\n")
        else:
            print("AI has no valid moves!")

    def _make_ai_move(self, move, player, ai_name):
        if move:
            self.game.makeMove(move, player)
            print(f"{ai_name} plays at {move}\n")
        else:
            print(f"{ai_name} has no valid moves!")

    def _print_board(self):
        print("\nCurrent Board:")
        for i, row in enumerate(self.game.board):
            print(f"{i:2}", end='  ')
            print(' '.join([' . ' if cell == 0 else ' X ' if cell == self.game.AI else ' O ' for cell in row]))

        col_numbers = [f" {i:2} " for i in range(self.game.width)]
        print("   " + ''.join(col_numbers))
        print()

    def _print_result(self, winner):
        self._print_board()
        if winner == self.game.AI:
            if self.game_mode == "ai_vs_ai":
                print(f"AI 1 ({self.ai1_algo.title()}) wins!")
            else:
                print(f"AI ({self.ai1_algo.title()}) wins!")
        elif winner == self.game.HUMAN:
            if self.game_mode == "ai_vs_ai":
                print(f"AI 2 ({self.ai2_algo.title()}) wins!")
            else:
                print("Human (O) wins!")
        else:
            print("It's a draw!")

    def _check_draw(self):
        return all(cell != 0 for row in self.game.board for cell in row)