# 匯入 tkinter，負責製作圖形化視窗介面（GUI）
import tkinter as tk

# 匯入 random，用來隨機產生地雷位置
import random

# partial 用來在按鈕事件中「預先帶入參數」
from functools import partial

# 遊戲設定：棋盤大小與地雷數量
ROWS = 9
COLS = 9
MINES = 10


# 定義踩地雷遊戲類別（物件導向設計）
class Minesweeper:
    def __init__(self, root):
        # 設定主視窗
        self.root = root
        self.root.title("踩地雷 Minesweeper")

        # 建立一個 Frame 來放置所有按鈕
        self.frame = tk.Frame(root)
        self.frame.pack()

        # 建立 9x9 的按鈕矩陣，用來顯示棋盤
        self.buttons = [[None for _ in range(COLS)] for _ in range(ROWS)]

        # 儲存實際棋盤資料
        # -1 代表地雷，其餘數字代表周圍地雷數
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        # 記錄每個格子是否被插旗
        self.flags = [[False for _ in range(COLS)] for _ in range(ROWS)]

        # 記錄每個格子是否已翻開
        self.revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]

        # 遊戲是否進行中（用來避免遊戲結束後還能操作）
        self.running = True

        # 建立地雷與數字棋盤
        self.create_mines()

        # 建立畫面上的按鈕
        self.create_buttons()


    # 隨機放置地雷，並計算周圍地雷數
    def create_mines(self):
        mines = set()

        # 隨機產生不重複的地雷位置
        while len(mines) < MINES:
            r = random.randint(0, ROWS-1)
            c = random.randint(0, COLS-1)
            mines.add((r, c))

        # 在棋盤中標記地雷，並更新周圍數字
        for r, c in mines:
            self.board[r][c] = -1
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and self.board[nr][nc] != -1:
                        self.board[nr][nc] += 1


    # 建立每一個棋盤按鈕
    def create_buttons(self):
        for r in range(ROWS):
            for c in range(COLS):
                # 建立按鈕，左鍵點擊會翻開格子
                btn = tk.Button(
                    self.frame,
                    width=3,
                    height=1,
                    command=partial(self.reveal_cell, r, c)
                )

                # 綁定滑鼠右鍵，用來插旗
                btn.bind("<Button-3>", partial(self.toggle_flag, r, c))

                # 使用 grid 排版方式放到指定位置
                btn.grid(row=r, column=c)

                # 儲存按鈕物件
                self.buttons[r][c] = btn


    # 右鍵插旗或取消插旗
    def toggle_flag(self, r, c, event):
        # 若遊戲已結束或格子已翻開，不能插旗
        if not self.running or self.revealed[r][c]:
            return

        # 插旗
        if not self.flags[r][c]:
            self.buttons[r][c].config(text="🚩")
            self.flags[r][c] = True
        # 取消插旗
        else:
            self.buttons[r][c].config(text="")
            self.flags[r][c] = False


    # 左鍵翻開格子
    def reveal_cell(self, r, c):
        # 若遊戲結束、已插旗或已翻開，則不處理
        if not self.running or self.flags[r][c] or self.revealed[r][c]:
            return

        # 如果踩到地雷
        if self.board[r][c] == -1:
            self.buttons[r][c].config(text="💣", bg="red")
            self.game_over()
            return

        # 翻開格子（遞迴展開）
        self._flood_fill(r, c)

        # 每次翻格後檢查是否勝利
        self.check_win()


    # 遞迴展開空白區域（類似原本踩地雷的展開效果）
    def _flood_fill(self, r, c):
        # 超出範圍、已翻開或已插旗就停止
        if not (0 <= r < ROWS and 0 <= c < COLS):
            return
        if self.revealed[r][c] or self.flags[r][c]:
            return

        # 標記為已翻開
        self.revealed[r][c] = True

        # 取得該格子的數字
        val = self.board[r][c]

        # 更新按鈕顯示
        self.buttons[r][c].config(
            text=str(val) if val > 0 else "",
            relief=tk.SUNKEN,
            bg="lightgrey"
        )

        # 若為 0，則自動展開周圍 8 個格子
        if val == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr != 0 or dc != 0:
                        self._flood_fill(r + dr, c + dc)


    # 遊戲失敗處理
    def game_over(self):
        self.running = False

        # 顯示所有地雷
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] == -1:
                    self.buttons[r][c].config(text="💣", bg="red")


    # 檢查是否勝利
    def check_win(self):
        # 若還有非地雷的格子沒翻開，則尚未勝利
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] != -1 and not self.revealed[r][c]:
                    return

        # 若全部安全格都翻開，則勝利
        self.running = False

        # 將所有格子變成綠色
        for r in range(ROWS):
            for c in range(COLS):
                self.buttons[r][c].config(bg="green")

        # 顯示勝利訊息視窗
        tk.messagebox.showinfo("勝利", "🎉 恭喜你，成功排除所有地雷！")


# 程式進入點
if __name__ == "__main__":
    # 建立主視窗
    root = tk.Tk()

    # 匯入訊息視窗模組
    import tkinter.messagebox

    # 建立遊戲物件
    game = Minesweeper(root)

    # 啟動視窗事件循環
    root.mainloop()
