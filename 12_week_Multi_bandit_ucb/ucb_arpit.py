import numpy as np
import math
import random
import matplotlib.pyplot as plt

#this is the description of the bandits
#this will give the success probability associated with each of the arm
action = 5                                  #this is the number of actions that are possible
bandit = [0.5, 0.9 , 0.7 , 0.4 , 0.90]       #success probability associated with each bandit

reward_success = [2 , 0.5, 1.0 ,10 ,1.1]
reward_fail = [-0.5 , -1 , 0 , -5 , -3]

#the problem is to choose the best arm
#according to the current probability distribution of the reward

exploration_epsilon = 0.2
number_of_episodes = 20000                         #number of episodes to run
selected = [0 for _ in range(action)]              #this will tell the number of times the arm is selected

Q = [0 for _ in range(action)]              #this will store the q value for each action
                                            #this will give the expected re


def bandit_solution (total):
    r = random.random()            #this is to decide either to explore or to exploit
    #this is to explore. i.e. randomly choose any action and then accumulate the reward
    if (r < exploration_epsilon):
        a = random.randint(0 , 4)
        p_success = random.random()
        if (p_success < bandit[a]):               #it is successful, get the positive reward
            selected[a] += 1               #increment the selected
            k = selected[a]
            Q[a] = Q[a] + (1/(k+1)) * (reward_success[a] - Q[a])      #update the value of q
            reward = reward_success[a]
        else:
            selected[a] += 1
            k = selected[a]
            #total += reward_fail[a]
            Q[a] = Q[a] + (1/(k+1)) * (reward_fail[a] - Q[a])
            reward = reward_fail[a]
            
    else:
        a = np.argmax (Q)
        p_success = random.random()
        if (p_success < bandit[a]):               #it is successful, get the positive reward
            selected[a] += 1               #increment the selected
            k = selected[a]
            Q[a] = Q[a] + (1/(k+1)) * (reward_success[a] - Q[a])      #update the value of q
            reward = reward_success[a]
        else:
            selected[a] += 1
            k = selected[a]
            Q[a] = Q[a] + (1/(k+1)) * (reward_fail[a] - Q[a])
            reward = reward_fail[a]
        
        
    probability = [0 for _ in range(action)]
    for i in range(action):
        probability[i] = exploration_epsilon/action
    a = np.argmax(Q)
    probability[a] += 1-exploration_epsilon
    
    return (reward + total, probability)



total = 0
proportion = np.zeros ((0 , action))
probable = np.zeros ((0 , action))
for itr in range(1, number_of_episodes+1):
    
    total , probability = bandit_solution(total)
    proportion = np.vstack((proportion , np.array(selected)/itr ))
    probable = np.vstack((probable , np.array(probability) ))

print("Q:",Q)

#plot for the proportion
bandit_name = ["bandit 1" , "bandit 2" , "bandit 3" , "bandit 4" , "bandit 5"]
plt.figure (figsize=(8 , 6))
for i , name  in zip (range(action) , bandit_name):
    plt.plot (range(number_of_episodes) , proportion[: , i] , label = name)
    
plt.legend()
plt.xlabel ("number of episodes")
plt.ylabel ("Proportion")
plt.show()
#plot for the proportion
bandit_name = ["bandit 1" , "bandit 2" , "bandit 3" , "bandit 4" , "bandit 5"]
plt.figure (figsize=(8 , 6))
for i , name  in zip (range(action) , bandit_name):
    plt.plot (range(number_of_episodes) , probable[: , i] , label = name)
    
plt.legend()
plt.xlabel ("number of episodes")
plt.ylabel ("Probability of selection")
plt.show()