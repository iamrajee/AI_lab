#-------------------------------------Imports--------------------------------------------------------#
import numpy as np
import random
from queue import Queue
import copy



#-------------------------------Initialisation and declaration----------------------------------#
N = 4
gamma = 0.9 #discount factor
State = np.zeros((N,N), dtype=int)
no_of_state = N*N
no_of_iter = 1000

no_of_rewards = 10
reward_limit = 100

for i in range(N):
    for j in range(N):
        State[i,j] = i*N+j 

def where_is_no(matrix,tempno):
    templist = np.array(matrix)
    x = np.where(matrix == tempno)
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


Actionlist = ["R", "U", "L", "D"]
rewards = {}
while(len(rewards)<no_of_rewards):
    randomstate = random.randint(1,no_of_state-1)
    randomaction = random.choice(Actionlist)
    predicted_state = next_state_fun(State,randomaction,randomstate,-1)
    randomreward = random.randint(0,reward_limit)

    flag = 0
    for (s,a) in rewards.keys():
        if (s == randomstate):
            flag = 1

    if (randomstate,randomaction) not in rewards and predicted_state != -1 and flag ==0:
        rewards.update({(randomstate,randomaction):randomreward})



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

# define and initialise V[s][0]
V = np.zeros(N*N, dtype=float)
pi = np.zeros(N*N, dtype=int)

def Value_iter(V,pi,noi):
    for k in range(noi):
        prev_V = np.copy(V)
        # print("k=",k,"    prev_V=",prev_V)
        for s in range(no_of_state):
            max = 0
            j_wrt_max = 0
            for j,a in enumerate(Actionlist):
                predicted_state = next_state_fun(State,a,s,-1)
                if predicted_state ==-1:
                    continue
                if (s,a) in rewards.keys():
                    curr_reward = rewards[(s,a)]
                else:
                    curr_reward = 0
                expected_future_reward = 0
                for next_s in range(no_of_state): #summation(T.V(t-1))
                    expected_future_reward +=(Transition_prob[s,next_s,j]*V[next_s])
                expected_curr_reward = curr_reward + (gamma*expected_future_reward)
                if expected_curr_reward > max:
                    max = expected_curr_reward
                    j_wrt_max = j
            V[s] = max
            pi[s] = j_wrt_max
        #--------converging condition for value----#
        if(list(prev_V) == list(V)):
            break
    return np.copy(V),np.copy(pi),k



def Policy_iter(V,pi,noi):
    for k in range(noi):
        prev_pi = np.copy(pi)
        # print("k=",k,"    prev_V=",prev_V)
        for s in range(no_of_state):
            
            #------Value evaluate from previous policy
            j = prev_pi[s]
            a = Actionlist[j]
            if (s,a) in rewards.keys():
                curr_reward = rewards[(s,a)]
            else:
                curr_reward = 0
            expected_future_reward = 0
            for next_s in range(no_of_state): #summation(T.V(t-1))
                expected_future_reward +=(Transition_prob[s,next_s,j]*V[next_s])
            expected_curr_reward = curr_reward + (gamma*expected_future_reward)
            V[s] = expected_curr_reward
            #------

            #------updating policy
            max = 0
            j_wrt_max = 0
            for j,a in enumerate(Actionlist):
                predicted_state = next_state_fun(State,a,s,-1)
                if predicted_state ==-1:
                    continue
                if (s,a) in rewards.keys():
                    curr_reward = rewards[(s,a)]
                else:
                    curr_reward = 0
                expected_future_reward = 0
                for next_s in range(no_of_state): #summation(T.V(t-1))
                    expected_future_reward +=(Transition_prob[s,next_s,j]*V[next_s])
                expected_curr_reward = curr_reward + (gamma*expected_future_reward)
                if expected_curr_reward > max:
                    max = expected_curr_reward
                    j_wrt_max = j
            pi[s] = j_wrt_max

        #--------converging condition for policy----#
        if(list(prev_pi) == list(pi)):
            break
    return np.copy(V),np.copy(pi),k

print("State =\n",State)

reward_grid = np.zeros(N*N,  dtype=[('foo', 'i4'), ('baz', 'S10')])
for s in range(no_of_state):
    for a in Actionlist:
        if (s,a) in rewards.keys():
            reward_grid[s] = (rewards[(s,a)],a)

reward_grid = reward_grid.reshape(N,N)
# print("rewards=",rewards)
print("rewards grid =\n",reward_grid)

print("\n**************************Value iter********************")
optimalvalue_V,optimalvalue_pi,optimalvalue_no_of_iter = Value_iter(np.copy(V),np.copy(pi),no_of_iter) #take random input (V,pi,no_of_iter), output optimal (V,pi,no_of_iter)
print("optimal_V=\n",np.around(optimalvalue_V, decimals=1).reshape(N,N))

optimalvalue_pi_ch = np.chararray((N, N))
for i in range(N):
    for j in range(N):
        optimalvalue_pi_ch[i,j] = Actionlist[optimalvalue_pi.reshape(N,N)[i,j]]
print("optimal_pi=\n",optimalvalue_pi_ch)
print("optimal_no_of_iter=",optimalvalue_no_of_iter)


print("\n**********************Policy iter********************")
optimalpolicy_V,optimalpolicy_pi,optimalpolicy_no_of_iter = Policy_iter(np.copy(V),np.copy(pi),no_of_iter) #take random input (V,pi,no_of_iter), output optimal (V,pi,no_of_iter)
optimalpolicy_pi_ch = np.chararray((N, N))
for i in range(N):
    for j in range(N):
        optimalpolicy_pi_ch[i,j] = Actionlist[optimalpolicy_pi.reshape(N,N)[i,j]]
print("optimal_V=\n",np.around(optimalpolicy_V, decimals=1).reshape(N,N))
print("optimal_pi=\n",optimalpolicy_pi_ch)
print("optimal_no_of_iter=",optimalpolicy_no_of_iter)