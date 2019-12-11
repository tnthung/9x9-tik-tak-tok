from tkinter     import *
from functools   import partial
import random
import time
import threading


class game:
    def __init__(self):
        self.record = []

        self.score  = [0, 0]
        self.array  = [[None for i in range(9)] for i in range(9)]
        self.grid   = random.randint(0, 8)
        self.turn   = random.randint(0, 1)

        self.root = Tk()

        self.sW()
        self.mW()
        self.pW()

        self.root.mainloop()

    def sW(self):
        self.root.title('9x9 Tik Tak Tok')

        self.root.geometry('405x318')
        self.root.resizable(0, 0)

    def mW(self):
        self.framGrid  = Frame(self.root) #
        self.framScore = Frame(self.root) #

        self.framGridSub = [Frame(self.framGrid, padx=5, pady=5) for i in range(9)] #

        self.menu     = Menu( self.root)
        self.menu.add_command(label='New Game', command=lambda :self.start())
        self.menu.add_command(label='Give Up' , command=lambda :self.giveup())
        self.menu.add_command(label='History' , command=lambda :self.history())
        self.menu.add_command(label='Help'    , command=lambda :self.help())

        self.button = {} #
        for i in range(9):
            for j in range(9):
                self.button[f'{i}-{j}'] = Button(self.framGridSub[i],
                                                       width   = 3,
                                                       height  = 1,
                                                       pady    = 4,
                                                       state   = DISABLED,
                                                       #text    = f'{i}-{j}',
                                                       command = partial(self.change, i, j)
                                                 )

        self.labelPlayer = Label(self.framScore, font=('arial', 24), text='O   X') #
        self.labelScore  = Label(self.framScore, font=('arial', 24), text='0 : 0') #

        self.framTime    = LabelFrame(self.root, text='Time') #
        self.lableTime   = Label(self.framTime, font=('arial', 24), text='00:00')  #

    def pW(self):
        self.framGrid .grid(row=0, column=0, rowspan=2)
        self.framTime .grid(row=0, column=1)
        self.framScore.grid(row=1, column=1)

        for i in range(3):
            for j in range(3):
                self.framGridSub[i*3+j].grid(row=i, column=j)

        for i in range(9):
            for j in range(3):
                for k in range(3):
                    self.button[f'{i}-{j*3+k}'].grid(row=j, column=k)

        self.lableTime.grid(row=0, column=0)

        self.labelPlayer.grid(row=0, column=0)
        self.labelScore .grid(row=1, column=0)

        self.root.config(menu=self.menu)

    def start(self):
        self.timeS()

        self.score    = [0, 0]
        self.array    = [[None for i in range(9)] for i in range(9)]
        self.grid     = random.randint(0, 8)
        self.turn     = random.randint(0, 1)
        self.timeC    = 0

        threading.Thread(target=self.count).start()

        for i in range(9):
            for j in range(9):
                self.button[f'{i}-{j}'].configure(state=DISABLED, text='')

            self.framGridSub[i].configure(bg='#f0f0f0')

        for i in range(9):
            self.button[f'{self.grid}-{i}'].configure(state=NORMAL)
            self.framGridSub[self.grid].configure(bg='#808080')

        self.labelPlayer.configure(text={0:'O  >X', 1:'O<  X'}.get(self.turn))

    def giveup(self):
        self.end()

        t = {0:'X', 1:'O'}.get(self.turn)+' gives up!!'

        self.record.append(t)
        self.msgBox(t)

        print('give up')

    def history(self):
        self.historyList(self.record)
        print(self.record)

    def change(self, x, y):
        self.array[x][y] = self.turn
        self.button[f'{x}-{y}'].configure(text={0:'X', 1:'O'}.get(self.turn))

        lineX, lineY = self.calLine()
        self.labelScore.configure(text=f'{lineX}:{lineY}')

        tmpWhile = self.check(lineX, lineY)

        self.turn = 0 if self.turn == 1 else 1
        self.grid = y

        self.labelPlayer.configure(text={0:'O  >X', 1:'O<  X'}.get(self.turn))

        tmp = 9
        while tmp and tmpWhile is None:
            tmp = 0
            for i in range(9):
                if self.array[self.grid][i] is None:
                    tmp += 1

            if tmp == 0:
                self.grid = random.randint(0, 8)
                tmp = 1

            else:
                break

        for i in range(9):
            for j in range(9):
                self.button[f'{i}-{j}'].configure(state=DISABLED)

            self.framGridSub[i].configure(bg='#f0f0f0')

        for i in range(9):
            if self.array[self.grid][i] is None:
                self.button[f'{self.grid}-{i}'].configure(state=NORMAL)

            self.framGridSub[self.grid].configure(bg='#808080')

        print(f'{x}, {y}')

    def check(self, x, y):
        tmp = 0
        for i in range(9):
            for j in range(9):
                if self.array[i][j] is None:
                    tmp += 1

        if tmp == 0:
            t = ''
            
            if x > y:
                t = 'O wins!!'

            elif x == y:
                t = 'Even!!'

            elif x < y:
                t = 'X wins!!'

            t += f'   Score {x}:{y}'
            t += f'   Time {self.timeC//60}:{self.timeC%60}'
            self.record.append(t)
            self.end()
            self.msgBox(t, '250x78', 35)
            return 1

    def end(self):
        self.timeP()

        for i in range(9):
            for j in range(9):
                self.button[f'{i}-{j}'].configure(state=DISABLED)

            self.framGridSub[i].configure(bg='#f0f0f0')

        self.labelPlayer.configure(text='O   X')

    def calLine(self):
        tmpO = 0
        tmpX = 0

        for i in range(9):
            tmp = self.array[i]

            a0 = tmp[0]
            a1 = tmp[1]
            a2 = tmp[2]
            a3 = tmp[3]
            a4 = tmp[4]
            a5 = tmp[5]
            a6 = tmp[6]
            a7 = tmp[7]
            a8 = tmp[8]

            if a0==1 and a1==1 and a2==1: tmpO += 1
            if a3==1 and a4==1 and a5==1: tmpO += 1
            if a6==1 and a7==1 and a8==1: tmpO += 1
            if a0==1 and a3==1 and a6==1: tmpO += 1
            if a1==1 and a4==1 and a7==1: tmpO += 1
            if a2==1 and a5==1 and a8==1: tmpO += 1
            if a0==1 and a4==1 and a8==1: tmpO += 1
            if a2==1 and a4==1 and a6==1: tmpO += 1

            if a0==0 and a1==0 and a2==0: tmpX += 1
            if a3==0 and a4==0 and a5==0: tmpX += 1
            if a6==0 and a7==0 and a8==0: tmpX += 1
            if a0==0 and a3==0 and a6==0: tmpX += 1
            if a1==0 and a4==0 and a7==0: tmpX += 1
            if a2==0 and a5==0 and a8==0: tmpX += 1
            if a0==0 and a4==0 and a8==0: tmpX += 1
            if a2==0 and a4==0 and a6==0: tmpX += 1

        tmpO = str(tmpO)
        tmpX = str(tmpX)

        if len(tmpO) == 1: tmpO += ' '
        if len(tmpX) == 1: tmpX =  ' ' + tmpX

        return tmpO, tmpX

    def timeS(self):
        self.lableTime.configure(text='00:00')
        self.timeFlag = True

    def timeP(self):
        self.timeFlag = False

    def count(self):
        while self.timeFlag:
            time.sleep(1)
            self.timeC += 1

            minuet = str(self.timeC//60)
            second = str(self.timeC% 60)

            if len(minuet) == 1: minuet = '0' + minuet
            if len(second) == 1: second = '0' + second

            t = minuet+':'+second

            self.lableTime.configure(text=t)

    @staticmethod
    def msgBox(text, size='150x78', width=20):
        root = Tk()

        root.geometry(size)
        root.resizable(0, 0)
        root.title('')

        Label(root, text=text, width=width, height=2).grid(row=0, column=0)
        Button(root, text='OK', width=10, height=2,
               command=lambda :root.destroy()).grid(row=1, column=0)

        root.mainloop()

    @staticmethod
    def historyList(history):
        root = Tk()

        root.title('History')

        list_ = Listbox(root, width=50)

        for i in history:
            list_.insert(END, i)

        list_.pack()

        root.mainloop()

    @staticmethod
    def help():
        root = Tk()

        root.title("Help")
        
        S = Scrollbar(root)
        T = Text(root, height=20, width=52)
        S.pack(side=RIGHT, fill=Y)
        T.pack(side=LEFT, fill=Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        
        quote = \
'''
New Game:
    press "New Game" button on the toolbar to start
    the new game.

Give up:
    press "Give up" the game will stop and record
    in history.

History:
    press "History" the all history of who wins,
    who gave up, time comsuming.

Help:
    press "Help" to open this page.

Rule:
    Before knowing the rule there's some words
    you'll need to know.

    1. CHUNK: the group of 9 botton which separated
    by spacing.
    
    2. ZONE: the gray square which surrounded
    the chunk.

    3. BLOCK: the button in the chunk.

    Every time when game started, it'll randomly
    choose a player and the chunk to start.

    To play the first player need to choose one
    block in zone and the one player choose will
    becoming a next position of zone for next player.
    
    For example:
        Assuming zone started at upper left.
        Player 1 choose the center block, then zone
        goes to center chunk. Now is Player 2's
        turn, he/she need to choose the block in
        new zone. If the chunk which zone suppose
        to go is full, the zone will automatically
        choose a chunk has empty block. Repeat this
        until all chunk are filled. Then the player
        who has more line in chunk becomes the
        winner.
'''
        
        T.insert(END, quote)
        root.mainloop()


game()

