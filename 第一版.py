import random

ROWS = 9
COLS = 9
MINES = 10

def create_board():
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    mines = set()

    while len(mines) < MINES:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)
        mines.add((r, c))

    for r, c in mines:
        board[r][c] = -1
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] != -1:
                    board[nr][nc] += 1

    return board, mines

def print_board(visible):
    print("  " + " ".join(str(i) for i in range(COLS)))
    for i, row in enumerate(visible):
        print(i, " ".join(row))

def reveal(board, visible, r, c):
    if visible[r][c] != "■":
        return
    if board[r][c] == -1:
        visible[r][c] = "*"
        return
    visible[r][c] = str(board[r][c])
    if board[r][c] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    reveal(board, visible, nr, nc)

def check_win(visible, mines):
    hidden = sum(row.count("■") for row in visible)
    return hidden == len(mines)

def main():
    board, mines = create_board()
    visible = [["■" for _ in range(COLS)] for _ in range(ROWS)]

    while True:
        print_board(visible)
        try:
            r, c = map(int, input("輸入座標 (row col): ").split())
        except ValueError:
            print("請輸入正確格式，例如：3 4")
            continue

        if not (0 <= r < ROWS and 0 <= c < COLS):
            print("超出範圍！")
            continue

        if board[r][c] == -1:
            print("💥 踩到地雷！遊戲結束")
            for mr, mc in mines:
                visible[mr][mc] = "*"
            print_board(visible)
            break

        reveal(board, visible, r, c)

        if check_win(visible, mines):
            print("🎉 恭喜你，成功排除所有地雷！")
            print_board(visible)
            break

if __name__ == "__main__":
    main()
