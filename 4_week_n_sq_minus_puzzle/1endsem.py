#Team - Rajendra singh(111601017), Surendra baskey(111601027), Sachin hansda(111601019)#



#-------------------------------------Imports--------------------------------------------------------#
import numpy as np
import random
from queue import Queue
import copy


#-------------------------------Initialisation and declaration----------------------------------#
N = 4 # matrix of N*N
# r, c = N,N

ri = 2
rj = 1
wi = 0
wj = 2
wm = [[ 1 for x in range(N)] for y in range(N)]
wm[ri][rj] = 2
wm[wi][wj] = 0

rm1 = [[ 1 for x in range(N)] for y in range(N)]
rm2 = [[ 1 for x in range(N)] for y in range(N)]
rm1[0][N-1] = 2
rm2[0][N-1] = 2
rm1[0][N-2] = 0
rm2[1][N-1] = 0

print("Correct matrix1 = ", rm1)
print("Correct matrix2 = ", rm2)
print("wrong matrix = ", wm)


b = random.sample(range(1,1+N**2), N**2)
b = np.array(b)

movelist = []


#--------------------function for finding indices of max element------------------------------------#
def where_is_no(matrix,tempno):
    templist = np.array(matrix)
    x = np.where(templist == tempno)
    p = (x[0][0], x[1][0])
    return p


#------------------------------function of moving any element in matrix---------------------------#
def move_matrix(matrix,move,p):
    if p == -1:
        p = where_is_no(matrix,0)
    i,j = p[0],p[1]
    if move == "right":
        if j != N-1:
           t = matrix[i][j+1]
           matrix[i][j+1] = matrix[i][j]
           matrix[i][j] = t
        else:
            return -1

    elif move == "up":
        if i != 0:
           t = matrix[i-1][j]
           matrix[i-1][j] = matrix[i][j]
           matrix[i][j] = t
        else:
            return -1
    elif move == "left":
        if j != 0:
           t = matrix[i][j-1]
           matrix[i][j-1] = matrix[i][j]
           matrix[i][j] = t
        else:
            return -1
    elif move == "down":
        if i != N-1:
           t = matrix[i+1][j]
           matrix[i+1][j] = matrix[i][j]
           matrix[i][j] = t
        else:
            return -1
    return matrix

#-----------------------------------function for finding reverse move for any move------------------------#
def oppmove(move):
    opp = None
    if move == "right":
        opp = "left"
    elif move == "left":
        opp = "right"
    elif move == "up":
        opp = "down"
    elif move == "down":
        opp = "up"
    return opp

#--------------------function for finding location of empty cell after any move------------#
def nextp(p,move):
    if move == "right":
        tempp = (p[0],p[1]+1)
    elif move == "left":
        tempp = (p[0],p[1]-1)
    elif move == "up":
        tempp = (p[0]-1,p[1])
    elif move == "down":
        tempp = (p[0]+1,p[1])
    return tempp


#----------------------Initialising queue, list---------------------------------------#
q = Queue()
s = [] #list of visited matrix
parent = [] #parent of above


#------------------------Order of movements-------------------------------------------#
moveorder = ["right","up","left","down"]

flagend = 0

#--------------------------------bfs function----------------------------------------#
def bfs(twm,avoidmove,p,trm1, trm2):
    if twm != trm1 and twm != trm2:
        for move in moveorder:
            if move != avoidmove: #aavoid going back to previous state
                child = move_matrix(copy.deepcopy(twm),move,p)
                if child != -1: #checking if move is possible or not
                    if  child not in s:
                        temptuple = (child,oppmove(move),nextp(p,move))
                        q.put(temptuple) #inserting in queue
                        # s.add(child)
                        s.append(child) #inserting in visited list
                        parent.append(twm) #inserting in parent list
        if(q.empty() != 1): #if queue not empty
            temptuple = q.get() #pop element
            child = temptuple[0]
            avoidmove = temptuple[1]
            p = temptuple[2]
            return bfs(child,avoidmove,p,trm1, trm2) #call bfs again
    else:
        print("\n\n\n **************TASK IS DONE*************")
        if twm == trm1:
            flagend = 1
            # rm = trm1
            print("right1")
            return 1
        else:
            flagend = 2
            # rm = trm2
            print("right2")
            return 2
        # return

wrong_matrix = wm

initialp = where_is_no(wrong_matrix,0)
Avoid_move_initial = -3
flagend = bfs(wrong_matrix,Avoid_move_initial,initialp,rm1, rm2) #call bfs


print("Path in reverse order is: ") #printing path
if flagend == 1:
            rm = rm1
elif flagend == 2:
            rm = rm2
print(rm)
temp = s.index(rm)
tempparent = parent[temp]
print(tempparent)
while(tempparent != wrong_matrix):
    temp = s.index(tempparent)
    tempparent = parent[temp]
    print(tempparent)