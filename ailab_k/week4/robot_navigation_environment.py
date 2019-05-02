# coding: utf-8
import numpy as np


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
        return (np.random.normal(2.5,2 , _dim[0]*_dim[1]) > 0).astype(int).reshape(_dim[0] , _dim[1])
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


def main():
    env = Environment()

if __name__ == "__main__":
    main()