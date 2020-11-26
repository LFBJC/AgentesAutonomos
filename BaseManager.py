import sc2
import Agent
import math
from sc2.constants import COMMANDCENTER, SCV
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from Agent import Agent

class BaseManager(Agent):
    def buildHandler(self, task):
        chosen = self.env.select_build_worker(task.location)
        if chosen:
            result = self.env.do(chosen.build(task.id, task.location))
            if result:
                return True
        return False

    def trainHandler(self,task):
        for structure in self.env.structures(task.location).ready.idle:
            if self.env.can_afford(task.id):
                result = self.env.do(structure.train(task.id))
                if result:
                    return True
        return False

    def upgradeHandler(self, task):
        for st in self.env.structures(task.id).ready.idle:
            if self.env.can_afford(task.upgrade) and self.env.tech_requirement_progress(task.location) == 1:
                result = self.env.do(st(task.upgrade))
                if result:
                    return True
        return False

    def researchHandler(self, task):
        for structure in self.env.structures(task.id).ready:
            if self.env.can_afford(task.upgrade):
                result = self.env.do(structure.research(task.upgrade))
                if result:
                    return True
        return False

    def handleTasks(self):
        for i in range(len(self.tasks)):
            result = self.handler[self.tasks[i].type](self, self.tasks[i])
            if (result):
                self.tasks.pop(i)
                break

    async def doAction(self):
        self.distributeWorkers()
        self.buildWorkers()
        self.handleTasks()

    def buildWorkers(self):
        for commandCenter in self.env.townhalls.idle:
            if self.env.can_afford(SCV) and self.env.supply_left > 10:
                self.env.do(commandCenter.train(SCV))

    def distributeWorkers(self):
        for scv in self.env.workers.idle:
            self.env.do(scv.gather(self.env.mineral_field.closest_to(scv)))

    handler = [buildHandler, trainHandler, upgradeHandler, researchHandler]
