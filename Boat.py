
import math

class Boat():
    def __init__(self, name, distance=0):
        self.name = name            #name of the Rower
        self.distance = distance    #distance in m the boat has rowed
        print "Created Boat " + self.name
    
    def getDistance(self):
            return self.distance
    
    def move(self, timeGone):
        pass