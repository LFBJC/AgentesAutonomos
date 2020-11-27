import sc2
import Agent
from sc2.constants import COMMANDCENTER, SCV
from sc2.ids.unit_typeid import UnitTypeId
from sc2.units import Units
from Agent import Agent
from GroupLeader import GroupLeader

class ArmyLeader(Agent):
    async def handleMessages(self):
        """
            deal with agent communication
        """

    async def doAction(self):
        await self.handleMessages()
        for group in self.groups:
            await group.doAction()

    def initGroups(self, models):
        for model in models:
            group = GroupLeader(self.env)
            group.unitID = model[0]
            group.maxSize = model[1]
            group.unitList = Units([],self.env)
            group.stance = 0
            self.groups.append(group)

    messageQueue = []
    groups = []
