import sc2
import BaseManager
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

    def sendTask(self) :
        if self.buildOrder != []:
            if self.time >= self.buildOrder[0][0]:
                order = self.buildOrder.pop(0)
                self.baseManager.receiveTask(order[1])

    async def setArmyStance(self) :
        """
            check intel and determine best army behaviour
        """

    async def on_start(self) :
        # TODO: checks for building placement
        vgs = None

        for th in self.townhalls.ready:
            vgs = self.vespene_geyser.closer_than(20, th)

        rp = list(self.main_base_ramp.corner_depots)

        self.buildOrder = [
            (17,Task(0, UnitTypeId.SUPPLYDEPOT, rp[1], None)),
            (29,Task(0, UnitTypeId.REFINERY, vgs[0], None)),
            (46,Task(0, UnitTypeId.BARRACKS, self.main_base_ramp.barracks_in_middle, None)),
            (92,Task(2, UnitTypeId.COMMANDCENTER, UnitTypeId.ORBITALCOMMAND, AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)),
            (94,Task(1, UnitTypeId.REAPER, UnitTypeId.BARRACKS, None)),
            # (103,Task(,,)),
            # (114,Task(,,)),
            # (128,Task(,,))
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
