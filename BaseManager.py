import sc2
import Agent
import math
import random
from sc2.constants import COMMANDCENTER, SCV
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from Agent import Agent

class BaseManager(Agent):
    async def buildHandler(self, task):
        if self.env.can_afford(task.id) and self.env.already_pending(task.id) == 0:
            if task.location == None:
                task.location = await self.env.find_placement(task.id,random.choice(self.env.structures).position, 100, True, 3, True)
            if task.location:
                chosen = self.env.workers.closest_to(task.location)
                if chosen:
                    result = self.env.do(chosen.build(task.id, task.location))
                    if result:
                        return True
        return False

    async def expansionHandler(self, task):
        for structure in self.env.structures(task.id).ready.idle:
            if not structure.has_add_on and self.env.can_afford(task.upgrade):
                if structure.is_active:
                    self.env.do(structure.stop())
                result = self.env.do(structure.build(task.upgrade))
                if result:
                    return True
        return False

    async def trainHandler(self,task):
        for structure in self.env.structures(task.location).ready.idle:
            if self.env.can_afford(task.id):
                result = self.env.do(structure.train(task.id))
                if result:
                    return True
        return False

    async def abilityHandler(self, task):
        for st in self.env.structures(task.id).ready.idle:
            if st.is_active:
                self.env.do(st.stop())
            if self.env.can_afford(task.upgrade) and self.env.tech_requirement_progress(task.location) == 1:
                result = self.env.do(st(task.upgrade))
                if result:
                    return True
        return False

    async def researchHandler(self, task):
        for structure in self.env.structures(task.id).ready.idle:
            if self.env.can_afford(task.upgrade):
                if structure.is_active:
                    self.env.do(structure.stop())
                result = self.env.do(structure.research(task.upgrade))
                if result:
                    return True
        return False

    async def handleTasks(self):
        for i in range(len(self.tasks)):
            result = await self.handler[self.tasks[i].type](self, self.tasks[i])
            if (result):
                self.tasks.pop(i)
                break

    async def doAction(self):
        await self.handleTasks()
        self.buildWorkers()
        self.distributeIdleWorkers()
        await self.env.distribute_workers()

    def buildWorkers(self):
        for commandCenter in self.env.townhalls.idle:
            if self.env.can_afford(SCV) and self.env.supply_left > 0 and self.env.supply_workers < self.maxWorkers:
                self.env.do(commandCenter.train(SCV))

    def distributeIdleWorkers(self):
        for scv in self.env.workers.idle:
            self.env.do(scv.gather(self.env.mineral_field.closest_to(scv)))

    maxWorkers = 40
    focusGas = True
    handler = [buildHandler, trainHandler, abilityHandler, researchHandler, expansionHandler]
