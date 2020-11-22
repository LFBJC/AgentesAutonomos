import sc2
import BaseManager
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from BaseManager import BaseManager

class Strategist(sc2.BotAI) :
    agents = []

    def __init__(self):
        self.agents.append(BaseManager(self))

    async def on_step(self, iteration) :
        for agent in self.agents:
            await agent.doAction()
