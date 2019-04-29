#5 arm
#average of each

import numpy as np
import math
import itertools
import random

no_arm = 5
no_round = 100
ucb_arm = np.full (no_arm,1)
lcb_arm = np.full (no_arm,0)
# avg_arm = np.full (no_arm,1/2)
no_selection = np.full ((no_round,no_arm),0)
sum_reward = np.full ((no_round,no_arm),0)
print(ucb_arm)
def selectsrm():
    i_wrt_maxucb = 0
    for i in range(no_arm):
        if ucb_arm[i]>ucb_arm[i_wrt_maxucb]:
            i_wrt_maxucb = i
    return i_wrt_maxucb

def give_reward(temp_i):
	if random.randint(0,1) < avg_arm[temp_i]:
		return 1


for n in range(no_round):
	a_wrt_max_confi = 0
	min_confi = -1
	for a in range(no_arm):
		avg_reward = sum_reward[a]/no_selection[a]
		delta_interval = math.sqrt((3*math.log(n)/(2*no_selection[a])))
		confi_level = (avg_reward-delta_interval,avg_reward+delta_interval)
		if confi_level>min_confi:
			min_confi = confi_level
			a_wrt_max_confi = a
	
	# a = selectsrm()
	# r = give_reward(a)
	# if a == 1:
	# 	lcb_arm[a]+=1/no_round
	# 	avg_arm[a] =(lcb_arm[a]+ucb_arm[a])/2
	# else:
	# 	ucb_arm[a]-=1/no_round
	# 	avg_arm[a] =(lcb_arm[a]+ucb_arm[a])/2

print(lcb_arm)
print(avg_arm)
print(ucb_arm)


