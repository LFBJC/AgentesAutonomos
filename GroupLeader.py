import sc2
import Agent
import collections
import random
from sc2.constants import COMMANDCENTER, SCV
from sc2.ids.unit_typeid import UnitTypeId
from Agent import Agent

class GroupLeader(Agent):
    async def focusAttack(self, chosen):
        for unit in self.unitList:
            self.env.do(unit.attack(chosen))

    async def moveUnits(self, chosen):
        for unit in self.unitList:
            if unit.distance_to(chosen) < 5 or unit.is_moving:
                continue
            self.env.do(unit.move(chosen))

    async def defensiveMarine(self):
        center = self.marshall.position
        closer = None
        if self.env.enemy_units.amount > 0:
            closer = self.env.enemy_units.closest_to(center)
            if True:
                await self.focusAttack(closer)
        elif self.env.enemy_structures.amount > 0:
            closer = self.env.enemy_structures.closest_to(center)
            await self.focusAttack(closer)
        else:
            closer = random.choice(self.env.structures).position
            await self.moveUnits(closer)

    async def agressiveMarine(self):
        center = self.marshall.position
        closer = None
        if self.env.enemy_units.amount > 0:
            closer = self.env.enemy_units.closest_to(center)
            if True:
                await self.focusAttack(closer)
        elif self.env.enemy_structures.amount > 0:
            closer = self.env.enemy_structures.closest_to(center)
            await self.focusAttack(closer)
        else:
            closer = self.env.enemy_start_locations[0]
            await self.moveUnits(closer)

    async def defensiveCruiser(self):
        center = self.marshall.position
        closer = None
        if self.env.enemy_units.amount > 0:
            closer = self.env.enemy_units.closest_to(center)
            if True:
                await self.focusAttack(closer)
        elif self.env.enemy_structures.amount > 0:
            closer = self.env.enemy_structures.closest_to(center)
            await self.focusAttack(closer)
        else:
            closer = random.choice(self.env.structures).position
            await self.moveUnits(closer)

    async def agressiveCruiser(self):
        center = self.marshall.position
        closer = None
        if self.env.enemy_units.amount > 0:
            closer = self.env.enemy_units.closest_to(center)
            if True:
                await self.focusAttack(closer)
        elif self.env.enemy_structures.amount > 0:
            closer = self.env.enemy_structures.closest_to(center)
            await self.focusAttack(closer)
        else:
            closer = self.env.enemy_start_locations[0]
            await self.moveUnits(closer)

    async def usualMedivac(self):
        for group in self.armyLeader.groups:
            if group.type_id == UnitTypeId.MARINE and group.marshall != None:
                if group.marshall.distance_to(self.unitList.center) > 8:
                    self.moveUnits(group.marshall.position)
                    break

    async def doAction(self):
        if self.unitList.amount > 0:
            self.latePos = self.marshall.position
            await self.behaviours[self.stance][self.unitID](self)

    behaviours = [
        {
            UnitTypeId.MARINE : defensiveMarine,
            UnitTypeId.BATTLECRUISER : defensiveCruiser,
            UnitTypeId.MEDIVAC : usualMedivac,
        },
        {
            UnitTypeId.MARINE : agressiveMarine,
            UnitTypeId.BATTLECRUISER : agressiveCruiser,
            UnitTypeId.MEDIVAC : usualMedivac,
        }
    ]

    armyLeader = None
    marshall = None
    latePos = None
    stance = None
    unitID = None
    unitList = None
    maxSize = None
