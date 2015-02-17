import math
from Logic.Boat import Boat
from PyRow.ErgStats import ErgStats

class BoatBoomerang(Boat):
    def __init__(self, name, pace=150, spm=20, boomerDistance=50, distance=0):
        Boat.__init__(self, name, distance)
        self.pace = pace            #time in seconds the boat needs to row 500m
        self.originalPace = pace    #do not forget the original pace
        self.spm = spm              #strokes per minute
        self.amplitude = 0.1       #amplitude with which the boats are rowing

        self.boomerDistance = boomerDistance #the distance to the player at which the boomerang activates
        self.boost = 5.0 #the speedboost which the boat will get when out of boomerDistance
        self.lastSecCheck = 0 #the last second where we checked the speed

        self.offsetTime = 0.0 #needed if the boat changes its pace
        self.offsetDist = 0.0 #needed if the boat changes its pace
        self.currentTime = 0.0#needed if the boat changes its pace

    def changePace(self, newPace):
        self.pace = newPace
        self.offsetTime = self.currentTime
        self.offsetDist = self.distance

    def move(self, timeGone):
        currentSec = int((timeGone / 1000.0) % 10)
        if( currentSec != self.lastSecCheck ):
            #if the boat is out of the given distance change the pace get back to the player
            distToPlayer = self.distance - ErgStats.distance
            if(distToPlayer > self.boomerDistance and (not self.pace >= ErgStats.pace) ):
                print "Slower!"
                self.changePace(ErgStats.pace + 5.0)
            elif(distToPlayer < -self.boomerDistance and (not self.pace <= ErgStats.pace) ):
                print "Faster!"
                self.changePace(ErgStats.pace - 5.0)
            elif((distToPlayer <= 1.0) and (distToPlayer >= -1.0) and (not self.pace == self.originalPace)):
                print "Original Pace!"
                self.changePace(self.originalPace)
            self.lastSecCheck = currentSec

        self.currentTime = timeGone
        strokesPerSecond = self.spm / 60.0
        velocity = 500.0 / self.pace

        timeGoneMs = ((timeGone - self.offsetTime) / 1000.0) #time is given in milliseconds, we need seconds
        timeCalc = timeGoneMs + self.amplitude * -math.sin(timeGoneMs * strokesPerSecond * 2.0 * math.pi)
        self.distance = self.offsetDist + (velocity * timeCalc)