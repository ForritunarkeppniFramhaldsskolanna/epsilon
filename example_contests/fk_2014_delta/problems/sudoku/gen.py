import random

def duplicates(x):
    x = [ i for i in x if i is not None ]
    return len(x) > len(set(x))

def check(arr):

    for i in range(9):

        if duplicates([ arr[i][j] for j in range(9) ]): return False
        if duplicates([ arr[j][i] for j in range(9) ]): return False

    for i in range(3):
        for j in range(3):

            if duplicates([ arr[3*i+x][3*j+y] for x in range(3) for y in range(3) ]):
                return False

    return True

def display(board):
    res = [ [ ' ' for j in range(9+2) ] for i in range(9+2) ]

    for i in range(9):
        for j in range(9):
            res[i+i//3][j+j//3] = str(1 + board[i][j]) if board[i][j] is not None else 'X'

    for i in range(9+2):
        for j in range(9+2):
            a = i % 4 == 3
            b = j % 4 == 3
            if a and b:
                res[i][j] = '+'
            elif a:
                res[i][j] = '-'
            elif b:
                res[i][j] = '|'


    for row in res:
        print(''.join(row))

def displaytex(board):
    for i in range(9):
        for j in range(9):
            print('%d/%d/%d,' % (i,j,board[8 - j][i]+1))


board = [ [ None for j in range(9) ] for i in range(9) ]
def gen(row):

    if row == 9:
        display(board)
        # print('')
        # displaytex(board)
        return True

    tries = 10

    def fill(col):
        if col == 9:
            return True

        poss = list(range(9))
        random.shuffle(poss)

        for p in poss:
            board[row][col] = p
            if check(board) and fill(col+1):
                return True
            board[row][col] = None

        return False

    for t in range(tries):
        if fill(0) and gen(row+1):
            return True

    return False

gen(0)

