import numpy as np
import matplotlib.pyplot as plt

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid, HexGrid
from mesa.time import BaseScheduler

from numba import jit

from agent import Pedestrian
from directions import Directions


class ContactModel(Model):

    #@jit(nopython=True)
    def __init__(self, N, height, width, exponent, steps):
        self.number_of_agents = N
        self.height = height
        self.width = width
        self.exponent = exponent

        #self.x_locs = np.zeros((N, steps))
        #self.y_locs = np.zeros((N))

        self.direction_range=3
        self.directions = Directions(self.direction_range)
        self.current_step_contacts=[]
        self.adjacency_matrix = np.zeros((N, N))
        self.grid = MultiGrid(self.width, self.height, torus=False)
        self.schedule = BaseScheduler(self)

        self.current_step = 0

         # Add N pedestrians to model (schedule, grid)
        for i in range(self.number_of_agents):
            x = self.random.randrange(1, self.grid.width-1)
            y = self.random.randrange(1, self.grid.height-1)

            pos = (x, y)
            new_human = Pedestrian(i, self, pos, self.exponent, self.directions)

            self.schedule.add(new_human)
            self.grid.place_agent(new_human, pos)

        self.data_collector=DataCollector()

        self.running=True
        self.data_collector.collect(self)

    '''
    #@jit(nopython=True)
    def contact_update(self, contact_ids):

        contact_ids  =sorted(contact_ids)
        if contact_ids not in self.current_step_contacts:
            self.current_step_contacts.append(contact_ids)
    '''

    #@jit(nopython=True)
    def update_adjecency_matrix(self):

        agents = self.schedule.agents
        for i, agent in enumerate(agents):
            neighbors = self.grid.get_neighbors(agent.pos, moore=True, radius= 5)
            for neighbor in neighbors:
                if neighbor.unique_id > agent.unique_id:
                    self.adjacency_matrix[agent.unique_id, neighbor.unique_id]+=1



        '''
        neighbors_in_contact = self.model.grid.get_neighbors(self.pos, moore=True, radius = 5)
        if len(neighbors_in_contact) > 0:
            for neighbor in neighbors_in_contact:
                if neighbor.unique_id != self.unique_id:
                    self.model.contact_update((self.unique_id, neighbor.unique_id))

        #TODO: order agent steps, order updates, double or not
        for id_tuple in self.current_step_contacts:
            self.adjacency_matrix[id_tuple[0], id_tuple[1]]+=1
        '''

    #@jit(nopython=True)
    def step(self):
        self.schedule.step()

        #self.update_adjecency_matrix()
        #self.current_step_contacts=[]
        self.data_collector.collect(self)

    #@jit(nopython=True)
    def run(self, N):
        for i in range(N):
            self.current_step+=1
            self.step()
            if i%100 == 0:
                print(i)
