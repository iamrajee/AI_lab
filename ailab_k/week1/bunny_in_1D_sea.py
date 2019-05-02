#!/usr/bin/env python3

# Kaushal Kishore (bithack)
# 111601008
# Question No. 2a

# Bunny in the Ocean.
# Bunny is the Agent.
# How did Bunny reached to the middle of the Ocean? Only he knows.
# We won't let bunny die.
# Let's save the bunny.

# The logic is straightforward.
# Initial Step: Bunny moves 1 unit distance to left.
# Further Step: Bunny reverses the direction and 
#       moves three times the distance it travelled in the previous step.
# Suppose the bunny is on the origin in the beginning then it moves to the 1 unit left.
# Now, bunny is at coordinate -1, if shore is not reached reverse the direction and move 
#   three times the distance travelled in previous step here 3 unit. Hence the bunny is at 
#   coordinate +2.  

import sys
import numpy as np

class Agent:
    '''
        next_action:
                    It is a list of two integers in the format (direction, distance).
                    Where direction can take two values 0 and 1 for Left and Right,
                    and distance can take a positive value.
                    This list can roughly be considered as the policy for the agent 
                    in the current scenario.
    '''

    def __init__(self):
        self.next_action = [0,1]

    def action(self):
        # deep copy the current value
        agent_action = self.next_action[:]
        # update the direction
        self.next_action[0] = self.next_action[0]^1
        # update the distance
        self.next_action[1] = self.next_action[1]*3
        return agent_action


class Environment:
    '''
        shore_position:
                        An integer denoting the 1-D coodinates of the shore position.
        agent_position:
                        An integer denoting the 1-D coordinates of the agent(bunny).
        shore_direction:
                        An integer denoting which side of the shore_position the land is present.
                        '0' means left and '1' means right
        
    '''
    def __init__(self):
        max_position = 100
        self.shore_position = np.random.randint(max_position)
        self.agent_position = np.random.randint(max_position)
        self.shore_direction = np.random.randint(0,2)

        while self.feedback():
            self.agent_position = np.random.randint(max_position)
        
        print("Environment Initialized with:")
        if self.shore_direction == 0:
            print("Shore is LEFT to coordinate : {0}".format(self.shore_position))
        else:
            print("Shore is RIGHT to coordinate : {0}".format(self.shore_position))

        print("Agent position:{0}\n".format(self.agent_position))

    def feedback(self):
        # if the shore_direction is left to the shore_position
        if self.shore_direction == 0 and (self.agent_position <= self.shore_position):
            self.agent_position = self.shore_position
            return True

        # if the shore_direction is right to the shore_position
        elif self.shore_direction == 1 and (self.agent_position >= self.shore_position):
            self.agent_position = self.shore_position
            return True

        return False

    def interact(self, action):
        # caching the agent's current position
        agent_pos_temp = self.agent_position
        try:
            if (len(action)!=2):
                print("Action argument must be a list of two integers.")
                return
            
            if action[0] == 0:
                # agent moving left
                self.agent_position -= action[1]
            else:
                # agent moving right
                self.agent_position += action[1]
        except:
            # reverting back to the previous data
            self.agent_position = agent_pos_temp
            print("Interaction with environment failed.")
            print("Check the code or Bunny will die in the middle of the ocean.")
            sys.exit()


def fetch_direction(x):
    if x==0:
        return 'LEFT'
    elif x==1:
        return 'RIGHT'

def main():
    ocean = Environment()
    bunny = Agent()
    step = 1
    
    # the bunny's survival quest begins
    while True:
        # action taken by the bunny
        action = bunny.action()

        # interact with environment with the actions we received from the agent
        ocean.interact(action)
        
        print("Step: {0}: \nBunny moves {1} units to {2}.\nBunny's current position: {3}\n"
                .format(step , action[1] , fetch_direction(action[0]) , ocean.agent_position))

        if ocean.feedback() == True:
            print("Mission Accomplished, Bunny has reached to the shore.")
            break

        step += 1

if __name__ == "__main__":
    main()

