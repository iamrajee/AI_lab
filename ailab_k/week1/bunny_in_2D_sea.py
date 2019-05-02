#!/usr/bin/env python3

# Kaushal Kishore (bithack)
# 111601008
# Question No. 2b

# Bunny in the Ocean. Why again?
# Bunny, how did you reach to the middle of the Ocean?
# This is the last time I am saving you.

# The ocean in this case is a half plane described by a line.

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


class Line:
    '''
        equation of a line in the form: ax + by + c = 0

        Sign of a Point:
                        A line divides a 2D plane into two halves with opposite signs.
                        What I mean by the sign is the value of the following expression:
                            sign( a*x + b*y + c) , where (x,y) is the coordinates of a point.
                        Hence one side of the line contains the points having positive sign
                        and other side of the line contains the points having negative sign.
    '''

    def __init__(self , _a=1, _b=1 ,_c=1):
        self.a = _a
        self.b = _b
        self.c = _c
    
    def __str__(self):
        return "({0})*x + ({1})*y + ({2}) = 0".format(self.a, self.b , self.c)
    
    def __repr__(self):
        return "Line: ({0})*x + ({1})*y + ({2}) = 0".format(self.a, self.b , self.c)

    def getSignOfPoint(self , point):
        if isinstance(point, Point):
            return np.sign(self.a * point.x + self.b * point.y + self.c)
        else:
            return None

class Environment:
    '''
        agent_position:
                        This is the coordinate of the agent in a 2D cartesian plane.
        plane_line:
                    The equation of the line which divides the plane into two halves 
                    where one of the halves is the plane.
        plane_sign: 
                    Takes on either of two values +1 or -1. Since any line divides  a 
                    2D plane in two halves, containing the points with negative and 
                    positive sign of points. The value of the plane_sign is to denote 
                    which side of the line the shore lies.
    '''


    def __init__(self):
        p = abs(50)
        self.agent_position = Point(np.random.randint(-p,p) , np.random.randint(-p,p))
        self.plane_line = Line(np.random.randint(-p,p) , np.random.randint(-p,p), np.random.randint(-p,p))
        self.plane_sign = [-1,1][np.random.randint(0,2)]
        
        while self.feedback() == True:
            self.agent_position = Point(np.random.randint(-p,p) , np.random.randint(-p,p))
        
        print("Environment initialized with:")
        print("Agent position: ", self.agent_position)
        print("Equation of the line: ", self.plane_line)
        print("Sign of the Plane: ", self.plane_sign)

    def feedback(self):
        if self.plane_line.getSignOfPoint(self.agent_position) == self.plane_sign:
            # if agent and the shore is on the same side of the plane
            return True
        return False

    def interact(self,action):
        try:
            direction = fetch_direction(action[0])
            distance = action[1]

            if direction == 'x-axis':
                self.agent_position.x += distance
            else:
                self.agent_position.y += distance

        except:
            print("Interaction with environment failed.")
            print("Please bithack! don't make mistakes while wirting Python code.")
            sys.exit()

class Agent:
    '''
        The strategy is similar to the 1D ocean, where the bunny once moved to left with some distance
        and the right with three times the same distance. In this case since it's a 2D we will let the 
        bunny move in two directions in each step. 

        For this case let's choose two axis x and y as two direction.
    '''


    def __init__(self):
        self.next_direction = 0
        self.step_count = 0
        self.dist_x_y = np.array([1,1])
        self.next_action = [self.next_direction , self.dist_x_y[self.next_direction]]

    def action(self):
        agent_action = self.next_action[:]

        self.step_count += 1        
        self.next_direction = self.next_direction ^ 1

        if self.step_count == 2:
            self.dist_x_y = (-3)*np.array(self.dist_x_y)
            self.step_count = 0

        # print(self.next_direction , self.dist_x_y)
        self.next_action = [self.next_direction , self.dist_x_y[self.next_direction]]
        return agent_action


def fetch_direction(x):
    direction_dict = { 0:"x-axis" , 1:"y-axis"}
    if  0<= x <= 1:
        return direction_dict[x]
    return None


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
        
        print("Step: {0}: \nBunny moves {1} along {2}.\nBunny's current position: {3}\n"
                .format(step , action[1] , fetch_direction(action[0]) , ocean.agent_position))

        if ocean.feedback() == True:
            print("Mission Accomplished, Bunny has reached to the shore.")
            break

        step += 1

if __name__ == "__main__":
    main()