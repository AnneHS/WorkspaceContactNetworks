from mesa.visualization.modules import CanvasGrid, ChartModule, CanvasHexGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import ContactModel
from agent import Pedestrian

def agent_portrayal(agent):
    if type(agent) is Pedestrian:
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": "blue",
                     "r": 0.5}


    return portrayal

grid = CanvasGrid(agent_portrayal, 114, 114,570, 570)
#N, grid_size, grid_size, exp, STEPS, seed=8
server = ModularServer(ContactModel, [grid], "Evacuation Model", {"N":145, "height":114,"width":114, "exponent":1.6, "steps": 1000, "seed":8})

server.port = 8420 #8422 #default
server.launch()
