import sc2
import Agent
import math
from sc2.constants import COMMANDCENTER, SCV
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from Agent import Agent

class BaseManager(Agent):
    async def buildHandler(self, task):
        chosen = self.env.select_build_worker(task.location)
        if chosen:
            result = None
            try:
                result = await self.env.do(chosen.build(task.id, task.location))
            except:
                return False
            if result != sc2.data.ActionResult.Error:
                return True
            return False
        return False

    async def trainHandler(self,task):
        for structure in self.env.units(task.location).ready.idle:
            if self.env.can_afford(task.id):
                try:
                    return await self.env.do(structure.train(task.id))
                except:
                    return False
                return True
        return False

    async def upgradeHandler(self, task): # TODO: fix method exception
        for structure in self.env.units(task.id).ready:
            if self.env.can_afford(task.upgrade):
                try:
                    return self.env.do(structure.research(task.upgrade))
                except:
                    return False
                return True
        return False

    async def handleTasks(self):
        for i in range(len(self.tasks)):
            result = await self.handler[self.tasks[i].type](self, self.tasks[i])
            if (result):
                self.tasks.pop(i)

    async def doAction(self):
        await self.env.distribute_workers()
        await self.buildWorkers()
        await self.handleTasks()

    async def buildWorkers(self):
        for commandCenter in self.env.units(COMMANDCENTER).ready.idle:
            if self.env.can_afford(SCV):
                await self.env.do(commandCenter.train(SCV))

    handler = [buildHandler, trainHandler, upgradeHandler]
