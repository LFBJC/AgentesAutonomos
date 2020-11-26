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
        if chosen and self.env.can_afford(task.id) and self.env.already_pending(task.id) == 0:
            result = self.env.do(chosen.build(task.id, task.location))
            if result:
                return True
        return False

    def expansionHandler(self, task):
        for structure in self.env.structures(task.id).ready.idle:
            if self.env.can_afford(task.upgrade):
                if structure.is_active:
                    self.env.do(structure.stop())
                result = self.env.do(structure.build(task.upgrade))
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

    def abilityHandler(self, task):
        for st in self.env.structures(task.id).ready.idle:
            if st.is_active:
                self.env.do(st.stop())
            if self.env.can_afford(task.upgrade) and self.env.tech_requirement_progress(task.location) == 1:
                result = self.env.do(st(task.upgrade))
                if result:
                    return True
        return False

    def researchHandler(self, task):
        for structure in self.env.structures(task.id).ready.idle:
            if self.env.can_afford(task.upgrade):
                if structure.is_active:
                    self.env.do(structure.stop())
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
        self.handleTasks()
        self.buildWorkers()
        self.distributeWorkers()

    def buildWorkers(self):
        for commandCenter in self.env.townhalls.idle:
            if self.env.can_afford(SCV) and self.env.supply_left > 0 and self.env.supply_workers < self.maxWorkers:
                self.env.do(commandCenter.train(SCV))

    def distributeWorkers(self):
        for scv in self.env.workers.idle:
            self.env.do(scv.gather(self.env.mineral_field.closest_to(scv)))

    maxWorkers = 36
    handler = [buildHandler, trainHandler, abilityHandler, researchHandler, expansionHandler]
