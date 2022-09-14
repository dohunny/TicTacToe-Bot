import time

def win_check(board, choice):

    return ( 
       ( board[0] == choice and board[1] == choice and board[2] == choice )
    or ( board[3] == choice and board[4] == choice and board[5] == choice )
    or ( board[6] == choice and board[7] == choice and board[8] == choice )
    
    or ( board[0] == choice and board[3] == choice and board[6] == choice )
    or ( board[1] == choice and board[4] == choice and board[7] == choice )
    or ( board[2] == choice and board[5] == choice and board[8] == choice )
    
    or ( board[0] == choice and board[4] == choice and board[8] == choice )
    or ( board[2] == choice and board[4] == choice and board[6] == choice )  )

def CompAI(board):
    position = 0
    possibilities = [x for x, letter in enumerate(board) if letter == '   ']
    print(possibilities)
    
    for let in [' O ', ' X ']:
        for i in possibilities:
            boardCopy = board[:]
            boardCopy[i] = let
            if(win_check(boardCopy, let)):
                position = i
                return position

    
    if 4 in possibilities:
        position = 4
        return position
    
    openEdges = [x for x in possibilities if x in [1, 3, 5, 7]]
    
    if len(openEdges) > 0:
        position = selectRandom(openEdges)
        return position
    
    openCorners = [x for x in possibilities if x in [0, 2, 6, 8]]

    if len(openCorners) > 0:
        position = selectRandom(openCorners)
        return position


def selectRandom(board):
    import random
    ln = len(board)
    r = random.randrange(0,ln)
    return board[r]

def place_marker(board, avail, choice, position):
    
    board[position] = choice
    avail[position] = ' '
    

from pwn import * 
context.log_level = "debug"

p = remote('211.229.232.100' ,30010)
# p = process('./prob')

row = [[],[],[],[],[]]
p.recvuntil(": X\n")
while True:
    try:
        tmp = p.recvrepeat(0.2).decode()
        if "yisf" in tmp.lower():
            print(tmp)
            break
        elif "you: x" in tmp.lower():
            tmp = '\n'.join(tmp.split('\n')[2:])
        tmp = tmp.split('\n')
        # print(tmp)

        for i in range(5):
            row[i] = tmp[i].split('|')
        
        theBoard = row[0] + row[2] + row[4]
        print(theBoard)
        available = [str(num) for num in range(0,10)] # a List Comprehension
        position = CompAI(theBoard)
        print(position)
        place_marker(theBoard, available, ' X ', position)
        p.sendline(str(position))
        p.recvline()
    except:
        continue
