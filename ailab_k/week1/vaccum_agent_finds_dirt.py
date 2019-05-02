#!/usr/bin/env python3

# Kaushal Kishore (bithack)
# 111601008
# Question No. 3

# Vaccum Robot: "Hey! bithack... I wanna find the dirt. Please help."
# Bithack: "Are you dumb? You are standing on it."
# Vaccum Robot: "Bithack you are awesome. Dirt Found. Cleaned."
# Vaccum Robot: "Hey! bithack... I wanna find the dirt. Please help."
# Bithack: "Again? Let's give you a brain."

import sys
import numpy as np

class Point():
    def __init__(self , _x=0, _y=0):
        self.x = _x
        self.y = _y

    def __str__(self):
        return "({0} , {1})".format(self.x, self.y)
    
    def __repr__(self):
        return "Point: ({0} , {1})".format(self.x, self.y)
    
    def __eq__(self, other):
        '''Overriding the default equality comparison.'''
        if isinstance(other , Point):
            return (self.x == other.x) and (self.y == other.y)
        return False

    def Set(self,other):
        if isinstance(other , Point):
            self.x = other.x
            self.y = other.y
            return True
        return False

class Agent:
    '''
        next_action: 
                    It is a list of two integers in the format (direction, distance).
                    Where direction can take values from 0,1,2,and 3 represting the directions
                    right,up,left,down respectively. Distance is an integer.
                    This list can roughly be considered as the policy for the agent 
                    in the current scenario.
        distance_count:
                    The logic is to move the agent in a spiral orientation to cover the complete 2D 
                    eventually. To achieve we need to move with same distance value two times in a 
                    row. This variable keeps track of a particular distance value used count.
    '''

    def __init__(self):
        self.next_action = [0 , 1]
        self.distance_count = 0
    
    def action(self):
        # deep copy the current value
        agent_action = self.next_action[:]
        # update the direction
        # direction is chosen in a cyclic order : 0 , 1, 2, 3, 0, 1, 2, 3, ....
        self.next_action[0] = (self.next_action[0] + 1) % 4
        # update the distance
        # distance is updated in the following sequnce to form a spiral to cover the 2D plane
        # 1 , 1, 2, 2, 3, 3, 4, 4, 5, 5, .....
        self.distance_count += 1

        if self.distance_count == 2:
            # if a certain distance is used twice then increment it 
            self.distance_count = 0
            self.next_action[1] += 1
        
        return agent_action

class Environment:
    '''
        dirt_position: 
                        This is the coordinate of the dirt in a 2D cartesian plane.
        agent_position:
                        This is the coordinate of the agent in a 2D cartesian plane.
    '''

    def __init__(self):
        p = abs(100)
        self.dirt_position = Point(np.random.randint(-p,p) , np.random.randint(-p,p))
        self.agent_position = Point(np.random.randint(-p,p) , np.random.randint(-p,p))
        # self.dirt_position = Point(2,7)
        # self.agent_position = Point(-10,-2)
        print("Environment initialized with:")
        print("Dirt position: " , self.dirt_position)
        print("Agent position: ", self.agent_position)


    def feedback(self):
        return self.agent_position == self.dirt_position
    
    def interact(self, action):
        # caching the agent position for safety
        agent_pos_temp = Point()
        agent_pos_temp.Set(self.agent_position)
        direction = fetch_direction(action[0])
        distance = action[1]
        
        try:
            if (self.agent_position.x == self.dirt_position.x):
                # x-coordinates match
                if direction == 'UP' and \
                self.agent_position.y <= self.dirt_position.y <= self.agent_position.y + distance:
                    self.agent_position.Set(self.dirt_position)
                    return None
                
                elif direction == 'DOWN' and \
                self.agent_position.y - distance <= self.dirt_position.y <= self.agent_position.y:
                    self.agent_position.Set(self.dirt_position)
                    return None

            elif (self.agent_position.y == self.dirt_position.y):
                # y-coordinates match            
                if direction == 'RIGHT' and \
                self.agent_position.x <= self.dirt_position.x <= self.agent_position.x + distance:
                    self.agent_position.Set(self.dirt_position)
                    return None

                elif direction=="LEFT" and \
                self.agent_position.x - distance <= self.dirt_position.x <= self.agent_position.x:
                    self.agent_position.Set(self.dirt_position)
                    return None

            if direction == "LEFT":
                self.agent_position.x -= distance
            elif direction == "RIGHT":
                self.agent_position.x += distance
            elif direction == "UP":
                self.agent_position.y += distance
            else:
                self.agent_position.y -= distance

        except:
            # reverting back to the previous data
            self.agent_position.Set(agent_pos_temp)
            print("Interaction with environment failed.")
            print("Please bithack! don't make mistakes while wirting Python code.")
            sys.exit()


def fetch_direction(x):
    direction_dict = { 0:"RIGHT" , 1:"UP" ,2:"LEFT" ,  3:"DOWN" }
    return direction_dict[x]


def main():
    agent = Agent()
    env = Environment()
    step = 1

    # let's test the brain of the vaccum agent
    while True:
        # action taken by the agent
        action = agent.action()

        # interact with environment with the actions we received from the agent
        env.interact(action)
        
        print("Step: {0}: \nAgent moves {1} units to {2}.\nAgent's current position: {3}\n"
                .format(step , action[1] , fetch_direction(action[0]) , env.agent_position))

        if env.feedback() == True:
            print("Mission Accomplished, Agent has found the dirt.")
            break

        step += 1

if __name__ == "__main__":
    main()