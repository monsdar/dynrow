
import math

class Boat():
    def __init__(self, name, distance=0):
        self.name = name            #name of the Rower
        self.distance = distance    #distance in m the boat has rowed

    def __lt__(self, other):
        if(self.distance < other.distance):
            return False
        else:
            return True

    def getDistance(self):
            return self.distance

    def reset(self):
        self.distance = 0.0

    def move(self, timeGone):
        pass