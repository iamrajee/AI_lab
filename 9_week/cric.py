#---------------------------------Necessary import-------------------------#
import numpy as np

#----------------------------------Change variable here-----------------------#
n_a = 5 #no of action
n_ball = 300#no of ball
n_wicket = 11#no of wicket
runs = [1,2,3,4,6]#possible runs

#------------------------------------Get prob. function-------------------------#
def get_prob (a , n_ball_temp):
    if (n_ball_temp < 1 or n_ball_temp > 10 ):#return for invalid
        return (-1 , -1)
    #prob. for [1,2,3,4,6] runs
    pw_best = [0.02, 0.04, 0.08, 0.16, 0.32]        #best player wicket prob low
    pw_worst = [0.05, 0.1, 0.2, 0.4, 0.8]           #worst player wicket prob high
    pw = pw_worst[a] + (pw_best[a] - pw_worst[a]) * ( (n_ball_temp-1)/9 )#given formulla
    
    pr_worst = 0.4#worst player run prob low         #prob of scoring if not out
    pr_best = 0.8#best player run prob high
    pr = pr_worst + (pr_best - pr_worst) * ( (n_ball_temp-1)/9)#given

    return (pw , pr)

#-------------------------------------Bellman value iteration function-------------------------#
def bellman (prev_V): #formula => V[st]=max_over_a{R[a]+sumation{P(st).V[s:t-1]}}, reward here is amount of run scored
    temp_V = np.zeros (prev_V.shape)
    policy = np.zeros (prev_V.shape , dtype = int)
    #---------for all states finding best action and V
    for i in range(1 , prev_V.shape[0]):#--------------rows = #balls left
        for j in range(1 , prev_V.shape[1]):#----------columns = #wicket left
            max_temp = -1
            a_wrt_max = 0
            for a in range(n_a):#maximum over action
                sum_temp = 0
                #suming over 3 possible states(out,run,no-run-no-out)
                pw , pr = get_prob (a , j)
                sum_temp += pw * (0 + temp_V[i-1][j-1]) #out                                    #reward=0, Tran_prob = pw
                sum_temp += (1-pw) * pr* (runs[a] + temp_V[i-1][j] ) #run                       #reward=runs[a], Tran_prob = (1-pw) * pr
                sum_temp += (1 - pw) * (1-pr) * (0 + temp_V[i-1][j])#not-out and no run        #reward=0, Tran_prob = (1 - pw) * (1-pr)
                if (sum_temp > max_temp):
                    max_temp = sum_temp
                    a_wrt_max = a

            policy[i][j] = runs[a_wrt_max]
            temp_V[i][j] = max_temp
    return  np.copy (temp_V) ,np.copy(policy)

#--------------------------------------Calling-----------------------------------------------#
initial_V = np.zeros ((n_ball+1 , n_wicket)) #for each state              ###why n_ball+1 bcz 0,1,....,n_ball ball left
policy = np.zeros (initial_V.shape , dtype = np.int)
final_V , policy= bellman (initial_V)

#---------------------------------------Saving-----------------------------------------------#
np.set_printoptions(formatter={'float': '{: 0.0f}'.format})
np.savetxt("policy.txt" , policy , fmt = "%i")
np.savetxt("value.txt" , final_V , fmt = "%i")


