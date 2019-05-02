#!/usr/bin/env python3

# Kaushal Kishore (bithack)
# 111601008
# Week 5
# Other Group Members: Pankaj Kumar (111601014) , Shiv Kumar Suthar (111601023)
# Question No. 1


import numpy as np 
from collections import deque
import heapq
import copy

class Environment:
    def __init__(self , _dim=(10,10) , _start=None , _end=None):
        self.dim = _dim
        self.grid = self.generate_random_grid(self.dim)
        
        # checking the type of the _start and _end variable
        if not (isinstance(_start, tuple) and list(map(type, _start)) == [int, int]) \
        or not ((isinstance(_end, tuple) and list(map(type, _end)) == [int, int])):
            self.agent_position = (0,0)
            self.goal_position = (self.dim[0]-1 , self.dim[1]-1)
        else:
            self.agent_position = _start
            self.goal_position = _end

        self.grid[self.agent_position] = 1
        self.grid[self.goal_position] = 1

        self.render()

    def generate_random_grid(self , _dim=(10,10)):
        return (np.random.normal(2.5,4 , _dim[0]*_dim[1]) > 0).astype(int).reshape(_dim[0] , _dim[1])
        # return np.random.randint(2 , size=_dim)

    # ⛳ or $: Goal State
    # █ or #: Blocked State
    # 🐍 or @: Agent Current Position 💃
    def render(self , grid=None , agent_pos=None, goal_pos=None):
        # printing the puzzle initially
        if grid is None:
            grid=self.grid[:]
        if agent_pos is None:
            agent_pos = self.agent_position
        if goal_pos is None:
            goal_pos = self.goal_position

        r , c = grid.shape[0] , grid.shape[1]

        for i in range(r):
            for j in range(c):
                coord = (i,j)
                try:
                    if coord == self.goal_position:
                        print('⛳' ,end="\t")
                    elif coord == self.agent_position:
                        print('💃' ,end="\t")
                    elif grid[coord] == 0:
                        print('█' ,end="\t")
                    else:
                        print("-" ,end="\t")
                except:
                    if coord == self.goal_position:
                        print('$' ,end="\t")
                    elif coord == self.agent_position:
                        print('@' ,end="\t")
                    elif grid[coord] == 0:
                        print('#' ,end="\t")
                    else:
                        print("-" ,end="\t")
            print("\n" , end="")

    def render_with_path(self , path , grid=None , agent_pos=None, goal_pos=None):
        if grid is None:
            grid=self.grid[:]
        if agent_pos is None:
            agent_pos = self.agent_position
        if goal_pos is None:
            goal_pos = self.goal_position

        r , c = grid.shape[0] , grid.shape[1]
        print("\nPath is shown with `*`.\n")
        for i in range(r):
            for j in range(c):
                coord = (i,j)
                try:
                    if coord == self.goal_position:
                        print('⛳' ,end="\t")
                    elif coord == self.agent_position:
                        print('💃' ,end="\t")
                    elif grid[coord] == 0:
                        print('█' ,end="\t")
                    elif coord in path:
                        print('*' ,end="\t")
                    else:
                        print("-" ,end="\t")
                except:
                    if coord == self.goal_position:
                        print('$' ,end="\t")
                    elif coord == self.agent_position:
                        print('@' ,end="\t")
                    elif grid[coord] == 0:
                        print('#' ,end="\t")
                    elif coord in path:
                        print('*' ,end="\t")
                    else:
                        print("-" ,end="\t")
            print("\n" , end="")



