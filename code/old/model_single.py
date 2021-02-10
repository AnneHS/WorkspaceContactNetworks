import numpy as np
import matplotlib.pyplot as plt

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid, MultiGrid, HexGrid
from mesa.time import RandomActivation, BaseScheduler

from agent import Pedestrian

class ContactModel(Model):
    def __init__(self, N, height, width, exponent, steps, seed):
        self.number_of_agents = N
        self.height = height
        self.width = width
        self.exponent = exponent
        self.range = 5
        self.neighborhood_deltas = self.initialize_neighborhood_deltas()

        self.x_locs = np.zeros((N, steps+1))
        self.y_locs = np.zeros((N, steps+1))

        self.current_step=0 #NEW

        self.current_step_contacts=[]
        self.adjacency_matrix = np.zeros((N, N))
        self.grid = Grid(self.width, self.height, torus=False)
        self.schedule = BaseScheduler(self)#RandomActivation(self)

         # Add N pedestrians to model (schedule, grid)
        taken_pos = []
        for i in range(self.number_of_agents):
            while True:
                x = self.random.randrange(1, self.grid.width-1)
                y = self.random.randrange(1, self.grid.height-1)
                pos = (x,y)
                if not pos in taken_pos:
                    break

            new_human = Pedestrian(i, self, pos, self.exponent, seed=i)
            self.schedule.add(new_human)

            self.grid.place_agent(new_human, pos)
            taken_pos.append(pos)

        self.data_collector=DataCollector()

        self.running=True
        self.data_collector.collect(self)

    def initialize_neighborhood_deltas(self):
        neighborhood_deltas=[]
        for x in range(-self.range, self.range+1):
            for y in range(-self.range, self.range+1):
                if x**2 + y**2 <= self.range**2:
                    neighborhood_deltas.append((x, y))
        return neighborhood_deltas


    def contact_update(self, contact_ids):

        contact_ids  =sorted(contact_ids)
        if contact_ids not in self.current_step_contacts:
            self.current_step_contacts.append(contact_ids)

    def get_neighbor_ids(self, position, id):
        x = position[0]
        y = position[1]
        neighbors = []
        for deltas in self.neighborhood_deltas:
            dx = deltas[0]
            dy = deltas[1]

            nx, ny = x + dx, y + dy
            if (not (0 <= nx < self.width) or not (0 <= ny < self.height)):
                continue

            content = self.grid[nx][ny]
            if isinstance(content, Pedestrian) and content.unique_id != id:
                #neighbors += [content.unique_id]
                neighbors+=[content.unique_id]

        return neighbors

    def update_adjecency_matrix(self):

        '''
        #TODO: order agent steps, order updates, double or not
        for id_tuple in self.current_step_contacts:
            self.adjacency_matrix[id_tuple[0], id_tuple[1]]+=1
        '''
        #print('ADJACENCY UPDATE')
        agents = self.schedule.agents
        for i, agent in enumerate(agents):
            neighbor_ids = self.get_neighbor_ids(agent.pos, agent.unique_id)

            for neighbor_id in neighbor_ids:
                if neighbor_id > agent.unique_id:
                    self.adjacency_matrix[agent.unique_id, neighbor_id]+=1


    def step(self):
        self.schedule.step()
        self.update_adjecency_matrix()
        #self.current_step_contacts=[]
        #self.data_collector.collect(self)

    def run(self, steps):
        for i in range(steps):

            self.step()

            self.current_step+=1 #NEW

            for agent in self.schedule.agents:
                self.x_locs[agent.unique_id][i+1] = agent.pos[0]
                self.y_locs[agent.unique_id][i+1] = agent.pos[1]

            if i%100 == 0:
                print(i)

N=10
grid_size = 20
exp = 1.6
STEPS=10
model =  ContactModel(N, grid_size, grid_size, exp, STEPS, seed=8)
model.run(STEPS)
