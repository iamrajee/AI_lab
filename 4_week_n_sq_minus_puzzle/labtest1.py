'''
#-------------------------------------Author-----------------------------------------------#
Rajendra singh(111601017)

#-------------------------------------Logic------------------------------------------------#
1) Here i used a star Algorithem to solve the problem to solve the problem. Heuritcs here is manhartan distance
2) At any configration maximum of 8 move are possible
3) These moves are ["right","up","left","down"] for both empty blocks(i.e 4+4=8)
4) For Initial configration, i'm taking all above possible move and puting them in priorty queue(here we need not to check the parity as it can alway be made equal to 0, i.e alway reachable) and also storing these configration in a list(which tells about visited states)
5)If queue is not empty then i pop one element(based on heuristic values) and call the a_star again on this poped element
6)If this poped element is equal to any of correct state(two correct state possible rm1, rm2) that means ours task is done.
7) we also store the parent,which block did we moved, direction of movement in an another list(parent, flaglist, tran) for any move so that we can print the path later in reverse order
8)Then, we print the path along with which block we moved and direction of movement
'''





#-------------------------------------Imports--------------------------------------------------------#
import numpy as np
import random
# from queue import Queue
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
import copy


#-------------------------------Initialisation and declaration----------------------------------#
N = 4 # matrix of N*N
r, c = N,N
rm2 = [[y*N+x for x in range(1,c+1)] for y in range(r)] #here rm1 and rm2 are the two possible configuration for correct state

rm1 = copy.deepcopy(rm2)
lastele = rm1[N-1][N-1]
rm1[N-1][N-1] = rm1[N-1][N-2]
rm1[N-1][N-2] = lastele

# print("Correct matrix2 = ", rm2)
# print("Correct matrix1 = ", rm1)



#-----------------------------------------Creating any random matrix-------------------------------------#
b = random.sample(range(1,1+N**2), N**2)
b = np.array(b)
wm2 = [[ b[y*N+x] for x in range(c)] for y in range(r)]


#----------------------------------------------------No. inside two empty block-------------------------#
max1 = N*N-1
max2 = N*N



#--------------------------------------------------Heuristic function--------------------------------------------#
def heu2(m):
    sum = 0
    flagblock = 0
    for i in range(N):
        for j in range(N):
            ele = rm2[i][j]
            tp = where_is_no(m,ele)
            if ele != max1 and ele != max2:
                sum += abs(i-tp[0])  + abs(j-tp[1])
            elif flagblock == 0:
                sum += abs(i-tp[0])  + abs(j-tp[1])
                tempsum2 = abs(N-1-tp[0])  + abs(N-1-tp[1])
                tempsum1 = abs(N-1-tp[0])  + abs(N-2-tp[1])
                if tempsum1 > tempsum2:
                    sum += tempsum1
                    flagblock = 1
                else:
                    sum += tempsum2
                    flagblock = 2
            elif flagblock == 1:
                tempsum2 = abs(N-1-tp[0])  + abs(N-1-tp[1])
                sum += tempsum2
            else:
                tempsum1 = abs(N-1-tp[0])  + abs(N-2-tp[1])
                sum += tempsum1
    return sum# + N**2-2


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
            wmmovelist.append(r)
            previous_flag = flag
            previous_move = r

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
q = Q.PriorityQueue()
s = [] #list of visited matrix
parent = [] #parent of above
tran = []
tranflag = []


#------------------------Order of movements and block-------------------------------------------#
moveorder = ["right","up","left","down"]
flagorder = [1,2]

count = 0
#---------------------------------------------Give the Input state here--------------------------------------------------#
wm3 = [[1,2,3],[4,5,9],[8,7,6]]
wm7 = [[1,9,8],[4,2,3],[7,5,6]]
wm4 = [[8, 1, 3], [4, 2, 6], [7, 5, 9]]
wm5 = [[1,2,3], [4, 6,5], [7, 8, 9]]
wm6 = [[1,2,3,4], [5,6,7,8], [9,10,12,11], [13,14,15,16]]
wm8 = [[1,2,3,4], [5,6,7,9], [8,10,11,12], [13,14,15,16]]
wm9 = [[1,2,3,4], [5,6,7,8], [12,10,11,9], [13,14,15,16]]
wm10 = [[1,2,3,4], [5,6,7,9], [8,10,12,11], [13,14,15,16]]
wrong_matrix = wm10

