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
from sc2.unit import Unit
from Task import Task
from ArmyLeader import ArmyLeader
from GroupLeader import GroupLeader

class Strategist(sc2.BotAI) :
    baseManager = None
    armyLeader = None
    intel = None
    mainBasePosition = None
    buildOrder = []
    unitGroups = [UnitTypeId.MARINE,UnitTypeId.BATTLECRUISER,UnitTypeId.MEDIVAC]

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
        # print(self.supply_army)
        if (self.supply_used > 100):
            for group in self.armyLeader.groups:
                group.stance = 1
        # if (self.supply_army < 130):
        #     for group in self.armyLeader.groups:
        #         group.stance = 0
        # elif (self.supply_army >= 130):
        #     for group in self.armyLeader.groups:
        #         group.stance = 1

    async def on_start(self) :

        rp = list(self.main_base_ramp.corner_depots)

        self.mainBasePosition = self.townhalls[0].position

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
            ("02:51",Task(0, UnitTypeId.STARPORT, None, None)),
            ("02:53",Task(2, UnitTypeId.STARPORT, UnitTypeId.TECHLAB, AbilityId.BUILD_TECHLAB_STARPORT)),
            ("02:57",Task(2, UnitTypeId.BARRACKS, UnitTypeId.REACTOR, AbilityId.BUILD_REACTOR_BARRACKS)),
            ("03:01",Task(2, UnitTypeId.COMMANDCENTER, UnitTypeId.ORBITALCOMMAND, AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)),
            ("03:17",Task(1, UnitTypeId.MARINE, UnitTypeId.BARRACKS, None)),
            ("03:18",Task(1, UnitTypeId.MARINE, UnitTypeId.BARRACKS, None)),
            ("03:19",Task(1, UnitTypeId.MARINE, UnitTypeId.BARRACKS, None)),
            ("03:20",Task(1, UnitTypeId.MARINE, UnitTypeId.BARRACKS, None)),
            ("03:21",Task(1, UnitTypeId.MARINE, UnitTypeId.BARRACKS, None)),
            ("03:22",Task(1, UnitTypeId.MARINE, UnitTypeId.BARRACKS, None)),
            ("03:25",Task(0, UnitTypeId.FUSIONCORE, None, None)),
            ("03:50",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:00",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:14",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:14",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:14",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:14",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:14",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:14",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("04:31",Task(0, UnitTypeId.COMMANDCENTER, None, None)),
            ("04:48",Task(0, UnitTypeId.REFINERY, None, None)),
            ("04:50",Task(0, UnitTypeId.REFINERY, None, None)),
            ("05:28",Task(0, UnitTypeId.STARPORT, None, None)),
            ("05:30",Task(2, UnitTypeId.STARPORT, UnitTypeId.TECHLAB, AbilityId.BUILD_TECHLAB_STARPORT)),
            ("05:35",Task(0, UnitTypeId.FUSIONCORE, None, None)),
            ("05:41",Task(1, UnitTypeId.BATTLECRUISER, UnitTypeId.STARPORT, None)),
            ("05:42",Task(1, UnitTypeId.BATTLECRUISER, UnitTypeId.STARPORT, None)),
            ("05:42",Task(1, UnitTypeId.BATTLECRUISER, UnitTypeId.STARPORT, None)),
            ("05:42",Task(1, UnitTypeId.BATTLECRUISER, UnitTypeId.STARPORT, None)),
            ("05:42",Task(1, UnitTypeId.BATTLECRUISER, UnitTypeId.STARPORT, None)),
            ("05:42",Task(1, UnitTypeId.BATTLECRUISER, UnitTypeId.STARPORT, None)),
            ("05:42",Task(1, UnitTypeId.BATTLECRUISER, UnitTypeId.STARPORT, None)),
            ("05:42",Task(1, UnitTypeId.BATTLECRUISER, UnitTypeId.STARPORT, None)),
            ("05:42",Task(1, UnitTypeId.BATTLECRUISER, UnitTypeId.STARPORT, None)),
            ("05:42",Task(1, UnitTypeId.BATTLECRUISER, UnitTypeId.STARPORT, None)),
            ("05:48",Task(2, UnitTypeId.COMMANDCENTER, UnitTypeId.ORBITALCOMMAND, AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)),
            ("07:00",Task(0, UnitTypeId.ARMORY, None, None))

        ]

    def deleteFromGroup(self, unit_tag : int):
        for group in self.armyLeader.groups:
            unit = group.unitList.find_by_tag(unit_tag)
            if unit != None:
                removed = group.unitList.pop(group.unitList.index(unit))
                if (group.marshall == removed):
                    if group.unitList.amount > 0:
                        group.marshall = group.unitList.closest_to(group.latePos)
                    else:
                        group.marshall = None
                break

    async def on_unit_destroyed(self, unit_tag: int):
        self.deleteFromGroup(unit_tag)

    async def on_unit_created(self, unit: Unit):
        if unit.type_id in self.unitGroups:
            for group in self.armyLeader.groups:
                if unit.type_id == group.unitID and group.unitList.amount < group.maxSize:
                    if group.unitList.amount == 0:
                        group.marshall = unit
                    group.unitList.append(unit)
                    break

    async def on_unit_took_damage(self, unit: Unit, amount_damage_taken: float):
        """
        Override this in your bot class. This function is called when your own unit (unit or structure) took damage.
        It will not be called if the unit died this frame.
        This may be called frequently for terran structures that are burning down, or zerg buildings that are off creep,
        or terran bio units that just used stimpack ability.
        TODO: If there is a demand for it, then I can add a similar event for when enemy units took damage
        Examples::
            print(f"My unit took damage: {unit} took {amount_damage_taken} damage")
        :param unit:
        """

    async def on_enemy_unit_entered_vision(self, unit: Unit):
        """
        Override this in your bot class. This function is called when an enemy unit (unit or structure) entered vision (which was not visible last frame).
        :param unit:
        """

    async def on_enemy_unit_left_vision(self, unit_tag: int):
        """
        Override this in your bot class. This function is called when an enemy unit (unit or structure) left vision (which was visible last frame).
        Same as the self.on_unit_destroyed event, this function is called with the unit's tag because the unit is no longer visible anymore.
        If you want to store a snapshot of the unit, use self._enemy_units_previous_map[unit_tag] for units or self._enemy_structures_previous_map[unit_tag] for structures.
        Examples::
            last_known_unit = self._enemy_units_previous_map.get(unit_tag, None) or self._enemy_structures_previous_map[unit_tag]
            print(f"Enemy unit left vision, last known location: {last_known_unit.position}")
        :param unit_tag:
        """

    async def on_step(self, iteration) :
        # await self.changeBuild()
        self.sendTask()
        await self.setArmyStance()
        await self.baseManager.doAction()
        await self.armyLeader.doAction()

    def __init__(self):
        self.unit_command_uses_self_do = True
        self.baseManager = BaseManager(self)
        self.armyLeader = ArmyLeader(self)
        self.armyLeader.initGroups([
            (UnitTypeId.MARINE, 50),
            (UnitTypeId.BATTLECRUISER, 15),
            (UnitTypeId.MEDIVAC, 8),
            # (UnitTypeId.SIEGETANK, 4),
            # (UnitTypeId.REAPER, 1)
        ])

    # function from https://github.com/BurnySc2/python-sc2/blob/develop/examples/terran/mass_reaper.py
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
