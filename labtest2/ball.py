#--------constraints-
#ball cant bowled more than 1 player in a over 

#---------------------------------Necessary import-------------------------#
import numpy as np
import math
import itertools
import random
#----------------------------------Change variable here-----------------------#
n_baller = 5 #no of ballers
n_over = 10#no of over
who_balled = [0,0,1,1,2,2,3,3,4,4]
n_wicket = 3#no of wicket
# runs = [1,2,3,4,6]#possible runs
strikerate = [(3,33),(3.5,30),(4,24),(4.5,18),(5,15)]

run_wicket_prob = []
for ele in strikerate:
    run_wicket_prob.append((ele[0], (1/ele[1])*6))

n_over_balled = np.zeros(5)
print("run_wicket_prob = ",run_wicket_prob)
# print(n_over_balled)


olpblist = []
my_list = [0,1,2]
for tuple_ in itertools.product(my_list, repeat=5):
    olpblist.append(tuple_)
    # print(tuple_)

len_olpblist = len(olpblist)

#-------------------------------------Bellman value iteration function-------------------------#
def bellman (prev_V): #formula => V[st]=max_over_a{R[a]+sumation{P(st).V[s:t-1]}}, reward here is amount of run scored
    # print("bellman",prev_V.shape)
    V = np.full (prev_V.shape,0)
    policy = np.zeros (prev_V.shape , dtype = int)
    w = n_wicket-1
    olpb = [2,2,2,2,2]
    # actionlist = [0,0,1,1,2,2,3,3,4,4]
    sum = 0
    optimal_over = []
    for o in range(n_over):
        # print("i = ",i,"w = ",w,"olpb = ",olpb)
        if w == -1:
            print("******************allout***************************")
            break 
        o=(n_over-1)-o
        # for w in range(n_wicket):
        #     w = (n_wicket-1)-w
        #     for olpb in olpblist:
        #         olpb = list(olpb)
        min_temp = 100000000
        a_wrt_min = 0
        actionlist = []
        for i,ele in enumerate(olpb):
            for j in range(ele):
                actionlist.append(i)
        for a in np.unique(actionlist):#minimum over action
            # temp_actionlist = actionlist
            curr_v = (1-run_wicket_prob[a][1]) * (run_wicket_prob[a][0] + V[o-1][w][olpblist.index(tuple(olpb))])    #when no is out
            # temp_actionlist.remove(a)
            # olpb[a] -=1
            curr_v += run_wicket_prob[a][1] * (run_wicket_prob[a][0] + V[o-1][w-1][olpblist.index(tuple(olpb))])        #when one player is out
            if(curr_v<min_temp):
                min_temp = np.round(curr_v,3)
                a_wrt_min = a
            # print(a)
        if a_wrt_min in actionlist:
             
            # print("a_wrt_min = ",a_wrt_min, "olpb = ",olpb )
            # print("o = ",o+1,"w = ",w,"olpb = ",olpb," ===>  a_wrt_min = ",a_wrt_min)
            # actionlist.remove(a_wrt_min)
            olpb[a_wrt_min] -=1
            if random.uniform(0,1) < run_wicket_prob[a_wrt_min][1]:
                w-=1
            V[o][w][olpblist.index(tuple(olpb))] = min_temp
            policy[o][w][olpblist.index(tuple(olpb))] = a_wrt_min
            print("o = ",o+1,"w = ",w+1,"a_wrt_min = ",a_wrt_min+1," ===>  olpb = ",olpb,"min_temp = ",min_temp)
            sum+=min_temp
            optimal_over.append(a_wrt_min+1)
        else:
            print("warning")
    print("optimal_run = ", sum," optimal_over = ", optimal_over)    
    return  np.copy (V) ,np.copy(policy)

#--------------------------------------Calling-----------------------------------------------#
initial_V = np.zeros((n_over,n_wicket,len_olpblist)) #for each state              ###why n_ball+1 bcz 0,1,....,n_ball ball left
policy = np.zeros (initial_V.shape , dtype = np.int)
final_V , policy= bellman (initial_V)

# print("final_V = \n", final_V)
# print("policy = \n")
# for ele in policy:
#     print(ele)
left = 9
# w_left = 2
# for i in range(10):
#     if i == 0:
#         temp_olpb = [2,2,2,2,2]
#         a = policy[left][w_left][olpblist.index(tuple(temp_olpb))]
#         print(a)
#         temp_olpb[a] -=1 
#         left -=1
#         if random.uniform(0,1) < run_wicket_prob[a][1]:
#             w_left-=1

#     else:
#         a = policy[left][w_left][olpblist.index(tuple(temp_olpb))]
#         print(a)


# #---------------------------------------Saving-----------------------------------------------#
# np.set_printoptions(formatter={'float': '{: 0.0f}'.format})
# np.savetxt("policy.txt" , policy , fmt = "%i")
# np.savetxt("value.txt" , final_V , fmt = "%i")
