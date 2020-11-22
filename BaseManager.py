import sc2
import Agent
from sc2.constants import COMMANDCENTER, SCV
from sc2.ids.unit_typeid import UnitTypeId
from Agent import Agent

class BaseManager(Agent):
    async def doAction(self):
        await self.env.distribute_workers()
        await self.buildWorkers()
        await self.buildDeppot()
        await self.buildExpansion()

    async def buildWorkers(self):
        for commandCenter in self.env.units(COMMANDCENTER).ready.idle:
            if self.env.can_afford(SCV):
                await self.env.do(commandCenter.train(SCV))

    async def buildDeppot(self):
        if self.env.supply_left < 5 and self.env.can_afford(UnitTypeId.SUPPLYDEPOT):
            if self.env.units(UnitTypeId.SUPPLYDEPOT).not_ready.amount + self.env.already_pending(UnitTypeId.SUPPLYDEPOT) < 1:
                workers = self.env.workers.gathering
                if workers != None:
                    worker = workers.furthest_to(workers.center)
                    placement = await self.env.find_placement(UnitTypeId.SUPPLYDEPOT, worker.position, placement_step=3)
                    if placement != None:
                        await self.env.do(worker.build(UnitTypeId.SUPPLYDEPOT, placement))

    async def buildExpansion(self):
        if self.env.can_afford(UnitTypeId.COMMANDCENTER) and self.env.units(UnitTypeId.COMMANDCENTER).amount < 4:
            await self.env.expand_now()
