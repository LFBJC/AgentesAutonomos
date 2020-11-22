import sc2
import Strategist
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from Strategist import Strategist

run_game(maps.get("AcropolisLE"), [Bot(Race.Terran, Strategist()), Computer(Race.Zerg, Difficulty.Easy)], realtime = False)
