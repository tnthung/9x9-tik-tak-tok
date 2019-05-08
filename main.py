import random


def checkLineO(array):
    tmp = 0

    a0 = array[0]
    a1 = array[1]
    a2 = array[2]
    a3 = array[3]
    a4 = array[4]
    a5 = array[5]
    a6 = array[6]
    a7 = array[7]
    a8 = array[8]

    if (a0==1 and a1==1 and a2==1):tmp += 1
    if (a3==1 and a4==1 and a5==1):tmp += 1
    if (a6==1 and a7==1 and a8==1):tmp += 1
    if (a0==1 and a3==1 and a6==1):tmp += 1
    if (a1==1 and a4==1 and a7==1):tmp += 1
    if (a2==1 and a5==1 and a8==1):tmp += 1
    if (a0==1 and a4==1 and a8==1):tmp += 1
    if (a2==1 and a4==1 and a6==1):tmp += 1
    return tmp

def checkLineX(array):
    tmp = 0

    a0 = array[0]
    a1 = array[1]
    a2 = array[2]
    a3 = array[3]
    a4 = array[4]
    a5 = array[5]
    a6 = array[6]
    a7 = array[7]
    a8 = array[8]

    if (a0==0 and a1==0 and a2==0):tmp += 1
    if (a3==0 and a4==0 and a5==0):tmp += 1
    if (a6==0 and a7==0 and a8==0):tmp += 1
    if (a0==0 and a3==0 and a6==0):tmp += 1
    if (a1==0 and a4==0 and a7==0):tmp += 1
    if (a2==0 and a5==0 and a8==0):tmp += 1
    if (a0==0 and a4==0 and a8==0):tmp += 1
    if (a2==0 and a4==0 and a6==0):tmp += 1
    return tmp

def pp________(array, p):
    for row in range(3):
        for columnB in range(3):
            for columnS in range(3):
                if   array[columnB][columnS+3*row] == 0: print(' X', end='')
                elif array[columnB][columnS+3*row] == 1: print(' O', end='')
                else:                                    print('  ', end='')

                if   columnS == 2 and columnB != 2: print(' #', end='')
                elif columnS == 2 and columnB == 2: print()

    if p: print('#######################')

def printArray(array):
    pp________(array[0:3], 1)
    pp________(array[3:6], 1)
    pp________(array[6: ], 0)

#printArray(array)

con = 'y'
game = 1

while game:
    # restart / start
    if con == 'y':
        array = [[None for i in range(9)] for i in range(9)]

        turn = random.randint(0, 1)
        grid = random.randint(0, 8)

        con = 'n'

    # count O's lines
    Ocount = 0
    for i in range(9):
        Ocount += checkLineO(array[i])

    # count X's lines
    Xcount = 0
    for i in range(9):
        Xcount += checkLineX(array[i])

    # tell if the grid is full
    none = 0
    for i in range(9):
        for j in range(9):
            if array[i][j] is None:
                none += 1

    if not none:
        if Ocount >  Xcount: con = input('O wins!! Want to continue? (Y/N)').lower()
        if Ocount <  Xcount: con = input('X wins!! Want to continue? (Y/N)').lower()
        if Ocount == Xcount: con = input('Even...  Want to continue? (Y/N)').lower()

        if   con == 'y': con = 'y'
        elif con == 'n': con = 'n'
        else:            con = 'n'

        if con == 'n': quit()

        continue

    # printout grids
    print('\n\n')
    printArray(array)

    # printout game state
    print("\n\n"+f"O: {Ocount}  X: {Xcount}")
    print({0:'X', 1:'O'}.get(turn)+"'s turn.")

    # tell if whole 3x3 grid are occupied
    check = 1
    while check:
        tmp = 0
        for i in range(9):
            if array[grid][i] is None:
                tmp += 1

        if tmp == 0: grid = random.randint(0, 8)
        else:        break

    # make choice
    try:
        insert = int(input('Choose one in '+
              {0:'upper left',
               1:'upper middle',
               2:'upper right',
               3:'middle left',
               4:'center',
               5:'middle right',
               6:'lower left',
               7:'lower middle',
               8:'lower right'}.get(grid)+': '))

    except Exception:
        print("Unknown input!!")
        turn = 0 if turn == 1 else 1
        continue

    # tell input
    if insert not in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        print("Unknown input!!")
        turn = 0 if turn == 1 else 1
        continue

    # tell if the chosen grid is empty
    if array[grid][insert] is None:
        array[grid][insert] = turn

    else:
        print("Already occupied!!")
        turn = 0 if turn == 1 else 1
        continue

    grid = insert
    turn = 0 if turn == 1 else 1




