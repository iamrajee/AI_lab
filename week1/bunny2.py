class shore:
    loc = 10
    def __init__(self, agent_loc):
        self.agent_loc=agent_loc

    def percept(self, steps, direction):
        if steps!=0:
            print(self.agent_loc, "\t\t", steps, "\t", direction)

        # update agent_loc
        if(direction == "r"):
            self.agent_loc=self.agent_loc+steps
        else:
            self.agent_loc=self.agent_loc-steps    
        
        # land or water
        if self.agent_loc==self.loc:
            return 1
        else:
            return 0

class agent:
    steps = 0

    def move_left(self):

        #increase step
        self.steps +=1

        percept = s.percept(self.steps, "l")

        if(percept):
            print("Shore reached")
        else:
            self.move_right()

    def move_right(self):

        #increase step
        self.steps +=1

        percept = s.percept(self.steps, "r")

        if(percept):
            print("Shore reached")
        else:
            self.move_left()

    

print("Agent_loc  Steps  Direction")

agent_loc = 0
steps = 0

s=shore(agent_loc)

percept=s.percept(steps, "l")

if percept:
    print("Shore reached")
else:
    a = agent()
    a.move_left()