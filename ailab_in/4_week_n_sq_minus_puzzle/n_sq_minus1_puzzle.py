#Team - Rajendra singh(111601017), Surendra baskey(111601027), Sachin hansda(111601019)#



#-------------------------------------Imports--------------------------------------------------------#
import numpy as np
import random
from queue import Queue
import copy


#-------------------------------Initialisation and declaration----------------------------------#
N = 4 # matrix of N*N
r, c = N,N
rm = [[y*N+x for x in range(1,c+1)] for y in range(r)]

print("Correct matrix = ", rm)

b = random.sample(range(1,1+N**2), N**2)
b = np.array(b)

movelist = []
wm2 = [[ b[y*N+x] for x in range(c)] for y in range(r)]


#--------------------function for finding indices of max element------------------------------------#
def where_is_no(matrix,tempno):
    templist = np.array(matrix)
    x = np.where(templist == tempno)
    p = (x[0][0], x[1][0])
    return p


#------------------------------function of moving any element in matrix---------------------------#
def move_matrix(matrix,move,p):
    if p == -1:
        p = where_is_no(matrix,N*N)
    i,j = p[0],p[1]
    if move == "right":
        if j != N-1:
        #    print("i,j = ", i,j)
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



#-------------------------Creating random wrong matrix starting from right matrix---------------------#
wm = copy.deepcopy(rm)
wmmovelist = []
previous_move = -2
no_of_step_away = 5 #no. of steps away from right matrix

while len(wmmovelist) != no_of_step_away:
    templist = ["right","up","left","down"]
    r = random.choice(templist)
    if r != oppmove(previous_move):
        tempresult = move_matrix(wm,r,-1)
        if tempresult != -1:
            wm = tempresult
            # print("-->", wm)
            wmmovelist.append(r)
            previous_move = r

# print("\nwmmovelist = ",wmmovelist)
# print("\nwm = ",wm)

# templ = len(wmmovelist)
# print("predicted correct movelist = ", end = "") #predicting correct moves
# for i in range(0,templ):
#     j = (templ-1)-i
#     print(oppmove(wmmovelist[j]), end =",")


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
# s = set()
# s.add(1)


#------------------------Order of movements-------------------------------------------#
moveorder = ["right","up","left","down"]



#--------------------------------bfs function----------------------------------------#
def bfs(twm,avoidmove,p,trm):
    if twm != trm:
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
            bfs(child,avoidmove,p,trm) #call bfs again
    else:
        print("\n\n\n **************TASK IS DONE*************")
        return


#--------------------function for finding parity------------------------------------------#
def parity(temp_wm):
    templist = []
    for bigele in temp_wm:
        for ele in bigele:
            templist.append(ele)
    sum = 0
    for i in range(0,len(templist)):
        ele1 = templist[i]
        for j in range(i+1,len(templist)):
            ele2 = templist[j]
            if ele2 < ele1:
                sum+=1
    pair = where_is_no(temp_wm,N*N)
    sum = sum + 2*(N-1)-pair[0]-pair[1]
    return sum%2

wrong_matrix = wm
print("Wrong matrix(randomly genrated) : ", wrong_matrix)
parity = parity(wrong_matrix)
if parity == 0:     #if parity 0
    print("solvable, since parity is 0")

    
    initialp = where_is_no(wrong_matrix,N*N)
    Avoid_move_initial = -3
    bfs(wrong_matrix,Avoid_move_initial,initialp,rm) #call bfs
    
    
    print("Path in reverse order is: ") #printing path
    print(rm)
    temp = s.index(rm)
    tempparent = parent[temp]
    print(tempparent)
    while(tempparent != wrong_matrix):
        temp = s.index(tempparent)
        tempparent = parent[temp]
        print(tempparent)
else:                   #if parity 1
    print("\n ==> Unsolvable wrong matrix since parity is 1 <==")

    




