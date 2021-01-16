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

grid = CanvasGrid(agent_portrayal, 4, 4, 500, 500)
server = ModularServer(ContactModel, [grid], "Evacuation Model", {"N":1, "height":4,"width":4})

server.port = 8420 #8422 #default
server.launch()
