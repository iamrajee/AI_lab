#!/usr/bin/env python3

# Kaushal Kishore (bithack)
# 111601008
# Week 5
# Other Group Members: Pankaj Kumar (111601014) , Shiv Kumar Suthar (111601023)
# Question No. 1

# Coding the nsquare_minus_one_puzzle
import sys
from collections import deque
import numpy as np


# <S , A, R, T>
class Environment:
    def __init__(self , _n=4):
        if isinstance(_n , int):
            self.n = _n
            
            # self.grid = [1,0,3,2] ; self.n = 2
            self.grid = [0,1,3,4,2,5,7,8,6] ; self.n = 3
            # self.grid = [1,2,3,4,5,0,6,8,9,10,7,11,13,14,15,12] , self.n = 4
            
            self.goal_state = list(range(1 , self.n*self.n))
            self.goal_state.append(0)
            
            # generating a puzzle : value '0' denotes the empty position
            # while True:
            #     self.grid = np.arange(1 , self.n*self.n).astype(int)
            #     np.random.shuffle(self.grid)
            #     self.grid = self.grid.tolist() 
            #     self.grid.append(0)
            #     if self.parity() == 0:
            #         break
            
            # printing the puzzle
            self.render()

            print("Initial d(s): {0}".format(self.d()))
            print("Initial Parity: {0}".format(self.parity()))

    def render(self , grid=None):
        # printing the puzzle initially
        if grid is None:
            grid=self.grid[:]

        for i in range(0,self.n):
            for j in range(0,self.n):
                if grid[i*self.n + j] != 0:
                    print(grid[i*self.n + j] ,end="\t" )
                else:
                    print('█' ,end="\t")
            print("\n" , end="")


    def indicator(self , condition):
        if condition == True:
            return 1
        return 0

    def d(self):
        (r , c) = divmod(self.grid.index(0) , self.n)
        return (self.n - r - 1 ) + (self.n - c - 1)

    def parity(self):
        accumulate_sum = 0
        # pi and pj are position index where as pi_s and pj_s are the value at that index
        print(self.grid)
        for pi in range(0,self.n*self.n):
            if self.grid[pi] == 0:
                continue
            for pj in range(pi , self.n*self.n):
                if self.grid[pj] == 0:
                    continue
                # print("{0} , {1} , {2}, {3}".format(
                #     self.grid[pi] , 
                #     self.grid[pj] , 
                #     self.grid[pj] < self.grid[pi] , 
                #     self.indicator(self.grid[pj] < self.grid[pi]
                #     )))
                accumulate_sum += self.indicator(self.grid[pj] < self.grid[pi])

        # print("Accumulate Sum: {0}".format(accumulate_sum))

        return (self.d()  + accumulate_sum) % 2

    def interact(self , action, grid=None , ret_matrix=False):
        if grid == None:
            grid = self.grid[:]
        
        # four actions are available : {left : 0, right:1 , up:2 , down:3}
        
        # calculating the position of the blank space
        r_blank , c_blank = divmod(grid.index(0) , self.n)

        if action is "LEFT" or action is 0 and c_blank > 0:
            # moving the blank space LEFT --> results in moving the left element right
            print("taking action left")
            r_element , c_element = r_blank , c_blank-1

        elif action is "RIGHT" or action is 1 and c_blank < self.n-1:
            print("taking action right")
            r_element , c_element = r_blank , c_blank+1
            
        elif action is "UP" or action is 2 and r_blank > 0:
            print("taking action up")
            r_element , c_element = r_blank-1 , c_blank

        elif action is "DOWN" or action is 3 and r_blank < self.n-1:
            print("taking action down")
            r_element , c_element = r_blank+1 , c_blank
        
        else:
            print("Invalid Action")
            return None
        
        grid[r_blank*self.n + c_blank] = grid[r_element*self.n + c_element]
        grid[r_element*self.n + c_element] = 0
        
        if ret_matrix==True:            
            return grid[:]
        
        self.grid = grid[:]

        print("Environment After action:")
        self.render()


class PuzzleSolver:
    def __init__(self , _env):
        if not isinstance(_env , Environment):
            print("InstanceError: Argument is not of correct datatype.")
            sys.exit()
        self.env = _env

    def solve(self, max_depth = 10):
        print("BFS started")
        fifoQ = deque()     # first-in first out queue
        visited = set()     # visited list
        goal_reached = False
        fifoQ.append(self.env.grid[:])

        cycle = 100

        while len(fifoQ) != 0 and goal_reached == False and cycle>0:
            print("Queue Size: " , len(fifoQ))
            # retrieve the current grid
            current_state = fifoQ.popleft()
            print("\nCurrent State: Que Size {0}".format(len(fifoQ)))

            print("\n----------------Popped State Render-------------------------")
            self.env.render(current_state)

            if ( tuple(current_state) not in visited):
                visited.add(tuple(current_state))

                # exploring the next states:
                # same as exploring the adjacent nodes in a graph

                print("======Adding States to queue========")

                for action in range(4):
                    # {left : 0, right:1 , up:2 , down:3}
                    next_state_for_current_action = self.env.interact(action, current_state[:] , True)
                    
                    if next_state_for_current_action == None:
                        continue

                    self.env.render(next_state_for_current_action)
                    print("\n")

                    if next_state_for_current_action == self.env.goal_state:
                        # goal state reached
                        print("Goal State Reached.")
                        self.env.render(next_state_for_current_action)
                        goal_reached = True
                        break
                    
                    # if this state is not visited yet add to the queue
                    if tuple(next_state_for_current_action) not in visited:
                        fifoQ.append(next_state_for_current_action)
                        print("appending to queue")

                print("===========================================")
                # print(visited)
            cycle-=1


def main():
    env = Environment(3)
    env.render()
    bfsSolver = PuzzleSolver(env)
    bfsSolver.solve()

    # opt = True
    # while True:
    #     print("four actions are available : {left : 0, right:1 , up:2 , down:3}")
    #     action = int(input("Enter the action 0 to 3: "))
    #     env.interact(action)
    #     opt = int(input("Do u want to continue? (0/1)"))
    #     if opt == 0:
    #         break

if __name__ == "__main__":
    main()
