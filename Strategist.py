import sc2
import BaseManager
import random
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from BaseManager import BaseManager
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
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

    async def sendTask(self) :
        tf = self.time_formatted
        while self.buildOrder != [] and tf >= self.buildOrder[0][0]:
            order = self.buildOrder.pop(0)
            if order[1].type == 0:
                if order[1].location == None:
                    order[1].location = await self.find_placement(order[1].id,random.choice(self.structures).position, 50, True, 2, True)
            self.baseManager.receiveTask(order[1])

    async def setArmyStance(self) :
        """
            check intel and determine best army behaviour
        """

    async def on_start(self) :
        vgs1 = None

        for th in self.townhalls.ready:
            vgs1 = self.vespene_geyser.closer_than(20, th)

        rp = list(self.main_base_ramp.corner_depots)

        ex1 = await self.get_next_expansion()

        vgs2 = self.vespene_geyser.closer_than(20, ex1)

        ex2 = await self.get_next_expansion()

        vgs3 = self.vespene_geyser.closer_than(20, ex2)

        self.buildOrder = [
            ("00:17",Task(0, UnitTypeId.SUPPLYDEPOT, rp[1], None)),
            ("00:29",Task(0, UnitTypeId.REFINERY, vgs1[0], None)),
            ("00:44",Task(0, UnitTypeId.BARRACKS, self.main_base_ramp.barracks_in_middle, None)),
            ("01:32",Task(2, UnitTypeId.COMMANDCENTER, UnitTypeId.ORBITALCOMMAND, AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)),
            ("01:43",Task(0, UnitTypeId.COMMANDCENTER, ex1, None)),
            ("01:34",Task(1, UnitTypeId.REAPER, UnitTypeId.BARRACKS, None)),
            ("01:43",Task(0, UnitTypeId.COMMANDCENTER, None, None)),
            ("02:08",Task(0, UnitTypeId.FACTORY, None, None)),
            ("02:15",Task(0, UnitTypeId.SUPPLYDEPOT, None, None)),
            ("02:21",Task(0, UnitTypeId.REFINERY, vgs1[1], None)),
            ("02:51",Task(0, UnitTypeId.FACTORY, None, None)),
            ("02:52",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("02:52",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            # ("02:57",Task(4, UnitTypeId.BARRACKS, None, UnitTypeId.TECHLAB)),
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
            ("04:31",Task(0, UnitTypeId.COMMANDCENTER, ex2, None)),
            ("04:41",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("04:41",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
            ("04:48",Task(0, UnitTypeId.REFINERY, vgs2[0], None)),
            ("04:48",Task(0, UnitTypeId.REFINERY, vgs2[1], None)),
            ("04:57",Task(1, UnitTypeId.SIEGETANK, UnitTypeId.FACTORY, None)),
            # ("05:27",Task(4, UnitTypeId.BARRACKS, None, UnitTypeId.TECHLAB)),
            ("05:28",Task(0, UnitTypeId.FACTORY, None, None)),
            ("05:28",Task(0, UnitTypeId.FACTORY, None, None)),
            ("05:29",Task(1, UnitTypeId.SIEGETANK, UnitTypeId.FACTORY, None)),
            ("05:35",Task(0, UnitTypeId.FACTORY, None, None)),
            ("04:41",Task(1, UnitTypeId.HELLION, UnitTypeId.FACTORY, None)),
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
        await self.sendTask()
        # await self.setArmyStance()
        await self.baseManager.doAction()
        # await self.armyLeader.doAction()

    def __init__(self):
        self.unit_command_uses_self_do = True
        self.baseManager = BaseManager(self)
        # self.armyLeader = ArmyLeader(self)
