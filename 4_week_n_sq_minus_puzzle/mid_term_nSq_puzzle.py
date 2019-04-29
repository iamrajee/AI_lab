'''
#-------------------------------------Author-----------------------------------------------#
Rajendra singh(111601017)

#-------------------------------------Logic------------------------------------------------#
1) Here i used bfs to solve the problem
2) At any configration maximum of 8 move are possible
3) These moves are ["right","up","left","down"] for both empty blocks(i.e 4+4=8)
4) For Initial configration, i'm taking all above possible move and puting them in queue and also storing these configration in a list(which tells about visited states)
5)If queue is not empty then i pop one element and call the bfs again on this poped element
6)If this poped element is equal to any of correct state(two correct state possible rm1, rm2) that means ours task is done.
7) we also store the parent in an another list for any move so that we can print the path later in reverse order
'''





#-------------------------------------Imports--------------------------------------------------------#
import numpy as np
import random
from queue import Queue
import copy


#-------------------------------Initialisation and declaration----------------------------------#
N = 4 # matrix of N*N
r, c = N,N
rm2 = [[y*N+x for x in range(1,c+1)] for y in range(r)]

rm1 = copy.deepcopy(rm2)
lastele = rm1[N-1][N-1]
rm1[N-1][N-1] = rm1[N-1][N-2]
rm1[N-1][N-2] = lastele

print("Correct matrix2 = ", rm2)
print("Correct matrix1 = ", rm1)




b = random.sample(range(1,1+N**2), N**2)
b = np.array(b)
wm2 = [[ b[y*N+x] for x in range(c)] for y in range(r)]

max1 = N*N-1
max2 = N*N



#--------------------function for finding indices of max element------------------------------------#
def where_is_no(matrix,tempno):
    templist = np.array(matrix)
    x = np.where(templist == tempno)
    p = (x[0][0], x[1][0])
    return p


#------------------------------function of moving any element in matrix---------------------------#
def move_matrix(matrix,move,p,tempmax):
    if p == -1:
        p = where_is_no(matrix,tempmax)
    i,j = p[0],p[1]
    if move == "right":
        if j != N-1:
            t = matrix[i][j+1]
            if t != max1 and t != max2:
                matrix[i][j+1] = matrix[i][j]
                matrix[i][j] = t
            else:
                return -1

        else:
            return -1
    elif move == "up":
        if i != 0:
            t = matrix[i-1][j]
            if t != max1 and t != max2:
                matrix[i-1][j] = matrix[i][j]
                matrix[i][j] = t
            else:
                return -1
        else:
            return -1
    elif move == "left":
        if j != 0:
            t = matrix[i][j-1]
            if t != max1 and t != max2:
                matrix[i][j-1] = matrix[i][j]
                matrix[i][j] = t
            else:
                return -1
        else:
            return -1
    elif move == "down":
        if i != N-1:
            t = matrix[i+1][j]
            if t != max1 and t != max2:
                matrix[i+1][j] = matrix[i][j]
                matrix[i][j] = t
            else:
                return -1  
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
wm = copy.deepcopy(rm2)
wmmovelist = []
previous_move = -2
previous_flag =  3
no_of_step_away = 5 #no. of steps away from right matrix

while len(wmmovelist) != no_of_step_away:
    templist = ["right","up","left","down"]
    flaglist = [0,1]
    r = random.choice(templist)
    flag = random.choice(flaglist)

    if (r == oppmove(previous_move) and flag == previous_flag) != 1:
        
        if flag == 1:
            tempmax = max1
        else:
            tempmax = max2

        tempresult = move_matrix(wm,r,-1, tempmax)

        if tempresult != -1:
            wm = tempresult
            # print("-->", wm)
            wmmovelist.append(r)
            previous_move = r

# print("\nwmmovelist = ",wmmovelist)
print("\nwm = ",wm)

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
tran = []
tranflag = []


#------------------------Order of movements-------------------------------------------#
moveorder = ["right","up","left","down"]
flagorder = [1,2]

#--------------------------------bfs function----------------------------------------#
def bfs(twm,flag,avoidmove,p1,p2,trm1, trm2):
    if twm != trm1 and twm != trm2 :
        for f in flagorder:
            if f == 1:
                p = p1
            elif f ==2:
                p = p2
            for move in moveorder:
                if (move == avoidmove and f == flag) != 1: #avoid going back to previous state
                    if f == 1:
                        child = move_matrix(copy.deepcopy(twm),move,p,max1)
                    elif f ==2:
                        child = move_matrix(copy.deepcopy(twm),move,p,max2)
                    
                    if child != -1: #checking if move is possible or not
                        if  child not in s:
                            if f ==1:
                                temptuple = (child,f,oppmove(move),nextp(p,move),p2)
                            else:
                                temptuple = (child,f,oppmove(move),p1, nextp(p,move))
                            q.put(temptuple) #inserting in queue
                            # s.add(child)
                            s.append(child) #inserting in visited list
                            parent.append(twm) #inserting in parent list
                            tran.append(move) #storing move
                            tranflag.append(f) #storing move


        print("queue length :", q.qsize() )
        if(q.empty() != 1): #if queue not empty
            temptuple = q.get() #pop element
            child = temptuple[0]
            flag = temptuple[1]
            avoidmove = temptuple[2]
            p1 = temptuple[3]
            p2 = temptuple[4]
            return bfs(child,flag,avoidmove,p1,p2,trm1,trm2) #call bfs again
    else:
        print("\n\n\n **************TASK IS DONE*************")
        return twm



wm3 = [[1,2,3],[4,5,9],[8,7,6]]
wm7 = [[1,9,8],[4,2,3],[7,5,6]]
wm4 = [[8, 1, 3], [4, 2, 6], [7, 5, 9]]
wm5 = [[1,2,3], [4, 6,5], [7, 8, 9]]
wm6 = [[1,2,3,4], [5,6,7,8], [9,10,12,11], [13,14,15,16]]
wm8 = [[1,2,3,4], [5,6,7,9], [8,10,11,12], [13,14,15,16]]
wrong_matrix = wm6


print("Wrong matrix(randomly genrated) : ", wrong_matrix)

initialp1 = where_is_no(wrong_matrix,max1)
initialp2 = where_is_no(wrong_matrix,max2)
initialflag = 2
Avoid_move_initial = -3


temp_rm = bfs(wrong_matrix,initialflag,Avoid_move_initial, initialp1,initialp2, rm1,rm2) #call bfs

print("Path is: ") #printing path
pathlist = []
pathlist.append(temp_rm)
temp = s.index(temp_rm)
tempparent = parent[temp]
tempmove = tran[temp]
tempflag = tranflag[temp]
# print(tempparent, tempmove)
pathlist.append((tempparent, tempmove, tempflag))
while(tempparent != wrong_matrix):
    temp = s.index(tempparent)
    tempparent = parent[temp]
    tempmove = tran[temp]
    tempflag = tranflag[temp]
    # print(tempparent, tempmove)
    pathlist.append((tempparent, tempmove, tempflag))

for i in range(len(pathlist)):
    j = len(pathlist) - 1 - i
    print(pathlist[j])

