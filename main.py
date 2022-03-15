import json
import time

from Task1 import Dijkstra
from Task2_UCS import UCS
from Task2 import BFS
from Task3 import *

COORD_PATH = "json/Coord.json"
COST_PATH = "json/Cost.json"
DIST_PATH = "json/Dist.json"
G_PATH = "json/G.json"

def loadJsonFile(path):
    f = open(path)
    data = json.load(f)
    f.close()
    print("Json file " + path + "has been loaded successfully.")
    return data



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    G = loadJsonFile(G_PATH)
    Cost = loadJsonFile(COST_PATH)
    Dist = loadJsonFile(DIST_PATH)
    Coord = loadJsonFile(COORD_PATH)

    # initializes start and end point
    start = "1"
    end = "50"

    print("---------------- ** Task 1 ** -------------------")
    timeStart = time.time()
    Dijkstra(Cost, Dist, G).findShortestPath(start, end)
    timeStop = time.time()
    print("time: ", timeStop - timeStart)
    print("-------------------------------------------------")

    print("---------------- ** Task 2 BFS** -------------------")
    timeStart = time.time()
    BFS(Cost, Dist, G, 287932).template(start, end)
    timeStop = time.time()
    print("time: ", timeStop - timeStart)
    print("-------------------------------------------------")

    print("---------------- ** Task 2 UCS** -------------------")
    timeStart = time.time()
    UCS(Cost, Dist, G, 287932).UCSbegin(start, end)
    timeStop = time.time()
    print("time: ", timeStop - timeStart)
    print("-------------------------------------------------")

    print("---------------- ** Task 3 ** -------------------")
    timeStart = time.time()
    AStarSearch(Cost, Dist, G, Coord).Astar(start, end)
    timeStop = time.time()
    print("time: ", timeStop - timeStart)
    print("-------------------------------------------------")
