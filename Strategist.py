import sc2
import BaseManager
import random
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from BaseManager import BaseManager
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.units import Units
from Task import Task

class Strategist(sc2.BotAI) :
    baseManager = None
    armyLeader = None
    intel = None
    buildOrder = []

    async def changeBuild(self) :
        """
            check intel and determine changes for current buildOrder
        """

    def sendTask(self) :
        tf = self.time_formatted
        while self.buildOrder != [] and tf >= self.buildOrder[0][0]:
            order = self.buildOrder.pop(0)
            self.baseManager.receiveTask(order[1])

    async def setArmyStance(self) :
        """
            check intel and determine best army behaviour
        """

    async def on_start(self) :

        rp = list(self.main_base_ramp.corner_depots)

        self.buildOrder = [
            ("00:17",Task(0, UnitTypeId.SUPPLYDEPOT, rp[0], None)),
            ("00:29",Task(0, UnitTypeId.REFINERY, None, None)),
            ("00:44",Task(0, UnitTypeId.BARRACKS, self.main_base_ramp.barracks_in_middle, None)),
            ("01:32",Task(2, UnitTypeId.COMMANDCENTER, UnitTypeId.ORBITALCOMMAND, AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)),
            ("01:34",Task(1, UnitTypeId.REAPER, UnitTypeId.BARRACKS, None)),
            ("01:43",Task(0, UnitTypeId.COMMANDCENTER, None, None)),
            ("02:08",Task(0, UnitTypeId.FACTORY, None, None)),
            ("02:15",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("02:21",Task(0, UnitTypeId.REFINERY, None, None)),
            ("02:51",Task(0, UnitTypeId.FACTORY, None, None)),
            ("02:52",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("02:52",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("02:57",Task(2, UnitTypeId.BARRACKS, UnitTypeId.TECHLAB, AbilityId.BUILD_TECHLAB_BARRACKS)),
            ("03:01",Task(2, UnitTypeId.COMMANDCENTER, UnitTypeId.ORBITALCOMMAND, AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)),
            ("03:17",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("03:39",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("03:39",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("03:45",Task(1, UnitTypeId.SIEGETANK, UnitTypeId.FACTORY, None)),
            ("03:50",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:00",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:14",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:14",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:17",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("04:17",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("04:22",Task(1, UnitTypeId.SIEGETANK, UnitTypeId.FACTORY, None)),
            ("04:31",Task(0, UnitTypeId.COMMANDCENTER, None, None)),
            ("04:41",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("04:41",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("04:48",Task(0, UnitTypeId.REFINERY, None, None)),
            ("04:48",Task(0, UnitTypeId.REFINERY, None, None)),
            ("04:57",Task(1, UnitTypeId.SIEGETANK, UnitTypeId.FACTORY, None)),
            # ("05:27",Task(4, UnitTypeId.BARRACKS, None, UnitTypeId.TECHLAB)),
            ("05:28",Task(0, UnitTypeId.FACTORY, None, None)),
            ("05:28",Task(0, UnitTypeId.FACTORY, None, None)),
            ("05:29",Task(1, UnitTypeId.SIEGETANK, UnitTypeId.FACTORY, None)),
            ("05:35",Task(0, UnitTypeId.FACTORY, None, None)),
            ("05:45",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("05:48",Task(2, UnitTypeId.COMMANDCENTER, UnitTypeId.ORBITALCOMMAND, AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)),
            # ("05:58",Task(4, UnitTypeId.BARRACKS, None, UnitTypeId.TECHLAB)),
            ("06:05",Task(1, UnitTypeId.SIEGETANK, UnitTypeId.FACTORY, None)),
            ("06:11",Task(0, UnitTypeId.ENGINEERINGBAY, None, None)),
            # ("06:21",Task(4, UnitTypeId.FACTORY, None, UnitTypeId.REACTOR)),
            ("06:24",Task(1, UnitTypeId.SIEGETANK, UnitTypeId.FACTORY, None)),
            ("06:41",Task(0, UnitTypeId.MISSILETURRET, None, None)),
            ("06:41",Task(0, UnitTypeId.MISSILETURRET, None, None)),
            ("06:41",Task(0, UnitTypeId.MISSILETURRET, None, None)),
            ("06:48",Task(0, UnitTypeId.MISSILETURRET, None, None)),
            ("06:48",Task(0, UnitTypeId.MISSILETURRET, None, None)),
            ("06:48",Task(0, UnitTypeId.MISSILETURRET, None, None)),
            ("07:00",Task(0, UnitTypeId.ARMORY, None, None))
        ]

    async def on_step(self, iteration) :
        # await self.changeBuild()
        self.sendTask()
        # await self.setArmyStance()
        await self.baseManager.doAction()
        # await self.armyLeader.doAction()

    def __init__(self):
        self.unit_command_uses_self_do = True
        self.baseManager = BaseManager(self)
        # self.armyLeader = ArmyLeader(self)

    async def distribute_workers(self, performanceHeavy=True, onlySaturateGas=False):
        mineralTags = [x.tag for x in self.mineral_field]
        gas_buildingTags = [x.tag for x in self.gas_buildings]

        workerPool = Units([], self)
        workerPoolTags = set()

        # Find all gas_buildings that have surplus or deficit
        deficit_gas_buildings = {}
        surplusgas_buildings = {}
        for g in self.gas_buildings.filter(lambda x: x.vespene_contents > 0):
            # Only loop over gas_buildings that have still gas in them
            deficit = g.ideal_harvesters - g.assigned_harvesters
            if deficit > 0:
                deficit_gas_buildings[g.tag] = {"unit": g, "deficit": deficit}
            elif deficit < 0:
                surplusWorkers = self.workers.closer_than(10, g).filter(
                    lambda w: w not in workerPoolTags
                    and len(w.orders) == 1
                    and w.orders[0].ability.id in [AbilityId.HARVEST_GATHER]
                    and w.orders[0].target in gas_buildingTags
                )
                for i in range(-deficit):
                    if surplusWorkers.amount > 0:
                        w = surplusWorkers.pop()
                        workerPool.append(w)
                        workerPoolTags.add(w.tag)
                surplusgas_buildings[g.tag] = {"unit": g, "deficit": deficit}

        # Find all townhalls that have surplus or deficit
        deficitTownhalls = {}
        surplusTownhalls = {}
        if not onlySaturateGas:
            for th in self.townhalls:
                deficit = th.ideal_harvesters - th.assigned_harvesters
                if deficit > 0:
                    deficitTownhalls[th.tag] = {"unit": th, "deficit": deficit}
                elif deficit < 0:
                    surplusWorkers = self.workers.closer_than(10, th).filter(
                        lambda w: w.tag not in workerPoolTags
                        and len(w.orders) == 1
                        and w.orders[0].ability.id in [AbilityId.HARVEST_GATHER]
                        and w.orders[0].target in mineralTags
                    )
                    # workerPool.extend(surplusWorkers)
                    for i in range(-deficit):
                        if surplusWorkers.amount > 0:
                            w = surplusWorkers.pop()
                            workerPool.append(w)
                            workerPoolTags.add(w.tag)
                    surplusTownhalls[th.tag] = {"unit": th, "deficit": deficit}

            if all(
                [
                    len(deficit_gas_buildings) == 0,
                    len(surplusgas_buildings) == 0,
                    len(surplusTownhalls) == 0 or deficitTownhalls == 0,
                ]
            ):
                # Cancel early if there is nothing to balance
                return

        # Check if deficit in gas less or equal than what we have in surplus, else grab some more workers from surplus bases
        deficitGasCount = sum(
            gasInfo["deficit"] for gasTag, gasInfo in deficit_gas_buildings.items() if gasInfo["deficit"] > 0
        )
        surplusCount = sum(
            -gasInfo["deficit"] for gasTag, gasInfo in surplusgas_buildings.items() if gasInfo["deficit"] < 0
        )
        surplusCount += sum(-thInfo["deficit"] for thTag, thInfo in surplusTownhalls.items() if thInfo["deficit"] < 0)

        if deficitGasCount - surplusCount > 0:
            # Grab workers near the gas who are mining minerals
            for gTag, gInfo in deficit_gas_buildings.items():
                if workerPool.amount >= deficitGasCount:
                    break
                workersNearGas = self.workers.closer_than(10, gInfo["unit"]).filter(
                    lambda w: w.tag not in workerPoolTags
                    and len(w.orders) == 1
                    and w.orders[0].ability.id in [AbilityId.HARVEST_GATHER]
                    and w.orders[0].target in mineralTags
                )
                while workersNearGas.amount > 0 and workerPool.amount < deficitGasCount:
                    w = workersNearGas.pop()
                    workerPool.append(w)
                    workerPoolTags.add(w.tag)

        # Now we should have enough workers in the pool to saturate all gases, and if there are workers left over, make them mine at townhalls that have mineral workers deficit
        for gTag, gInfo in deficit_gas_buildings.items():
            if performanceHeavy:
                # Sort furthest away to closest (as the pop() function will take the last element)
                workerPool.sort(key=lambda x: x.distance_to(gInfo["unit"]), reverse=True)
            for i in range(gInfo["deficit"]):
                if workerPool.amount > 0:
                    w = workerPool.pop()
                    if len(w.orders) == 1 and w.orders[0].ability.id in [AbilityId.HARVEST_RETURN]:
                        self.do(w.gather(gInfo["unit"], queue=True))
                    else:
                        self.do(w.gather(gInfo["unit"]))

        if not onlySaturateGas:
            # If we now have left over workers, make them mine at bases with deficit in mineral workers
            for thTag, thInfo in deficitTownhalls.items():
                if performanceHeavy:
                    # Sort furthest away to closest (as the pop() function will take the last element)
                    workerPool.sort(key=lambda x: x.distance_to(thInfo["unit"]), reverse=True)
                for i in range(thInfo["deficit"]):
                    if workerPool.amount > 0:
                        w = workerPool.pop()
                        mf = self.mineral_field.closer_than(10, thInfo["unit"]).closest_to(w)
                        if len(w.orders) == 1 and w.orders[0].ability.id in [AbilityId.HARVEST_RETURN]:
                            self.do(w.gather(mf, queue=True))
                        else:
                            self.do(w.gather(mf))
