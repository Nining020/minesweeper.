import tkinter as tk
import random
import time

KUROMI_MINE = "😈🎀"

DIFFICULTY = {
    "簡單": (8, 8, 10),
    "普通": (12, 12, 20),
    "困難": (16, 16, 40)
}

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("酷洛米踩地雷 💜")
        self.show_menu()

    # ====== 選單畫面 ======
    def show_menu(self):
        self.clear()
        tk.Label(
            self.root,
            text="😈 酷洛米踩地雷 🎀",
            font=("Arial", 20, "bold"),
            fg="#8B008B"
        ).pack(pady=20)

        tk.Label(self.root, text="請選擇難度", font=("Arial", 14)).pack(pady=10)

        for name in DIFFICULTY:
            tk.Button(
                self.root,
                text=name,
                font=("Arial", 12),
                width=10,
                command=lambda n=name: self.start_game(n)
            ).pack(pady=5)

    # ====== 遊戲初始化 ======
    def start_game(self, difficulty):
        self.clear()

        self.rows, self.cols, self.mines_count = DIFFICULTY[difficulty]
        self.start_time = None
        self.timer_running = False
        self.game_over = False
        self.revealed = set()

        self.info = tk.Label(self.root, text="時間：0 秒", font=("Arial", 12))
        self.info.pack()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        tk.Button(
            self.root,
            text="重新開始",
            command=self.show_menu
        ).pack(pady=5)

        self.create_board()
        self.create_buttons()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ====== 地圖生成 ======
    def create_board(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        mines = set()

        while len(mines) < self.mines_count:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            mines.add((r, c))

        for r, c in mines:
            self.board[r][c] = '*'
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] != '*':
                        self.board[nr][nc] += 1

    def create_buttons(self):
        self.buttons = {}
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.frame,
                    width=3,
                    height=1,
                    bg="#E6E6FA",
                    command=lambda r=r, c=c: self.click(r, c)
                )
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    # ====== 計時 ======
    def start_timer(self):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.info.config(text=f"時間：{elapsed} 秒")
            self.root.after(1000, self.update_timer)

    # ====== 點擊處理 ======
    def click(self, r, c):
        if self.game_over or (r, c) in self.revealed:
            return

        self.start_timer()
        self.revealed.add((r, c))
        btn = self.buttons[(r, c)]

        if self.board[r][c] == '*':
            btn.config(text=KUROMI_MINE, bg="#FFB6C1")
            self.end_game(False)
            return

        btn.config(
            text=str(self.board[r][c]) if self.board[r][c] > 0 else "",
            relief=tk.SUNKEN,
            bg="#D8BFD8"
        )

        if self.rows * self.cols - len(self.revealed) == self.mines_count:
            self.end_game(True)

    # ====== 結束 ======
    def end_game(self, win):
        self.game_over = True
        self.timer_running = False
        elapsed = int(time.time() - self.start_time)

        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == '*':
                    self.buttons[(r, c)].config(text=KUROMI_MINE)

        if win:
            self.info.config(text=f"🎉 酷洛米勝利！耗時 {elapsed} 秒")
        else:
            self.info.config(text="💥 被酷洛米炸到了！")

if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()
