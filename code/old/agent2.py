import numpy as np
import powerlaw
import random

from mesa import Agent, Model
from mesa.time import RandomActivation
#from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class Pedestrian(Agent):
    def __init__(self, unique_id, model, pos):
        self.unique_id = unique_id
        self.model = model
        self.pos = pos
        self.traversable = True
        self.trip_lengths = powerlaw.Power_Law(xmin=7, parameters=[1.9]) #1.5-2.0 #xmin 17?
        self.directions = np.arange(0, 18)

        #self.not_moved = False

        ##self.on_trip = False
        #self.current_direction = 0
        self.remaining_steps = 0
        #self.remaining_steps_in_current_direction = 0

    def get_position(self):
        return self.pos

    def contact(self):
        in_contact = self.model.grid.get_cell_list_contents([self.pos])
        if len(in_contact) > 1:
            for other in in_contact:
                if other.unique_id != self.unique_id:
                    self.model.contact_update((self.unique_id, other.unique_id))

    def plan_trip(self):
        length_of_trip =  int(self.trip_lengths.generate_random(1)[0]) #generate_random ignores xmax
        self.remaining_steps = length_of_trip
        self.on_trip = True

        print("Pedestrian {}, currently at {}, is on a trip of length {}".format(self.unique_id, self.pos, self.remaining_steps))

    def check_if_traversable(self, coordinates):

        possible_coordinates=[]
        for coordinate in coordinates:
            if ( 0 <= coordinate[0] < self.model.width) and (0 <= coordinate[1] < self.model.height):
                contents = self.model.grid.get_cell_list_contents(coordinate)

                cell_traversable = True
                for content in contents:
                    if not content.traversable:
                        cell_traversable= False
                if cell_traversable:
                    possible_coordinates.append(coordinate)

        return possible_coordinates

    def get_coordinates_in_range(self, distance):
        '''
        Returns a list of coordinates at given distance, that are inside the
            grid and traversable
        '''
        # get possible shifts
        x_shifts = np.arange(-distance, distance+1, 1)
        y_shifts = np.arange(-distance, distance+1, 1)
        possible_shifts=[]
        for x_shift in x_shifts:
            for y_shift in y_shifts:
                if abs(x_shift) + abs(y_shift) == distance:
                    possible_shifts.append((x_shift, y_shift))

        # get possible coordinates: in grid and traversable
        coordinates = []
        for shift in possible_shifts:
            new_x = self.pos[0] + shift[0]
            new_y = self.pos[1] + shift[1]
            coordinate = (new_x, new_y)
            coordinates.append(coordinate)

        possible_coordinates = self.check_if_traversable(coordinates)

        return possible_coordinates


    def change_direction(self):
        '''
        Change direction: selects destination coordinate at distance 3,
            or less if less than 3 steps remaining for current trip.
        '''

        if self.remaining_steps >= 3:
            distance = 3
        else:
            distance = self.remaining_steps
        coordinates = self.get_coordinates_in_range(distance)

        self.current_direction = random.choice(coordinates)
        self.remaining_steps_in_current_direction = distance

    def get_possible_moves(self):

        x = self.pos[0]
        y = self.pos[1]
        x_dist = self.current_direction[0] - x
        y_dist = self.current_direction[1] - y

        moves=[]
        if x_dist < 0:
            moves.append((x-1, y))
        elif x_dist > 0:
            moves.append((x+1, y))
        if y_dist < 0:
            moves.append((x, y-1))
        elif y_dist > 0:
            moves.append((x, y+1))

        possible_moves = self.check_if_traversable(moves)
        return possible_moves

    def move(self):

        if self.remaining_steps == 0:
            self.plan_trip()
        if self.remaining_steps_in_current_direction == 0:
            self.change_direction()

        possible_moves = self.get_possible_moves()
        #print(possible_moves)
        if len(possible_moves) > 0:
            new_position = random.choice(possible_moves)
            self.model.grid.move_agent(self, new_position)
            self.remaining_steps -= 1
            self.remaining_steps_in_current_direction -=1
        else:
            # Random move to prevent deadlock
            if self.not_moved:
                possible_steps = self.model.grid.get_neighborhood(
                    self.pos,
                    moore=True,
                    include_center=False)
                new_position = self.random.choice(possible_steps)
                self.model.grid.move_agent(self, new_position)
                self.remaining_steps_in_current_direction = abs(self.pos[0] - self.current_direction[0]) + abs(self.pos[1] - self.current_direction[1])
            else:
                self.not_moved = True

    def step(self):
        self.move()
        self.contact()
