#-------------------------------------Imports--------------------------------------------------------#
import numpy as np
import random
from queue import Queue
import copy



#-------------------------------Initialisation and declaration----------------------------------#
N = 2
lamda = 0.9 #discount factor
State = np.zeros((N,N), dtype=int)
no_of_state = N*N
no_of_iter = 6
for i in range(N):
    for j in range(N):
        State[i,j] = i*N+j 
print(State)

Actionlist = ["L", "U", "R", "D"]
rewards = {}
no_of_rewards = 5
reward_limit = 100
while(len(rewards)<no_of_rewards):
    randomstate = random.randint(0,no_of_state)
    randomaction = random.choice(Actionlist)
    randomreward = random.randint(0,reward_limit)
    if (randomstate,randomaction) not in rewards:
        rewards.update({(randomstate,randomaction):randomreward})

print(rewards)
def where_is_no(matrix,tempno):
    templist = np.array(matrix)
    x = np.where(templist == tempno)
    p = (x[0][0], x[1][0])
    return p

def next_state_fun(matrix,move,current_state,p):
    if p == -1:
        p = where_is_no(matrix,current_state)
    i,j = p[0],p[1]
    if move == "R":
        if j != N-1:
           t = matrix[i][j+1]
        else:
            return -1

    elif move == "U":
        if i != 0:
           t = matrix[i-1][j]
        else:
            return -1
    elif move == "L":
        if j != 0:
           t = matrix[i][j-1]
        else:
            return -1
    elif move == "D":
        if i != N-1:
           t = matrix[i+1][j]
        else:
            return -1
    return t


Transition_prob = np.zeros((N*N,N*N,len(Actionlist)), dtype=float)

for current_state in range(N*N):
    for j in range(len(Actionlist)):
        action = Actionlist[j]
        predicted_state = next_state_fun(State,action,current_state,-1)
        main_prob = random.randint(5,10)/10
        if predicted_state != -1:
            other_prob = (1 - main_prob)/(N*N-1)
        else:
            other_prob = 1/(N*N)
        
        for next_state in range(N*N):
            if next_state == predicted_state:
                Transition_prob[current_state,next_state,j] =  main_prob
            else:
                Transition_prob[current_state,next_state,j] = other_prob
    


# print(Transition_prob, type(Transition_prob),Transition_prob.shape)

# count = 0
# for action in range(4):
#     for i in range(N*N):
#         sum = 0
#         for k in range(N*N):
#             sum += Transition_prob[i][k][action]
#             count+=1
#         print(sum)
# print("count=", count)

#define and initialise V[s][0]
V = np.zeros((no_of_iter,N*N), dtype=float)
pi = np.zeros((no_of_iter,N*N), dtype=int)
# print(pi)
for s in range(no_of_state):
    max = 0
    for a in Actionlist:
        if (s,a) in rewards.keys():
            temp_reward = rewards[(s,a)]
        else:
            temp_reward = 0
        if temp_reward > max:
            max = temp_reward
    V[no_of_iter-1][s] = max

# print(V)


def fun_V(temp_k,s):
    if temp_k == no_of_iter-1:
        return V[no_of_iter-1][s]
    max = 0
    j_wrt_max = 0
    for j,a in enumerate(Actionlist):
        if (s,a) in rewards.keys():
            temp_reward = rewards[(s,a)]
        else:
            temp_reward = 0

        other_part = 0
        for next_s in range(no_of_state):
            other_part +=(lamda*Transition_prob[s,next_s,j]*fun_V(temp_k+1,next_s)) //function or iteration
        sum_temp = temp_reward+other_part
        if sum_temp > max:
            max = sum_temp
            j_wrt_max = j
    # V[temp_k][s] = max
    pi[temp_k][s] = j_wrt_max
    return max

for k in range(no_of_iter):
    k = (no_of_iter-1)-k
    print("k=",k)
    for s in range(no_of_state):
        print("s=",s)
        V[k][s] = fun_V(k,s)
    print(V[k],pi[k])
print(V)