#---------------------------------#
# wrong_matrix = 
tp1i = where_is_no(wrong_matrix,max1)
tp2i = where_is_no(wrong_matrix,max2)
def gnf(m):
    tp1 = where_is_no(m,max1)
    tp2 = where_is_no(m,max2)
    return1 = abs(tp1[0]-tp1i[0])+abs(tp1[1]-tp1i[1])+abs(tp2[0]-tp2i[0])+abs(tp2[1]-tp2i[1])
    return2 = abs(tp1[0]-tp2i[0])+abs(tp1[1]-tp2i[1])+abs(tp2[0]-tp1i[0])+abs(tp2[1]-tp1i[1])
    if return1 > return2:
        return return1
    else:
        return return2

#--------------------------------A_function function----------------------------------------#
def a_star(count,twm,flag,avoidmove,p1,p2,trm1, trm2,gn):
    count +=1
    print(count,gn)#,len(s))
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
                            temph = heu2(child) + gnf(child)
                            print("heu2 = ", temph)
                            if f ==1:
                                temptuple = (temph,child,f,oppmove(move),nextp(p,move),p2,gn+1)
                            else:
                                temptuple = (temph,child,f,oppmove(move),p1, nextp(p,move),gn+1)
                            q.put(temptuple) #inserting in priorty queue
                            s.append(child) #inserting in visited list
                            parent.append(twm) #inserting in parent list
                            tran.append(move) #storing move
                            tranflag.append(f) #storing move

        # print("queue length :", q.qsize() )
        if(q.empty() != 1): #if queue not empty
            temptuple2 = copy.deepcopy(q.get()) #pop element
            child = temptuple2[1]
            flag = temptuple2[2]
            avoidmove = temptuple2[3]
            p1 = temptuple2[4]
            p2 = temptuple2[5]
            # gn = temptuple[6]
            return a_star(count,copy.deepcopy(child),flag,avoidmove,copy.deepcopy(p1),copy.deepcopy(p2),trm1,trm2,temptuple2[6]) #call a_star again
    else:
        print("\n\n\n **************TASK IS DONE*************")
        return twm
        






#---------------------------------------Printing Initial and Posssible final state--------------------------------------------------#
print("\nInitial State : ", wrong_matrix)
print("\nTwo possible final state: ")
print(rm2)
print(rm1)



#-----------------------------------------------------Initial Arguments for a_star---------------------------------------------------#
initialp1 = where_is_no(wrong_matrix,max1)
initialp2 = where_is_no(wrong_matrix,max2)
initialflag = 2
Avoid_move_initial = -3
initial_gn = 0


#----------------------------------------------------Calling a_star------------------------------------------------------#
temp_rm = a_star(count,copy.deepcopy(wrong_matrix),initialflag,Avoid_move_initial, copy.deepcopy(initialp1),copy.deepcopy(initialp2), rm1,rm2,initial_gn) #call a_star

print("\n Actual final state = ", temp_rm)





#--------------------------------------------------Printing path-------------------------------------------#
print("\nPath is(e.g: 1 mean block 15 and 2 mean block 16): ") #printing path
pathlist = []
pathlist.append(temp_rm)
temp = s.index(temp_rm)
tempparent = parent[temp]
tempmove = tran[temp]
tempflag = tranflag[temp]
pathlist.append((tempparent, tempmove, tempflag))
while(tempparent != wrong_matrix):
    temp = s.index(tempparent)
    tempparent = parent[temp]
    tempmove = tran[temp]
    tempflag = tranflag[temp]
    pathlist.append((tempparent, tempmove, tempflag))

for i in range(len(pathlist)):
    j = len(pathlist) - 1 - i
    print(pathlist[j])

print("")
print("No. of steps = ",len(pathlist))




