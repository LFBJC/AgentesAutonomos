import sc2
import Agent
import math
import random
from sc2.constants import COMMANDCENTER, SCV
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from Agent import Agent
from Task import Task

class BaseManager(Agent):
    async def buildHandler(self, task):
        if self.env.can_afford(task.id) and self.env.tech_requirement_progress(task.id) == 1:
            if task.id == UnitTypeId.REFINERY:
                for th in self.env.townhalls.ready:
                    vespenes = self.env.vespene_geyser.closer_than(10, th)
                    myvp = await self.getVespeneLocation(vespenes)
                    if myvp != None:
                        task.location = myvp
                        break
                if task.location == None:
                    return False

            if task.id == UnitTypeId.COMMANDCENTER:
                task.location = await self.env.get_next_expansion()

            if task.location and (await self.env.can_place(task.id, [task.location.position]))[0]:
                chosen = self.env.workers.closest_to(task.location)
                if chosen:
                    if chosen.is_gathering:
                        result = self.env.do(chosen.build(task.id, task.location))
                    else:
                        result = self.env.do(chosen.build(task.id, task.location, True))
                    if result:
                        return True
            else:
                task.location = await self.env.find_placement(task.id,random.choice(self.env.structures).position, 80, True, 4, True)
                return False
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
            if self.env.can_afford(task.id) and self.env.tech_requirement_progress(task.id) == 1 and self.env.calculate_supply_cost(task.id) <= self.env.supply_left:
                result = self.env.do(structure.train(task.id))
                if (structure.has_reactor):
                    result = self.env.do(structure.train(task.id))
                if result:
                    return True
        return False

    async def abilityHandler(self, task):
        for st in self.env.structures(task.id).ready:
            if task.id in [UnitTypeId.BARRACKS, UnitTypeId.STARPORT, UnitTypeId.ARMORY] and st.has_add_on:
                continue
            if st.is_active:
                self.env.do(st.stop())
                return False
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

    def depotRaise(self):
        for depot in self.env.structures(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            if self.env.enemy_units == []:
                continue
            if depot.distance_to(self.env.enemy_units.closest_to(depot)) <= 15:
                self.env.do(depot(AbilityId.MORPH_SUPPLYDEPOT_RAISE))

    def depotLower(self):
        for depot in self.env.structures(UnitTypeId.SUPPLYDEPOT).ready:
            if self.env.enemy_units == [] or depot.distance_to(self.env.enemy_units.closest_to(depot)) > 15:
                self.env.do(depot(AbilityId.MORPH_SUPPLYDEPOT_LOWER))

    async def getVespeneLocation(self, vespenes):
        for vp in vespenes:
            if (await self.env.can_place(UnitTypeId.REFINERY, [vp.position]))[0]:
                return vp
        return None

    async def doAction(self):
        self.postBuildOrder()
        await self.handleTasks()
        self.buildWorkers()
        self.distributeIdleWorkers()
        self.depotLower()
        # self.depotRaise()
        await self.env.distribute_workers()

    def receiveTask(self,task):
        if task.type != 2:
            self.tasks.append(task)
        else:
            self.tasks.insert(0, task)

    def buildWorkers(self):
        for commandCenter in self.env.townhalls.idle:
            if self.env.can_afford(SCV) and self.env.supply_left > 0 and self.env.supply_workers < self.maxWorkers:
                self.env.do(commandCenter.train(SCV))

    def distributeIdleWorkers(self):
        for scv in self.env.workers.idle:
            self.env.do(scv.gather(self.env.mineral_field.closest_to(scv)))

    def notProducing(self, id):
        for task in self.tasks:
            if id == task.id:
                return False
        return True

    def postBuildOrder(self):
        if self.env.time_formatted > self.buildTimeEnd:
            for tg in self.targetList:
                if self.env.units(tg[0]).amount < tg[2] and self.notProducing(tg[0]):
                    self.receiveTask(Task(1,tg[0],tg[1],None))
            if self.env.supply_left <= 16 and self.env.supply_cap != 200 and self.env.already_pending(UnitTypeId.SUPPLYDEPOT) == 0:
                self.receiveTask(Task(0,UnitTypeId.SUPPLYDEPOT,None,None))

    maxWorkers = 50
    focusGas = True

    targetList = [
        (UnitTypeId.MARINE,UnitTypeId.BARRACKS,50),
        (UnitTypeId.BATTLECRUISER,UnitTypeId.STARPORT,20),
        # (UnitTypeId.MEDIVAC,UnitTypeId.STARPORT,4),
    ]

    buildTimeEnd = "06:20"
    handler = [buildHandler, trainHandler, abilityHandler, researchHandler, expansionHandler]
