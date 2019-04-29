#---------------------------------Necessary import-------------------------#
import numpy as np
import math
import copy
import itertools
#----------------------------------Change variable here-----------------------#
actions = []
for i in range(-5,6):
    for j in range(-5,6):
        for k in range(-5,6):
            if i+j+k == 0:
                actions.append((i,j,k))
n_a = len(actions) #no of action
print(n_a, actions)
def trancost(ts):
    return np.abs(ts[0])

n1,n2,n3 = 5,5,5
maxn1,maxn2,maxn3 = 9,5,5

lambda_req = [3,2,2]
lambda_ret = [3,1,1]

no_of_iter = 1
gamma = 0.9
#------------------------------------Get prob. function-------------------------#
def poisson(tn, tlamda):
    s = (tlamda**tn)*(math.exp(-tlamda))/math.factorial(tn)
    return s
    

print(poisson(5,3))

#============================
JointProbLocation1 = np.ones((maxn1, maxn1, maxn1, maxn1))*1000
JointProbLocation2 = np.ones((maxn2, maxn2, maxn2, maxn2))*1000
JointProbLocation3 = np.ones((maxn3, maxn3, maxn3, maxn3))*1000
JointRewardLocation1 = np.ones((maxn1, maxn1, maxn1, maxn1))*1000
JointRewardLocation2 = np.ones((maxn2, maxn2, maxn2, maxn2))*1000
JointRewardLocation3 = np.ones((maxn3, maxn3, maxn3, maxn3))*1000
# print("shape:", np.shape(JointProbLocation1))
ProbRequestLocation1 = np.asarray([poisson(lambda_req[0], i) for i in range(maxn1)])
ProbRequestLocation2 = np.asarray([poisson(lambda_req[1], i) for i in range(maxn2)])
ProbRequestLocation3 = np.asarray([poisson(lambda_req[2], i) for i in range(maxn3)])

RewardRequestLocation1 = np.asarray([poisson(lambda_req[0], i)*i*10 for i in range(maxn1)])
RewardRequestLocation2 = np.asarray([poisson(lambda_req[1], i)*i*10 for i in range(maxn2)])
RewardRequestLocation3 = np.asarray([poisson(lambda_req[2], i)*i*10 for i in range(maxn3)])

ProbReturnLocation1 = np.asarray([poisson(lambda_ret[0], i) for i in range(maxn1)])
ProbReturnLocation2 = np.asarray([poisson(lambda_ret[1], i) for i in range(maxn2)])
ProbReturnLocation3 = np.asarray([poisson(lambda_ret[2], i) for i in range(maxn3)])


for (reqStart, reqEnd, retStart, retEnd) in itertools.product(np.arange(maxn1), np.arange(maxn1), np.arange(maxn1), np.arange(maxn1)):  #start, End inclusive
    if(reqEnd - reqStart + 1 != retEnd - retStart + 1):
        continue
        
    JointProbLocation1[reqStart, reqEnd, retStart, retEnd] = np.sum(
        ProbRequestLocation1[reqStart:reqEnd+1]*ProbReturnLocation1[retStart:retEnd+1])
    JointRewardLocation1[reqStart, reqEnd, retStart, retEnd] = np.sum(
        RewardRequestLocation1[reqStart:reqEnd+1]*ProbReturnLocation1[retStart:retEnd+1])
    
for (reqStart, reqEnd, retStart, retEnd) in itertools.product(np.arange(maxn2), np.arange(maxn2), np.arange(maxn2), np.arange(maxn2)):
    if(reqEnd - reqStart + 1 != retEnd - retStart + 1):
        continue
    
    JointProbLocation2[reqStart, reqEnd, retStart, retEnd] = np.sum(
        ProbRequestLocation2[reqStart:reqEnd+1]*ProbReturnLocation2[retStart:retEnd+1])
    JointRewardLocation2[reqStart, reqEnd, retStart, retEnd] = np.sum(
        RewardRequestLocation2[reqStart:reqEnd+1]*ProbReturnLocation2[retStart:retEnd+1])
    
for (reqStart, reqEnd, retStart, retEnd) in itertools.product(np.arange(maxn3), np.arange(maxn3), np.arange(maxn3), np.arange(maxn3)):
    if(reqEnd - reqStart + 1 != retEnd - retStart + 1):
        continue
    
    JointProbLocation3[reqStart, reqEnd, retStart, retEnd] = np.sum(
        ProbRequestLocation3[reqStart:reqEnd+1]*ProbReturnLocation3[retStart:retEnd+1])
    JointRewardLocation3[reqStart, reqEnd, retStart, retEnd] = np.sum(
        RewardRequestLocation3[reqStart:reqEnd+1]*ProbReturnLocation3[retStart:retEnd+1])
#============================

V = np.zeros((maxn1+1, maxn2+1, maxn3+1))
policy = np.zeros((maxn1+1, maxn2+1, maxn3+1))
# print("V",np.shape(V))

def isvalidstate(tn1,tn2,tn3):
    if tn1 >= 0 and tn2 >= 0 and tn3 >= 0 and tn1 <= maxn1 and tn2 <= maxn2 and tn3 <= maxn3:
        return 1
    else:
        return 0
#==================================================================================
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
    policy = np.zeros (prev_V.shape , dtype = int)
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
            print("a_wrt_max:",a_wrt_max)
            policy[state1,state2,state3] = a_wrt_max

    return  np.copy (temp_V) ,np.copy(policy)

#--------------------------------------Calling-----------------------------------------------#
initial_State = (n1,n2,n3)
initial_V = np.zeros ((maxn1,maxn2,maxn3)) #for each stat
policy = np.zeros (initial_V.shape , dtype = np.int)
final_V , policy= bellman (initial_V,initial_State)
'''
#---------------------------------------Saving-----------------------------------------------#
np.set_printoptions(formatter={'float': '{: 0.0f}'.format})
np.savetxt("policy.txt" , policy , fmt = "%i")
np.savetxt("value.txt" , final_V , fmt = "%i")

'''
