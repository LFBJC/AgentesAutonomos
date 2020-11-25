import sc2

class Agent :
    env = None
    tasks = []

    def __init__(self, env):
        self.env = env

    async def doAction(self):
        """

        """

    def receiveTask(self,task):
        self.tasks.append(task)
