import numpy as np
import gym
import matplotlib.pyplot as plt
from time import *

#========================== env ===========================#
env = gym.make('MountainCar-v0')
env.reset()

#========================== discretise state space ===========================#
def discret(temp):
    tempd = (temp- env.observation_space.low)*np.array([10, 100])
    tempd = np.round(tempd, 0).astype(int)
    return tempd

#========================== value iteration ===========================#
def Viteration(env, lr, gamma, ep, mnep, e):
    #=====ns=======#        !!! .n wont work
    ns = (env.observation_space.high - env.observation_space.low) * np.array([10, 100])#10 horzontal and 100 verticle
    ns = np.round(ns, 0).astype(int) + 1
    
    #=====qtable=======#
    Q = np.random.uniform(low = -1, high = 1, size = (ns[0], ns[1], env.action_space.n))
    
    #=====rsum, rlist, avgrlist=======#
    rlist = []
    avgrlist = []
    
    epd = (ep-mnep)/e# Calculate episodic epd in ep
    #========== for e episodes ============#
    for i in range(e):
        done = False
        rsum,R = 0,0
        s = env.reset() #return (x,y)
        sd = discret(s)# Discretize
        #========== while not done ============#
        while done != True:
            if i >= (e - 5):# Render environment for last five e
                env.render()
                sleep(0.005)
            #====== explore vs exploit =====#
            if np.random.random() < 1 - ep:#epsilon greedy exr vs expt
                a = np.argmax(Q[sd[0], sd[1]])
            else:
                a = np.random.randint(0, env.action_space.n)
            s_, R, done, info = env.step(a)
            s_d = discret(s_)# Discretize
            #====== update q =====#
            if done and s_[0] >= 0.5:#Allow for terminal states
                Q[sd[0], sd[1], a] = R
            else:# Adjust Q value for current s
                Q[sd[0], sd[1],a] =(1-lr)*Q[sd[0],sd[1],a]  +   lr*(R + gamma*np.max(Q[s_d[0], s_d[1]]))
            #====== variable update =====#
            rsum += R# Update variables
            sd = s_d
        #====== epsilion decay =====#
        if ep > mnep:# Decay ep
            ep -= epd
        rlist.append(rsum)# Track rewards
        
        #====== avg reward per 100 episodes =====#
        if (i+1) % 100 == 0:
            avgr = np.mean(rlist)
            avgrlist.append(avgr)
            rlist = []
            print('Episode {} Average Reward: {}'.format(i+1, avgr))
            
    env.close()
    return avgrlist

#========================================== calling ==================================#
lr=0.1
gamma=0.9
ep=0.8
e=50
mnep = 0
avgrlist = Viteration(env, lr, gamma, ep, mnep, e)

#========================================== plot and save ==================================#
plt.plot(100*(np.arange(len(avgrlist)) + 1), avgrlist)
plt.xlabel('Episodes')
plt.ylabel('Average Reward')
plt.title('Average Reward vs Episodes')
plt.savefig('rewards/'+'epi_'+str(e)+'_lr_'+str()+'_gamma_'+str(gamma)+'.jpg')
plt.show()
plt.close()