import time

from Logic.Boat import Boat
from PyRow.ErgStats import ErgStats

class BoatConcept2(Boat):
    def __init__(self, name, distance=0):
        super(BoatConcept2, self).__init__(name, distance)

    def initialize(self):
        pass

    def move(self, timeGone):
        self.distance = ErgStats.distance
        self.pace = ErgStats.pace
