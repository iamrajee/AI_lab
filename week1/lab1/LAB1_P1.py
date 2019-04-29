#-------Program1--------------------------------------

class shore:
    loc=10
    
    """Class to define the shore."""
    def __init__(self,agent_loc):
        #locaton of the shore
        self.agent_loc=agent_loc
    
           
    def percept(self,steps,direction):
        """ Input: agent location
            Output: Shore reached or not"""
        if steps!=0:
            print(self.agent_loc,"\t\t", steps, "\t",direction)  
            
        #update agent location
        if(direction=="r"):
            self.agent_loc=self.agent_loc+steps
        else:
            self.agent_loc=self.agent_loc-steps
            
        #Give percept        
        if self.agent_loc==self.loc:
            return 1
        else:
            return 0
    
class agent:
    """Class that defines agent"""
    #number of steps taken by the agent
    steps=0
    
    def move_left(self):
            """Perform action moves left"""
            
            #increment steps
            self.steps = self.steps+1
            
            #recieve percept
            percept= s.percept(self.steps,"l")
            
            if(percept): #shore reached
                print("Shore reached")
            else: #shore not reached
                self.move_right()
                
    def move_right(self):
            """Perform action move right"""
        
            #update steps
            self.steps = self.steps+1
                      
            #recieve percept
            percept= s.percept(self.steps,"r")
            
            if(percept): #shore reached
                print("Shore reached")
            else: #shore not reached
                self.move_left()
    
    
        
        
        
print("Agent Location   Steps  Direction ")
agent_loc=0 # agent location
steps=0 #initialize steps

s=shore(agent_loc) #shore identifies agent location

percept=s.percept(steps,"l") #agent recieves percept from shore

if percept:
    print("Shore reached")
else: #if shore not reached agent moves left
    
    a=agent()
    a.move_left()
    

        
        

