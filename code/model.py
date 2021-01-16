import numpy as np
import matplotlib.pyplot as plt

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid, HexGrid
from mesa.time import RandomActivation

from agent import Pedestrian


class ContactModel(Model):
    def __init__(self, N, height, width, exponent):
        self.number_of_agents = N
        self.height = height
        self.width = width
        self.exponent = exponent

        self.current_step_contacts=[]
        self.adjacency_matrix = np.zeros((N, N))
        self.grid = MultiGrid(self.width, self.height, torus=False)
        self.schedule = RandomActivation(self)

         # Add N pedestrians to model (schedule, grid)
        taken_pos = []
        for i in range(self.number_of_agents):
            while True:
                x = self.random.randrange(1, self.grid.width-1)
                y = self.random.randrange(1, self.grid.height-1)
                pos = (x,y)
                if not pos in taken_pos:
                    break

            new_human = Pedestrian(i, self, pos, self.exponent)
            self.schedule.add(new_human)

            self.grid.place_agent(new_human, pos)
            taken_pos.append(pos)

        self.data_collector=DataCollector()

        self.running=True
        self.data_collector.collect(self)

    def contact_update(self, contact_ids):

        contact_ids  =sorted(contact_ids)
        if contact_ids not in self.current_step_contacts:
            self.current_step_contacts.append(contact_ids)


    def update_adjecency_matrix(self):

        #TODO: order agent steps, order updates, double or not
        for id_tuple in self.current_step_contacts:
            self.adjacency_matrix[id_tuple[0], id_tuple[1]]+=1

    def step(self):
        self.schedule.step()
        self.update_adjecency_matrix()
        self.current_step_contacts=[]
        self.data_collector.collect(self)

    def run(self, N):
        for i in range(N):
            print(i)
            self.step()

        #distances = []
        #lengths = []
        global_test=[]
        global_trip_info=[]

        for agent in self.schedule.agents:
            agent.trip_info.pop()
            global_trip_info.append(agent.trip_info)

        return global_trip_info

'''
N=145
it = 10000
width = 139
height = 139
model = ContactModel(N, width, height)
global_trip_info = model.run(it)

lengths = []
distances = []
for info in global_trip_info:
    for trip in info:
        lengths.append(trip[0])
        distances.append(int(trip[1]))

lengths_count = {}
for length in lengths:
    if length in lengths_count:
        lengths_count[length]+=1
    else:
        lengths_count[length]=1

distances_count = {}
for distance in distances:
    if distance in distances_count:
        distances_count[distance]+=1
    else:
        distances_count[distance]=1

max_x = max(distances)+20
max_y = max(max(lengths_count.values()), max(distances_count.values()))+10
plt.bar(list(lengths_count.keys()), lengths_count.values())
plt.title('Trip length: steps')
plt.xlim(xmax=max_x)
plt.ylim(ymax=max_y)
plt.xlabel('steps')
plt.ylabel('count')
plt.show()

plt.bar(list(distances_count.keys()), distances_count.values())
plt.title('Trip length: euclidian distance')
plt.xlim(xmax=max_x)
plt.ylim(ymax=max_y)
plt.xlabel('distance')
plt.ylabel('count')
plt.show()


# Save adjacency matrix
matrix = np.asarray(model.adjacency_matrix)
matrix[matrix==0]=['nan']
#print(model.adjacency_matrix)
new_matrix = np.zeros((N+1, N+1))
for i in range(N):
    new_matrix[0,i+1] = int(i)
    new_matrix[i+1, 0] = int(i)

#print(new_matrix)
for i in range(1, N+1):
    for j in range(1, N+1):
        new_matrix[i, j] = matrix[i-1, j-1]

#print(new_matrix)
np.savetxt(f'../results/test2/adjacency_N{N}_{width}x{height}_i{it}.csv', new_matrix, delimiter=";")

# Save area matrices
for agent in model.schedule.agents:
    np.savetxt(f'../results/test2/agent_areas/agent{agent.unique_id}.csv', agent.area_traversed, delimiter=";")
'''
