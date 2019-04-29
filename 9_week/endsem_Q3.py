#---------------------------------Necessary import-------------------------#
import numpy as np
import math
import copy
import itertools
#----------------------------------Change variable here-----------------------#
n1,n2,n3 = 5,5,5
maxn1,maxn2,maxn3 = 9,5,5

lambda_req = [3,2,2]
lambda_ret = [3,1,1]

no_of_iter = 10
gamma = 0.9

#----------------------------------List of actions-----------------------#
actions = []
for i in range(-5,6):
    for j in range(-5,6):
        for k in range(-5,6):
            if i+j+k == 0:
                actions.append((i,j,k))
n_a = len(actions) #no of action
print("Total no. of possible action:", n_a,"\nAll possible action are : \n", actions)



#----------------------------------Transporting cost over night for action ts-----------------------#
def trancost(ts):
    return np.abs(ts[0])


#------------------------------------Get prob. function-------------------------#
def poisson(tn, tlamda):
    s = (tlamda**tn)*(math.exp(-tlamda))/math.factorial(tn)
    return s
    
#----------------------------------Initialise-----------------------#
V = np.zeros((maxn1+1, maxn2+1, maxn3+1))

#---------------------------------Wheither state is valid or not-----------------------#
def isvalidstate(tn1,tn2,tn3):
    if tn1 >= 0 and tn2 >= 0 and tn3 >= 0 and tn1 <= maxn1 and tn2 <= maxn2 and tn3 <= maxn3:
        return 1
    else:
        return 0

#---------------------------------- Get probabilty function -----------------------#
def get_prob(ts,ts_):
    #prob of being in new state is:
    delta = []
    req = []
    ret = []
    tprob = []
    for i in range(3):
        delta.append(ts_[i] - ts[i])
    for i in range(3):
        req.append(max(0,-delta[i]))
    for i in range(3):
        ret.append(max(0,delta[i]))
   
    for i in range(3):
        tlambda_req = lambda_req[i]
        tlambda_ret = lambda_ret[i]
        templist = []
        for r,_ in enumerate(range(req[i],ts[i]+1)):#for all request in (orignal req,maxpossible_request)
            treq = req[i] + r
            tret = ret[i] + r
            templist.append( poisson(treq,tlambda_req)*poisson(tret,tlambda_ret) )
        tprob.append(np.sum(templist))
    return tprob



#-------------------------------------Bellman value iteration function-------------------------#
def bellman (prev_V, state):
    temp_V = np.zeros (prev_V.shape)
    # policy = np.zeros (prev_V.shape , dtype = int)
    policy = []
    for i in range(maxn1+1):
        policy2 = []
        for j in range(maxn2+1):
            policy1 = []
            for k in range(maxn3+1):
                policy1.append(None)
            policy2.append(policy1)
        policy.append(policy2)
    print(state)
    for i in range(no_of_iter):
        for state1,state2,state3 in itertools.product(np.arange(maxn1+1),np.arange(maxn2+1),np.arange(maxn3+1)):
            maxvalue = -10000000
            a_wrt_max = -1
            for a in actions:
                nextstate1=state1+a[0]
                nextstate2=state2+a[1]
                nextstate3=state3+a[2]
                if isvalidstate(nextstate1,nextstate2,nextstate3) == 1:
                    cost = trancost(a)
                    reward = 0.0 - cost #negative of cost
                    for s1,s2,s3 in itertools.product(np.arange(maxn1+1),np.arange(maxn2+1),np.arange(maxn3+1)):#new state after all request and return
                        prob = get_prob((nextstate1,nextstate2,nextstate3),(s1,s2,s3))
                        reward += gamma*np.product(prob)*V[s1,s2,s3]
                    # tempV = reward
                    if reward > maxvalue:
                        V[state1,state2,state3] = reward
                        maxvalue = reward
                        a_wrt_max = a
            print("a_wrt_max:",a_wrt_max,type(a_wrt_max))
            policy[state1][state2][state3] = a_wrt_max# a_wrt_max #<upgrading policy #but causing error so commented

    return  np.copy (temp_V) ,np.copy(policy)

#--------------------------------------Calling-----------------------------------------------#
initial_State = (n1,n2,n3)
initial_V = np.zeros ((maxn1,maxn2,maxn3)) #for each stat
final_V , policy= bellman (initial_V,initial_State)
print(policy)
