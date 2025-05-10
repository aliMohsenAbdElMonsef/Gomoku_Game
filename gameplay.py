class gamePlay:
    def __init__(self):
        self.width = 15
        self.height = 15
        self.AI = 1
        self.HUMAN = 2
        self.board = [[0] * self.width for _ in range(self.height)]
        self.moves8 = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        self.dirs = [(1,0),(1,1),(1,-1),(0,1)]
        self.last_move = None

    def checkValidation(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def playround(self, move, round):
        x, y = move
        self.board[x][y] = self.AI if round == self.AI else self.HUMAN
        self.last_move = (x, y)

    def checkWinner(self):
        if self.last_move is None:
            return 0
        x, y = self.last_move
        curr = self.board[x][y]
        if curr == 0:
            return 0
        for dx, dy in self.dirs:
            count = 1
            nx, ny = x + dx, y + dy
            while self.checkValidation(nx, ny) and self.board[nx][ny] == curr:
                count += 1
                nx += dx
                ny += dy
            nx, ny = x - dx, y - dy
            while self.checkValidation(nx, ny) and self.board[nx][ny] == curr:
                count += 1
                nx -= dx
                ny -= dy
            if count >= 5:
                return curr
        return 0

    def generateMoves(self):
        candidates = set()
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] != 0:
                    for dx, dy in self.moves8:
                        nx, ny = i + dx, j + dy
                        if self.checkValidation(nx, ny) and self.board[nx][ny] == 0:
                            candidates.add((nx, ny))
        if not candidates and self.board[self.height//2][self.width//2] == 0:
            return [(self.height//2, self.width//2)]
        scored = []
        for (x, y) in candidates:
            score = 0
            for dx, dy in self.moves8:
                nx, ny = x + dx, y + dy
                if self.checkValidation(nx, ny) and self.board[nx][ny] != 0:
                    score += 1
            scored.append((score, x, y))
        scored.sort(reverse=True, key=lambda s: s[0])
        return [(x, y) for (_, x, y) in scored]

    def makeMove(self, move, player):
        x, y = move
        self.board[x][y] = player
        self.last_move = (x, y)

    def undoMove(self, move):
        x, y = move
        self.board[x][y] = 0

    def evaluate(self):
        winner = self.checkWinner()
        if winner == self.AI:
            return 10**7
        elif winner == self.HUMAN:
            return -10**7
        weights = {
            (4, 2): 10**6,
            (4, 1): 10**5,
            (3, 2): 10**4,
            (3, 1): 10**3,
            (2, 2): 10**2,
            (2, 1): 10,
        }
        def score_player(player):
            total = 0
            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j] != player:
                        continue
                    for dx, dy in self.dirs:
                        prev_i, prev_j = i - dx, j - dy
                        if self.checkValidation(prev_i, prev_j) and self.board[prev_i][prev_j] == player:
                            continue
                        count = 1
                        ni, nj = i + dx, j + dy
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
                        total += weights.get((count, open_ends), 0)
            return total
        return score_player(self.AI) - score_player(self.HUMAN)

    def minimax(self, depth, maximizing):
        if depth == 0 or self.checkWinner() != 0:
            return self.evaluate(), None
        best_move = None
        if maximizing:
            max_eval = -float('inf')
            for move in self.generateMoves():
                self.makeMove(move, self.AI)
                eval_score, _ = self.minimax(depth-1, False)
                self.undoMove(move)
                self.last_move = None
                if eval_score > max_eval:
                    max_eval, best_move = eval_score, move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.generateMoves():
                self.makeMove(move, self.HUMAN)
                eval_score, _ = self.minimax(depth-1, True)
                self.undoMove(move)
                self.last_move = None
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

                self.makeMove(move, self.AI)
                eval_score, _ = self.alphabeta(depth-1, alpha, beta, False)
                self.undoMove(move)
                self.last_move = None
                if eval_score > max_eval:
                    max_eval, best_move = eval_score, move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.generateMoves():

                self.makeMove(move, self.HUMAN)
                eval_score, _ = self.alphabeta(depth-1, alpha, beta, True)
                self.undoMove(move)
                self.last_move = None
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