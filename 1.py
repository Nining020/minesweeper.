import random

ROWS = 8
COLS = 8
MINES = 10

def create_board():
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    mines = set()

    while len(mines) < MINES:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)
        mines.add((r, c))

    for r, c in mines:
        board[r][c] = '*'
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] != '*':
                    board[nr][nc] += 1

    return board, mines

def print_board(show_board):
    print("  " + " ".join(str(i) for i in range(COLS)))
    for i, row in enumerate(show_board):
        print(i, " ".join(row))

def play():
    board, mines = create_board()
    show_board = [['■' for _ in range(COLS)] for _ in range(ROWS)]
    revealed = set()

    while True:
        print_board(show_board)
        try:
            r, c = map(int, input("輸入 row col：").split())
        except ValueError:
            print("請輸入正確格式，例如：1 2")
            continue

        if not (0 <= r < ROWS and 0 <= c < COLS):
            print("超出範圍！")
            continue

        if (r, c) in mines:
            print("💥 你踩到地雷了，遊戲結束！")
            board[r][c] = '*'
            print_board(board)
            break

        show_board[r][c] = str(board[r][c])
        revealed.add((r, c))

        if ROWS * COLS - len(revealed) == MINES:
            print("🎉 恭喜你，成功排雷！")
            print_board(board)
            break

if __name__ == "__main__":
    play()
