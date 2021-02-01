import numpy as np
import matplotlib.pyplot as plt

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid, HexGrid
from mesa.time import RandomActivation, BaseScheduler

from agent import Pedestrian

class ContactModel(Model):
    def __init__(self, N, height, width, exponent, steps, seed):
        self.number_of_agents = N
        self.height = height
        self.width = width
        self.exponent = exponent

        self.x_locs = np.zeros((N, steps+1))
        self.y_locs = np.zeros((N, steps+1))

        self.current_step=0 #NEW

        self.current_step_contacts=[]
        self.adjacency_matrix = np.zeros((N, N))
        self.grid = MultiGrid(self.width, self.height, torus=False)
        self.schedule = BaseScheduler(self)#RandomActivation(self)

         # Add N pedestrians to model (schedule, grid)
        taken_pos = []
        for i in range(self.number_of_agents):
            x = self.random.randrange(1, self.grid.width-1)
            y = self.random.randrange(1, self.grid.height-1)

            pos = (x, y)
            new_human = Pedestrian(i, self, pos, self.exponent, seed=i)

            self.schedule.add(new_human)
            self.grid.place_agent(new_human, pos)
            self.x_locs[i][0] = x
            self.y_locs[i][0] = y
            taken_pos.append(pos)

        self.data_collector=DataCollector()

        self.running=True
        self.data_collector.collect(self)

    def contact_update(self, contact_ids):

        contact_ids  =sorted(contact_ids)
        if contact_ids not in self.current_step_contacts:
            self.current_step_contacts.append(contact_ids)


    def update_adjecency_matrix(self):

        '''
        #TODO: order agent steps, order updates, double or not
        for id_tuple in self.current_step_contacts:
            self.adjacency_matrix[id_tuple[0], id_tuple[1]]+=1
        '''

        agents = self.schedule.agents
        for i, agent in enumerate(agents):
            neighbors = self.grid.get_neighbors(agent.pos, moore=True, radius= 5)
            for neighbor in neighbors:
                if neighbor.unique_id > agent.unique_id:
                    self.adjacency_matrix[agent.unique_id, neighbor.unique_id]+=1

    def step(self):
        self.schedule.step()
        self.update_adjecency_matrix()
        #self.current_step_contacts=[]
        #self.data_collector.collect(self)

    def run(self, N):
        for i in range(N):

            self.step()

            self.current_step+=1 #NEW

            for agent in self.schedule.agents:
                self.x_locs[agent.unique_id][i+1] = agent.pos[0]
                self.y_locs[agent.unique_id][i+1] = agent.pos[1]

            if i%100 == 0:
                print(i)
