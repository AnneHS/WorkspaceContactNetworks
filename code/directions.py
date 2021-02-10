import numpy as np
import random
import math


random.seed(8)

class Directions():
    def __init__(self, range):
        self.range = range
        self.directions = []
        self.generate_directions()

    #@jit(nopython=True)
    def generate_directions(self):
        shifts = np.arange(-self.range, self.range+1, 1)

        # Append shifts clockwise
        for shift in shifts:
            self.directions.append([-self.range, shift])
        for shift in shifts[1:]:
            self.directions.append([shift, self.range])
        for shift in shifts[-2::-1]:
            self.directions.append([self.range, shift])
        for shift in shifts[-2:0:-1]:
            self.directions.append([shift, -self.range])

    def correlated(self, current_direction, i):
        dir = [current_direction.x_shift, current_direction.y_shift]
        index = (self.directions.index(dir) + i)%len(self.directions)
        new_direction = self.directions[index]
        return Direction(new_direction, self.range)
        #pass


class Direction():
    def __init__(self, direction, range):
        self.x_shift = direction[0]
        self.y_shift = direction[1]
        self.range = range

    def calculate_steps(self, trip_length):
        ''' Calculate number of steps needed to cover trip_length, taking into
        account the current direction. '''

        avg_xmove = abs(self.x_shift)/self.range
        avg_ymove = abs(self.y_shift)/self.range

        # horizontal or vertical
        if self.x_shift==0 or self.y_shift == 0:
            number_of_steps = trip_length
        # pure diagonal
        elif abs(self.x_shift) == abs(self.y_shift):
            number_of_steps = int(trip_length/math.sqrt(2))

        # non-pure diagonals
        elif avg_xmove == 1:
            avg_step_length = avg_ymove * math.sqrt(2) + (1-avg_ymove) * 1
            number_of_steps = int((trip_length/avg_step_length))
        elif avg_ymove == 1:
            avg_step_length = avg_xmove * math.sqrt(2) + (1-avg_xmove) * 1
            number_of_steps = int((trip_length/avg_step_length))

        return number_of_steps

    def move(self):
        ''' Move according to direction (x-coordinate, y-coordinate)'''
        if random.random() < (abs(self.x_shift)/self.range):
            if self.x_shift > 0:
                x_move = 1
            elif self.x_shift < 0:
                x_move = -1
        else:
            x_move = 0

        if random.random() < (abs(self.y_shift)/self.range):
            if self.y_shift > 0:
                y_move = 1
            elif self.y_shift < 0:
                y_move = -1
        else:
            y_move = 0

        return np.array([x_move, y_move])

    def change(self, shift):
        ''' Mirror direction when bouncing off wall'''

        if shift[0] > 0 and self.x_shift < 0 or shift[0] < 0 and self.x_shift > 0:
            self.x_shift = -self.x_shift
        if shift[1] > 0 and self.y_shift < 0 or shift[1] < 0 and self.y_shift > 0:
            self.y_shift = -self.y_shift

    def __str__(self):
        return f'Direction is {self.x_shift}, {self.y_shift}'


'''
#directions=np.random.uniform(-np.pi,np.pi,size=N)
#print(directions)
print(360/24)
angle_step = 15
N=100
for i in range(N):
    radians = np.random.vonmises(0, kappa=4)
    degrees = math.degrees(radians)
    jumps = math.floor(degrees/15)
    print(radians, degrees, jumps)
'''