class Agent:
    '''
        env : Object of the Class Environment
        h   : heuristic function
    '''
    def g(self , r , c ):
        pass

    def __init__(self, env:Environment , h):
        self.env = copy.deepcopy(env)
        self.h = h

    def path_search(self):
        # unlike BFS where we used FIFO-queue, we will be using priority queue (min-heap)
        openStates = []

        # creating a set for the explored coordinates
        visited = set()     # visited set

        # creating a array for the g(n)
        g = np.ones_like(self.env.grid) * float("inf")
        g[self.env.agent_position] = 0

        # pushing the starting position into the heap
        heapq.heappush( openStates , tuple([ self.h(self.env.agent_position , self.env.goal_position) , self.env.agent_position ]) )

        # creating a cameFrom set : it'll be used for reconstructing the smallest path
        _r , _c = self.env.grid.shape
        cameFrom = -1*np.ones((2,_r,_c)).astype(np.int)

        goal_reached = False

        # to limit the search for `cycle` number of steps
        cycle = 100000

        while len(openStates) != 0 and goal_reached == False and cycle>0:
            # pop an element from the  min heap having lowest f-score
            current = heapq.heappop(openStates)[1]

            # if goal is reached
            if current ==  self.env.goal_position:
                goal_reached = True
                break

            # if the current coordinate is not explored
            if (current not in visited):
                # mark and explore the current coordinate
                visited.add(tuple(current))

                # since it is a grid problem, therefore, there are four adjacent nodes : L,R,U,D
                # LEFT

                # get the next coordinate on moving left
                nextpos = ( current[0] , current[1] - 1 )
                # if this coodinate is valid
                if (nextpos[1] >= 0) and self.env.grid[nextpos] != 0:
                    # if nextpos is not explored yet
                    if (nextpos not in visited):
                        # update the g(n) for the nextpos
                        g[nextpos] = g[current] + 1
                        # calculate the f-score by using heuristics 
                        f_nextpos = g[nextpos] + self.h(nextpos , self.env.goal_position)
                        # push this information into the min-heap
                        heapq.heappush(openStates , tuple([ f_nextpos , nextpos ]))
                        # add the information about the parent coodinate position in the cameFrom array
                        # cameFrom array will be used to reconstruct the path in the next step
                        cameFrom[: , nextpos[0] , nextpos[1]] = current
                    

                # RIGHT
                # the procedure is same as in above step
                nextpos = ( current[0] , current[1] + 1 )
                if (nextpos[1] < _c) and self.env.grid[nextpos] != 0:
                    if (nextpos not in visited):
                        g[nextpos] = g[current] + 1
                        f_nextpos = g[nextpos] + self.h(nextpos , self.env.goal_position)
                        heapq.heappush(openStates , tuple([ f_nextpos , nextpos ]))
                        cameFrom[: , nextpos[0] , nextpos[1]] = current

                # UP
                nextpos = ( current[0] - 1 , current[1] )
                if (nextpos[0] >= 0) and self.env.grid[nextpos] != 0:
                    if (nextpos not in visited):
                        g[nextpos] = g[current] + 1
                        f_nextpos = g[nextpos] + self.h(nextpos , self.env.goal_position)
                        heapq.heappush(openStates , tuple([ f_nextpos , nextpos ]))
                        cameFrom[: , nextpos[0] , nextpos[1]] = current

                # DOWN
                nextpos = ( current[0] + 1, current[1] )
                if (nextpos[0] < _r) and self.env.grid[nextpos] != 0:
                    if (nextpos not in visited):
                        g[nextpos] = g[current] + 1
                        f_nextpos = g[nextpos] + self.h(nextpos , self.env.goal_position)
                        heapq.heappush(openStates , tuple([ f_nextpos , nextpos ]))
                        cameFrom[: , nextpos[0] , nextpos[1]] = current

            cycle-=1
        # print the g-score
        print(g)
        if cycle > 0 and goal_reached==False:
            print("Goal Unreachable.")
        elif cycle == 0 and goal_reached==False:
            print("Goal Unreachable in cuurent cycle value. Try to increase the steps")
        elif goal_reached == True:
            # reconstructing the path using backtracing
            path = [self.env.goal_position]
            while True:
                _r , _c = path[-1]
                if (_r , _c) == (-1 , -1):
                    break
                path.append(tuple(cameFrom[: , _r , _c]))

            self.env.render_with_path(path)
            




def euclidean_distance(coord1 , coord2):
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def manhattan_distance(coord1 , coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def main():
    env = Environment((10,10))
    agent = Agent(env , euclidean_distance)
    agent.path_search()

if __name__ == "__main__":
    main()
