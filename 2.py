import tkinter as tk
import random
import time

ROWS = 8
COLS = 8
MINES = 10
CELL_SIZE = 40

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("踩地雷")

        self.start_time = None
        self.timer_running = False

        self.info_label = tk.Label(root, text="時間：0 秒", font=("Arial", 12))
        self.info_label.pack()

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.restart_btn = tk.Button(root, text="重新開始", command=self.restart)
        self.restart_btn.pack(pady=5)

        self.restart()

    def restart(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.start_time = None
        self.timer_running = False
        self.info_label.config(text="時間：0 秒")

        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.buttons = {}
        self.revealed = set()
        self.game_over = False

        self.place_mines()
        self.create_buttons()

    def place_mines(self):
        mines = set()
        while len(mines) < MINES:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            mines.add((r, c))

        for r, c in mines:
            self.board[r][c] = '*'
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and self.board[nr][nc] != '*':
                        self.board[nr][nc] += 1

    def create_buttons(self):
        for r in range(ROWS):
            for c in range(COLS):
                btn = tk.Button(
                    self.frame,
                    width=4,
                    height=2,
                    command=lambda r=r, c=c: self.click(r, c)
                )
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    def start_timer(self):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.info_label.config(text=f"時間：{elapsed} 秒")
            self.root.after(1000, self.update_timer)

    def click(self, r, c):
        if self.game_over or (r, c) in self.revealed:
            return

        self.start_timer()

        btn = self.buttons[(r, c)]
        self.revealed.add((r, c))

        if self.board[r][c] == '*':
            btn.config(text="💣", bg="red")
            self.end_game(False)
            return

        btn.config(text=str(self.board[r][c]), relief=tk.SUNKEN, bg="lightgray")

        if self.board[r][c] == 0:
            btn.config(text="")

        if ROWS * COLS - len(self.revealed) == MINES:
            self.end_game(True)

    def end_game(self, win):
        self.game_over = True
        self.timer_running = False
        elapsed = int(time.time() - self.start_time)

        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] == '*':
                    self.buttons[(r, c)].config(text="💣")

        if win:
            self.info_label.config(text=f"🎉 勝利！耗時：{elapsed} 秒")
        else:
            self.info_label.config(text="💥 踩到地雷！遊戲結束")

if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()
