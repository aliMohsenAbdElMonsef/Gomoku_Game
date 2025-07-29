class gamePlay:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.AI = 1
        self.HUMAN = 2
        self.board = [[0] * self.width for _ in range(self.height)]
        self.moves8 = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        self.dirs = [(1,0),(1,1),(1,-1),(0,1)]
        self.last_move = None
        self.curr_player = self.AI

    def checkValidation(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def playround(self, move, round):
        x, y = move
        self.board[x][y] = self.AI if round == self.AI else self.HUMAN
        self.last_move = (x, y)

    def checkWinner(self):
        if not self.last_move:
            return 0
        x, y = self.last_move
        player = self.board[x][y]
        if self.is_winning_move(self.last_move, player):
            return player
        return 0

    def generateMoves(self):
        candidates = set()
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    for dx, dy in self.moves8:
                        nx, ny = row + dx, col + dy
                        if self.checkValidation(nx, ny) and self.board[nx][ny] == 0:
                            candidates.add((nx, ny))
        if not candidates:
            for row in range(self.height):
                for col in range(self.width):
                    if self.board[row][col] == 0:
                        candidates.add((row, col))
        if not candidates and self.board[self.height // 2][self.width // 2] == 0:
            candidates.add((self.height // 2, self.width // 2))
        scored = []
        for (x, y) in candidates:
            score = 0
            if self.is_winning_move((x, y), self.AI):
                score += 1000000
            if self.is_winning_move((x, y), self.HUMAN):
                score += 500000
            for dx, dy in self.dirs:
                score += self.score_position((x, y), dx, dy, self.AI)
                score += self.score_position((x, y), dx, dy, self.HUMAN)
            scored.append((score, x, y))

        scored.sort(reverse=True, key=lambda s: s[0])
        return [(x, y) for (_, x, y) in scored[:40]]
    def score_position(self, pos, dx, dy, player):
        x, y = pos
        score = 0
        sequence = []
        for i in range(-4, 5):
            nx = x + dx * i
            ny = y + dy * i
            if self.checkValidation(nx, ny):
                cell = self.board[nx][ny]
                if cell == player:
                    sequence.append(1)
                elif cell == 0:
                    sequence.append(0)
                else:
                    sequence.append(-1)
            else:
                sequence.append(-2)
        for i in range(4, len(sequence) - 4):
            window = sequence[i - 4:i + 5]
            player_count = window.count(1)
            empty_count = window.count(0)

            if player_count == 4 and empty_count >= 1:
                score += 1000
            elif player_count == 3 and empty_count >= 2:
                score += 100
            elif player_count == 2 and empty_count >= 3:
                score += 10

        return score
    def makeMove(self, move, player):
        x, y = move
        self.board[x][y] = player
        self.curr_player = 3-player
        self.last_move = (x, y)

    def undoMove(self, move):
        x, y = move
        self.board[x][y] = 0

    def is_winning_move(self, move, player):
        x, y = move
        for dx, dy in self.dirs:
            count = 1
            nx, ny = x + dx, y + dy
            while self.checkValidation(nx, ny) and self.board[nx][ny] == player:
                count += 1
                nx += dx
                ny += dy
            nx, ny = x - dx, y - dy
            while self.checkValidation(nx, ny) and self.board[nx][ny] == player:
                count += 1
                nx -= dx
                ny -= dy
            if count >= 5:
                return True
        return False
    def evaluate(self):
        winner = self.checkWinner()
        if winner == self.AI:
            return 10 ** 7
        elif winner == self.HUMAN:
            return -10 ** 7

        ai_weights = {
            (4, 2): 10 ** 6,
            (4, 1): 10 ** 5,
            (3, 2): 10 ** 4,
            (3, 1): 10 ** 3,
            (2, 2): 10 ** 2,
            (2, 1): 10,
        }

        human_weights = {
            (4, 2): 10 ** 7,
            (4, 1): 10 ** 6,
            (3, 2): 10 ** 5,
            (3, 1): 10 ** 4,
            (2, 2): 10 ** 3,
            (2, 1): 10 ** 2,
        }

        def score_player(player):
            total = 0
            current_weights = ai_weights if player == self.AI else human_weights
            for i in range(self.width*self.height):
                    tempi = i//self.height
                    tempj = i%self.height
                    if self.checkValidation(tempi,tempj) and self.board[tempi][tempj] != player:
                        continue
                    for dx, dy in self.dirs:
                        prev_i, prev_j = tempi - dx, tempj - dy
                        if self.checkValidation(prev_i, prev_j) and self.board[prev_i][prev_j] == player:
                            continue
                        count = 1
                        ni, nj = tempi + dx, tempj + dy
                        while self.checkValidation(ni, nj) and self.board[ni][nj] == player:
                            count += 1
                            ni += dx
                            nj += dy
                        open_ends = 0
                        if self.checkValidation(prev_i, prev_j) and self.board[prev_i][prev_j] == 0:
                            open_ends += 1
                        next_i, next_j = ni, nj
                        if self.checkValidation(next_i, next_j) and self.board[next_i][next_j] == 0:
                            open_ends += 1
                        if count >= 5:
                            continue
                        total += current_weights.get((count, open_ends), 0)
            return total

        ai_score = score_player(self.AI)
        human_score = score_player(self.HUMAN)
        return ai_score - human_score

    def minimax(self, depth, maximizing):
        if depth == 0 or self.checkWinner() != 0:
            return self.evaluate(), None

        best_move = None
        if maximizing:
            max_eval = -float('inf')
            for move in self.generateMoves():
                original_last_move = self.last_move
                original_curr_player = self.curr_player
                self.makeMove(move, self.AI)
                eval_score, _ = self.minimax(depth - 1, False)
                self.undoMove(move)
                self.curr_player = original_curr_player
                self.last_move = original_last_move
                if eval_score > max_eval:
                    max_eval, best_move = eval_score, move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.generateMoves():
                original_last_move = self.last_move
                original_curr_player = self.curr_player
                self.makeMove(move, self.HUMAN)
                eval_score, _ = self.minimax(depth - 1, True)
                self.undoMove(move)
                self.curr_player = original_curr_player
                self.last_move = original_last_move
                if eval_score < min_eval:
                    min_eval, best_move = eval_score, move
            return min_eval, best_move

    def alphabeta(self, depth, alpha, beta, maximizing):
        if depth == 0 or self.checkWinner() != 0:
            return self.evaluate(), None
        best_move = None
        if maximizing:
            max_eval = -float('inf')
            for move in self.generateMoves():
                original_last_move = self.last_move
                original_curr_player = self.curr_player
                self.makeMove(move, self.AI)
                eval_score, _ = self.alphabeta(depth - 1, alpha, beta, False)
                self.undoMove(move)
                self.curr_player = original_curr_player
                self.last_move = original_last_move
                if eval_score > max_eval:
                    max_eval, best_move = eval_score, move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.generateMoves():
                original_last_move = self.last_move
                original_curr_player = self.curr_player
                self.makeMove(move, self.HUMAN)
                eval_score, _ = self.alphabeta(depth - 1, alpha, beta, True)
                self.undoMove(move)
                self.curr_player = original_curr_player
                self.last_move = original_last_move
                if eval_score < min_eval:
                    min_eval, best_move = eval_score, move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def print_board(self):
        for row in self.board:
            print(' '.join(['.' if cell==0 else ('X' if cell==self.AI else 'O') for cell in row]))
        print()