#--------------------------------Team-------------------------------#
#RAJENDRA SINGH(111601017)
#SUENDRA BASKEY(111601027)
#SACHIN HANSDA (111601019)

#---------------------------------Class for state--------------------------------------#
class State :
    def __init__(self, x, y) :
        self.x = x
        self.y = y


#---------------------------------Class for envirnoment--------------------------------------#
class Envir : 
    def __init__(self,x_initial, y_initial, x_final, y_final, grid, N) :
        self.start = State(x_initial, y_initial)     #start point
        self.G = State(x_final, y_final)   #end point
        self.grid = grid                                #matix of env
        self.N = N                                  #size of matrix    
    #------------------function for finding next state---------------------------------------#      
    def nextState(self, move) :
        x = self.State.x                    #x variable
        y = self.State.y                  #y variable
        if(move == 'l') :
            if(y <= 1 or self.grid[x][y-1] == 0):
                return    #on invalid move

            self.grid[x][y]   = self.M[x][y-1]
            self.grid[x][y-1] = self.M[x][y]
            self.State = State(x, y-1)    #update state
        elif(move == 'r') :
            if(y >= self.n or self.grid[x][y+1] == 0):
                return  #on invalid move
            self.grid[x][y]   = self.M[x][y+1]
            self.grid[x][y+1] = self.M[x][y]
            self.State = State(x, y+1)    #update state 
        elif(move == 'u') :
            if(x <= 1 or self.grid[x-1][y] == 0):
                return     #on invalid move
                
            self.grid[x][y]   = self.M[x-1][y]
            self.grid[x-1][y] = self.M[x][y]
            self.State = State(x-1, y)    #update state
        elif(move == 'd') :
            if(x >= self.n or self.grid[x+1][y] == 0):
                return   #on invalid move

            self.grid[x][y]   = self.M[x+1][y]
            self.grid[x+1][y] = self.M[x][y]
            self.State = State(x+1, y)    #update state
        else:
             return  
    #----------------------------function for checking if goal state reached or not---------------------#
    def check_goal(self) :        #check if goal reached
        return self.State.equal(self.G)


#--------------------------------Class for agent------------------------------------------------------#        
class Agent :
    #----------------------------function for finding next state---------------------------------------#  
    def nextState(self, temp_env, move):
        temp_env.nextState(move) 
    #----------------------------function for checking if goal state reached or not---------------------#     
    def check_goal(self, temp_env):
        return temp_env.check_goal()


N = 100
xi,yi = 2,5
xf,yf = 8,7
r, c = N,N
grid = [[0 for x in range(c)] for y in range(r)]

h = [[0 for x in range(c)] for y in range(r)]
for i in range(N):
    for j in range(N):
        h[i][j] = abs(xf-i)  + abs(yf-j)

print(h)

for w in range(40,N-10):
   grid[w][w] = 1

for w in range(20,N-40):
    grid[70][w] = 1
    grid[23][w] = 1

# for ele in grid:
#     print(ele)

env1 = Envir(xi, yi, xf, yf, grid, N)
agent1 = Agent()

# def aStart(env):
    




    
        