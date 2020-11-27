import sc2
import Agent
import collections
from sc2.constants import COMMANDCENTER, SCV
from sc2.ids.unit_typeid import UnitTypeId
from Agent import Agent

class GroupLeader(Agent):
    async def defensiveReaper(self):
        """

        """

    async def defensiveHelion(self):
        """

        """

    async def defensiveTank(self):
        """

        """

    async def agressiveReaper(self):
        """

        """

    async def agressiveHelion(self):
        """

        """

    async def agressiveTank(self):
        """

        """

    async def doAction(self):
        await self.behaviours[self.stance][self.unitID](self)

    behaviours = [
        {
            UnitTypeId.REAPER : defensiveReaper,
            UnitTypeId.HELLION : defensiveHelion,
            UnitTypeId.SIEGETANK : defensiveTank
        },
        {
            UnitTypeId.REAPER : agressiveReaper,
            UnitTypeId.HELLION : agressiveHelion ,
            UnitTypeId.SIEGETANK : agressiveTank
        }
    ]
    stance = None
    unitID = None
    unitList = None
    maxSize = None
