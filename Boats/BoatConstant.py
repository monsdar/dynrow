import math

from Logic.Boat import Boat


class BoatConstant(Boat):
    def __init__(self, name, pace=150, spm=20, distance=0):
        super(BoatConstant, self).__init__(name, distance)
        self.pace = pace            #time in seconds the boat needs to row 500m
        self.originalPace = pace    #do not forget the original pace
        self.spm = spm              #strokes per minute
        self.amplitude = 0.1       #amplitude with which the boats are rowing

        self.offsetTime = 0.0 #needed if the boat changes its pace
        self.offsetDist = 0.0 #needed if the boat changes its pace
        self.currentTime = 0.0#needed if the boat changes its pace

    def reset(self):
        super(BoatConstant, self).reset()
        self.pace = self.originalPace
        self.offsetTime = 0.0
        self.offsetDist = 0.0
        self.currentTime = 0.0

    def changePace(self, newPace):
        self.pace = newPace
        self.offsetTime = self.currentTime
        self.offsetDist = self.distance

    def move(self, timeGone):
        self.currentTime = timeGone
        strokesPerSecond = self.spm / 60.0
        velocity = 500.0 / self.pace

        timeGoneOffset = (timeGone - self.offsetTime) #apply theo ffset onto the time
        timeCalc = timeGoneOffset + self.amplitude * -math.sin(timeGoneOffset * strokesPerSecond * 2.0 * math.pi)
        self.distance = self.offsetDist + (velocity * timeCalc)
