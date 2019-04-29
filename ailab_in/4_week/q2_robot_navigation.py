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
    def __init__(self,x_initial, y_initial, x_final, y_final, Mat, N) :
        self.State = State(x_initial, y_initial)     #start point
        self.G = State(x_final, y_final)   #end point
        self.Mat = Mat                                #matix of env
        self.N = N                                  #size of matrix    
    #------------------function for finding next state---------------------------------------#      
    def nextState(self, move) :
        x = self.State.x                    #x variable
        y = self.Mat.State.y                  #y variable
        if(move == 'l') :
            if(y <= 1 or self.Mat[x][y-1] == 0):
                return    #on invalid move

            self.Mat[x][y]   = self.M[x][y-1]
            self.Mat[x][y-1] = self.M[x][y]
            self.State = State(x, y-1)    #update state
        elif(move == 'r') :
            if(y >= self.n or self.Mat[x][y+1] == 0):
                return  #on invalid move
            self.Mat[x][y]   = self.M[x][y+1]
            self.Mat[x][y+1] = self.M[x][y]
            self.State = State(x, y+1)    #update state 
        elif(move == 'u') :
            if(x <= 1 or self.Mat[x-1][y] == 0):
                return     #on invalid move
                
            self.Mat[x][y]   = self.M[x-1][y]
            self.Mat[x-1][y] = self.M[x][y]
            self.State = State(x-1, y)    #update state
        elif(move == 'd') :
            if(x >= self.n or self.Mat[x+1][y] == 0):
                return   #on invalid move

            self.Mat[x][y]   = self.M[x+1][y]
            self.Mat[x+1][y] = self.M[x][y]
            self.State = State(x+1, y)    #update state
        else:
             return  
    #----------------------------function for checking if goal state reached or not---------------------#
    def check_goal(self) :        #check if goal reached
        return self.State.equal(self.G)


#----------------------------------Class for agent------------------------------------------------------#        
class Agent :
    #------------------function for finding next state---------------------------------------#  
    def nextState(self, temp_env, move):
        temp_env.nextState(move) 
    #----------------------------function for checking if goal state reached or not---------------------#     
    def check_goal(self, temp_env):
        return temp_env.check_goal()
    
        