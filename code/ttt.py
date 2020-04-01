import random

alpha = 0.1
greedy = 0.5
epoch = 500
iter_per_epoch = 1000

V = [ 0.5 for _ in range(3**9) ]

t2d = lambda x:int(str(x)[::-1],3)
d2t = lambda x:[ x//3**i%3 for i in range(9) ]
win = lambda l,who:(l[0]==who and l[1]==who and l[2]==who) or (l[3]==who and l[4]==who and l[5]==who) or (l[6]==who and l[7]==who and l[8]==who) or (l[0]==who and l[3]==who and l[6]==who) or (l[1]==who and l[4]==who and l[7]==who) or (l[2]==who and l[5]==who and l[8]==who) or (l[0]==who and l[4]==who and l[8]==who) or (l[2]==who and l[4]==who and l[6]==who)

# init
for i in range(3**9):
    l = d2t(i)
    a = win(l,1)
    b = win(l,2)
    if a and b:continue # not reached
    elif a:V[i] = 1.0
    elif b:V[i] = 0.0

# returns a state randomly
def random_move(state,who):
    if who not in (1,2):raise KeyError("'who' can only be 1(for X) or 2(for O)");
    l = d2t(state)
    l[ random.choice( [i for i in range(len(l)) if l[i] == 0 ]) ] = who
    return t2d(''.join(map(str,l)))

# returns a state with best value
def best_move(state):
    l = d2t(state)
    bv = 0  # best value yet
    bi = -1 # state index for best value
    for i in ( i for i in range(len(l)) if l[i] == 0): # each possible move
        s = l.copy();s[i] = 1;
        ss = t2d(''.join(map(str,s))) # new move state
        if bv < V[ss]: bv = V[ss]; bi = ss;
    return bi

def picker():
    while 1:yield 1;yield 2;

# train
for i in range(epoch):
    win_num = lose_num = 0
    for _ in range(iter_per_epoch):
        p = picker()
        s = t2d('000000000') # start with empty board
        while 1:
            if next(p) == 1:
                if random.random() < greedy:
                    ns = best_move(s)
                else:
                    ns = random_move(s,1)
            else:
                ns = random_move(s,2)
            # update
            V[s] += alpha * (V[ns]-V[s])
            s = ns
            if win(d2t(s),1):
                win_num += 1;break;
            elif win(d2t(s),2):
                lose_num += 1;break;
            elif 0 not in d2t(s):
                break; # it's a tie
    print('Epoch %d, win %d lose %d tie %d'%(i,win_num,lose_num,iter_per_epoch-win_num-lose_num))

# save train data
with open('XO.txt',"w") as f:
    print(V,file=f)

def print_board(s):
    l = d2t(s)
    d = ['_','X','O']
    for i in range(3):
        for j in range(3):
            print(d[l[i*3+j]],end='')
        print()

# play with
while input('Play?(y/n)') == 'y':
    p = picker()
    s = t2d('000000000')
    while 1:
        print_board(s)
        if next(p) == 1:
            s = best_move(s) # stop training
        else:
            l = d2t(s)
            while 1:
                move = int(input('Your move:'))
                if move not in (i for i in range(len(l)) if l[i] == 0):
                    print('Invalid move. try again.')
                    continue
                else:
                    break;
            l[move]=2
            s = t2d(''.join(map(str,l)))
            print('s=',s)
        if win(d2t(s),1):
            print_board(s)
            print('Computer wins!');break;
        elif win(d2t(s),2):
            print_board(s)
            print('You win!');break;
        elif 0 not in d2t(s):
            print("It's a tie");break;

