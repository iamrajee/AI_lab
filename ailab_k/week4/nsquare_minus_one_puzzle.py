#!/usr/bin/env python3


# Kaushal Kishore (bithack)
# 111601008
# Week 4
# Other Group Members: Pankaj Kumar (111601014)
# Question No. 1

# Coding the nsquare_minus_one_puzzle
import sys
import numpy as np

# <S , A, R, T>
class Environment:
    def __init__(self , _n=4):
        if isinstance(_n , int):
            self.n = _n
            
            # self.grid = [5 , 6, 8, 9, 7, 12, 10, 11, 13, 14, 2, 3, 1, 4, 0, 15]

            # generating a puzzle : value '0' denotes the empty position
            
            self.grid = np.arange(1 , self.n*self.n).astype(int)
            np.random.shuffle(self.grid)
            self.grid = self.grid.tolist() 
            self.grid.append(0)

            
            # printing the puzzle
            self.render()

            print("Initial d(s): {0}".format(self.d()))
            print("Initial Parity: {0}".format(self.parity()))

    def render(self):
        # printing the puzzle initially
        for i in range(0,self.n):
            for j in range(0,self.n):
                if self.grid[i*self.n + j] != 0:
                    print(self.grid[i*self.n + j] ,end="\t" )
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

    def interact(self , action):
        # four actions are available : {left : 0, right:1 , up:2 , down:3}
        
        # calculating the position of the blank space
        r_blank , c_blank = divmod(self.grid.index(0) , self.n)

        if action is "LEFT" or action is 0 and c_blank > 0:
            # moving the blank space LEFT --> results in moving the left element right
            r_element , c_element = r_blank , c_blank-1

        elif action is "RIGHT" or action is 1 and c_blank < self.n-1:
            r_element , c_element = r_blank , c_blank+1
            
        elif action is "UP" or action is 2 and r_blank > 0:
            r_element , c_element = r_blank-1 , c_blank

        elif action is "DOWN" or action is 3 and r_blank < self.n-1:
            r_element , c_element = r_blank+1 , c_blank
        
        else:
            print("Invalid Action")
        
        self.grid[r_blank*self.n + c_blank] = self.grid[r_element*self.n + c_element]
        self.grid[r_element*self.n + c_element] = 0

        print("Environment After action:")
        self.render()


env = Environment()
opt = True
while True:
    print("four actions are available : {left : 0, right:1 , up:2 , down:3}")
    action = int(input("Enter the action 0 to 3: "))
    env.interact(action)
    opt = int(input("Do u want to continue? (0/1)"))
    if opt == 0:
        break
