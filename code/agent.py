import numpy as np
import powerlaw
import random
import math

from mesa import Agent, Model
from mesa.time import RandomActivation
from directions import Directions, Direction
#from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class Pedestrian(Agent):

    DIRECTION_DEGREES = 15
    #NR_OF_DIRECTIONS = 24

    def __init__(self, unique_id, model, pos, exp, x_min, seed=None):
        self.unique_id = unique_id
        self.model = model
        self.pos = pos

        self.area_traversed = np.zeros((model.width, model.height))
        self.traversable = True
        self.trip_lengths = powerlaw.Power_Law(xmin=x_min, parameters=[exp]) #1.5-2.0 #xmin 17?
        self.direction_range=3
        self.directions = Directions(self.direction_range)
        self.trip_lengths_covered = []
        self.steps_covered = []

        self.area_traversed[self.pos[0], self.pos[1]] = 1
        self.on_trip = False
        self.current_direction = 0
        self.remaining_steps = 0



    def plan_trip(self):
        '''
        Plan new tip:
        i. Determine trip length
        ii. Determine new direction based on current direction (correlated RW)
        '''

        # Direction
        if self.current_direction == 0:  # first trip
            direction = random.choice(self.directions.directions)
            self.current_direction = Direction(direction, self.direction_range)
        else:  # correlated random walk
            radians = np.random.vonmises(0, kappa=4)
            degrees = math.degrees(radians)
            jumps = math.floor(degrees/Pedestrian.DIRECTION_DEGREES)
            self.current_direction = self.directions.correlated(self.current_direction, jumps)

        # Trip length
        length_of_trip =  int(self.trip_lengths.generate_random(1)[0]) #generate_random ignores xmax
        self.remaining_steps = self.current_direction.calculate_steps(length_of_trip)
        self.model.trip_lengths.append(self.remaining_steps)
        self.trip_lengths_covered.append(length_of_trip)
        self.steps_covered.append(self.remaining_steps)



    def contact(self):
        '''
        Find all other agents within range (radius = 5) and update contacts.
        '''
        neighbors_in_contact = self.model.grid.get_neighbors(self.pos, moore=True, radius = 5)
        if len(neighbors_in_contact) > 0:
            for neighbor in neighbors_in_contact:
                if neighbor.unique_id != self.unique_id:
                    self.model.contact_update((self.unique_id, neighbor.unique_id))


    def check_if_traversable(self, coordinate):
        '''
        Check if location is traversable.
        '''

        traversable = True
        if ( 0 <= coordinate[0] < self.model.width) and (0 <= coordinate[1] < self.model.height):
            contents = self.model.grid.get_cell_list_contents(coordinate)

            for content in contents:
                if not content.traversable:
                    traversable = False
        else:
            traversable = False

        return traversable


    def move(self):
        '''
        Move pedestrian one step
        '''
        # Plan new trip, if current trip length reached
        if self.remaining_steps == 0:
            self.plan_trip()

        # Determine move based on current direction
        shift = self.current_direction.move()
        move = (self.pos[0] + shift[0], self.pos[1] + shift[1])

        # Check if move is possible (can't traverse walls)
        if self.check_if_traversable(move):
            new_position = move
            self.model.grid.move_agent(self, new_position)
            self.remaining_steps -=1
        else:
            '''
            If not traversable, determine the two alternative moves (i. bounce
            of vertical wall, ii. bounce of horizontal wall). Determine
            which bouncing move works, then move and update direction accordingly
            '''
            # Bouncing moves
            alternative_shifts = [
            [-shift[0], shift[1]],
            [shift[0], -shift[1]],
            [-shift[0], -shift[1]]
            ]

            # If bouncing move possible --> move and update direction
            # TODO: Possible bias for objects??? Always checks vertical wall shift first
            for bounce_shift in alternative_shifts:

                move = (self.pos[0] + bounce_shift[0], self.pos[1] + bounce_shift[1])
                if self.check_if_traversable(move):

                    # Bounce: move + new direction
                    new_position = move
                    self.model.grid.move_agent(self, new_position)
                    self.remaining_steps -=1
                    self.current_direction.change(bounce_shift)

                    break

    def step(self):
        self.move()
        #self.contact()
