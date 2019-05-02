#!/usr/bin/env python3

# Kaushal Kishore (bithack)
# 111601008
# Week 3
# Other Group Members: Saptdeep Das (111601020) , Pankaj Kumar (111601014)
# Question No. 1

# Usage : curse_of_dimensionality.py  d L
# where d and L are the areguments to the program representing dimension and length

# This program is a generalized to cover all the cases of (d,L).
# Hence all the three environments(1D , 2D, 3D) can be simulated by passing the argument value accodingly.

import sys 
import numpy as np
from time import time

class Environment:
    '''
        This is generalized program for creating the environment with same principle.

        _d : dimension of the environment
        _L : is the length of a particular axis

        agent_position : List containing the current position of the agent.
        actions : stores all possible actions that the agent can take
        total_actions : total number of possible actions
    '''
    def __init__(self , _d , _L ):
        self.d = int(_d)
        self.L = int(_L)

        # initializing the agents position
        self.agent_position = (int(np.ceil(self.L/2))* np.ones(self.d).astype(np.int))
        
        # initializing the actions array
        # for a 1D case, actions array will be initialized with values: 
        # [ [1]  , [-1]] representing the direction of the motion forward and backward by 1 unit
        # for a 2D case, actions array will be initialized with values: 
        # [[1,0] , [0,1] , [-1,0] , [0,-1]] representing the direction of the motions 
        # right, up, left, and down by 1 unit
        # and similarly for higher dimensional cases
        self.actions = np.vstack((np.eye(self.d) , -np.eye(self.d))).astype(int)
    
        # caching the value of total actions in a separate variable
        self.total_actions = int(2*self.d)
        
        print("Environment Initialized With: ")
        print("Dimension : {0}".format(self.d))
        print("L : {0}".format(self.L))
        print("Total Actions : {0}".format(self.total_actions))
        print("Agent Position : {0}".format(self.agent_position))
        print("Actions: \n{0}".format(self.actions))
    
    def get_total_actions_count(self):
        return self.total_actions

    def get_actions(self):
        return self.actions

    def interact(self , action_idx):        
        # get the desired action using the action index from the stored action array
        # Here current action also represent the displacement of the agent for the current step.
        current_action = self.actions[action_idx]

        # caching the agents current position
        agent_current_position = self.agent_position

        # add the displacement to the current position of the agent
        self.agent_position = current_action + self.agent_position

        # if some of the coordinates is greater than L
        if np.where(self.agent_position > self.L)[0].shape[0] != 0 or \
        np.where(self.agent_position < 0)[0].shape[0] != 0:
            self.agent_position = agent_current_position

    # returns true if agent position is in the goal state
    def feedback(self):
        if np.sum(self.agent_position) == self.d * self.L:
            return True
        return False
    

# This week program has a very simple agent which doesn't do any complex calculations.
# The agent in each step choose an action randomly from the available set of the actions.
class Agent:
    def __init__(self , total_actions):
        # agent get to know the total number of available actions
        self.n = total_actions

    def choose_action(self):
        # from the available number of actions agent choose a random action
        return np.random.randint(self.n)


def main(argv):
    try:
        # if any system argument is provided then initialize d and L with those values
        d = int(argv[1])
        L = int(argv[2])
    except:
        # else take default values
        d = 1
        L = 10
    
    env = Environment(d , L)
    agent = Agent(env.get_total_actions_count())

    cycle = 0

    t0 = time()
    while env.feedback() == False:
        print("\n-----------------------------------\nCycle : {0}".format(cycle))
        action_idx = agent.choose_action()
        print("Agent's Current Position: {0}".format(env.agent_position))
        print("Agent's Current Action: {0}".format(env.actions[action_idx]))
        env.interact(action_idx)
        print("Agent's New Position: {0}".format(env.agent_position))
        cycle += 1
    
    t1 = time()
    print("\nET : {0} ms".format((t1-t0)*1000))


if __name__ == "__main__":
    main(sys.argv)