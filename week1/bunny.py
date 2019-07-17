class Agent:
    def __init__(self):
        self.alive = True
        self.performance = 0
    def move(self, Environment):
        pass
    def percept(self,Environment):
        pass

class Environment:
    def __init__(self):
        self.agent = 0
        
    def percept(self, agent):
        raise NotImplementedError

    def execute_action(self, agent, action):
        raise NotImplementedError

    def default_location(self,thing):
        return None

    def is_done(self):
        return agent.is_alive()

    def step(self):
        pass