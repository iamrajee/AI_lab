#========================================Name==============================================#
#@Rajendra Singh
# ======================================-:Concept:==========================================
'''
We will take discrete posi and velo. Now state depend on posi and velo.
We then run Value iteration. At each time step we have follow possible action;
[left, neutral, right]
Until agent reach 0.6 reward is -1, from then 0.
'''


#=====================================Imports================================================#
import numpy as np
import matplotlib.pyplot as plt




#========================================Initial Variable====================================#
grid_size = (100, 100)
velo = (-0.07, 0.07)
posi = (-1.2, 0.6)
actions = [-1, 0, 1]
posi_step = (posi[1] - posi[0])/(grid_size[0] - 1)
velo_step = (velo[1] - velo[0])/(grid_size[1] - 1)



#===============Takes current posi, current Velo and claculates new velo and then using new velo calculates new Position.===========
def function_update(oldPos, oldVel, action):
    newVel = oldVel + (action * 0.001) + np.cos(3*oldPos)*(-0.0025)
    newVel = min(max(newVel, velo[0]), velo[1])
    
    newPos = oldPos + newVel
    newPos = min(max(newPos, posi[0]), posi[1])
    
    if(newPos<= posi[0]):
        newVel = 0
    
    return newPos, newVel

def infinity_norm(currValue, optimalValue):
    maxDiff = 0
    for i in range(env.rowNum):
        for j in range(env.colNum):
            maxDiff = max(maxDiff, abs(currValue[i, j] - optimalValue[i, j]))
    return maxDiff



  
#==================if agent reaches the goal=> return True==============================
def goal_achieved(pos):
    if pos < 0.6:
        return False
    return True



#==================input= pos, vel and output = corr. index===============
def getIndex(pos, vel):
    posInd = (pos - posi[0])/posi_step
    velInd = (vel - velo[0])/velo_step
    
    posInd = np.ceil(posInd)
    velInd = np.ceil(velInd)
    
    return int(posInd), int(velInd) 




#==========Input = posi, velo, Output = corr. values=========================
#... in continuous world.
def get_state(posInd, velInd):   #row, col
    pos = posi[0] + posInd*posi_step
    vel = velo[0] + velInd*velo_step
    
    return pos, vel




#==================================Value Iteration===================================
minNum = -1000000
gamma = 1
def Value_Iter(value, policy):
    print("Value Iteration in progress")
    for iter1 in range(500):
        if(iter1%50 == 0): print("Iteration: ", iter1)
        for posInd in range(grid_size[0]):
            for velInd in range(grid_size[1]):
                optimalVal = minNum
                optimalAction = -1
                for action in actions:
                    currVal = 0
                    pos, vel = get_state(posInd, velInd)
                    newPos, newVel = function_update(pos, vel, action)
                    newPosInd, newVelInd = getIndex(newPos, newVel)
    
                    if(goal_achieved(newPos)):
                        currVal += 0 + gamma*value[newPosInd, newVelInd]
                    else:
                        currVal += -1 + gamma*value[newPosInd, newVelInd]

                    if(currVal > optimalVal):
                        optimalVal = currVal
                        optimalAction = action

                value[posInd, velInd] = optimalVal
                policy[posInd, velInd] = optimalAction
    print("Value Itertion Finished")




# ========================Calling Value iteration============================================#
value = np.zeros(grid_size)
policy = np.zeros(grid_size)
Value_Iter(value, policy)




#===============================Heatmap=======================================================
plt.imshow(value, cmap = "hot" , interpolation="nearest")
plt.show()


np.savetxt("value.txt", value, fmt = "%i")
np.savetxt("policy.txt", policy, fmt = "%i")