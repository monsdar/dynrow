"""
Rolling Average boat - goes at the rolling average of another boat over the last so many meters.  
The idea is that it tracks another boat and keeps pace with the boats average pace over the last
so many meters.

(C) 2015 Kevin Dahlhausen.  Licensed to Nils Brinkmann for use with DynRow under the same 
license as DynRow is distributed.

"""

from BoatConstant import BoatConstant
from util.CircularBuffer import CircularBuffer

import logbook
log = logbook.Logger("BoatRollingAverage")


class BoatRollingAverage(BoatConstant):
    def __init__(self, name, other_boat, meters_to_average=500, meters_between_pace_updates=10):
        super(BoatRollingAverage, self).__init__(name)
        self.other_boat = other_boat 
        self.meters_to_average = meters_to_average
        self.meters_between_pace_updates=meters_between_pace_updates
        self.reset()

    def reset(self):
        super(BoatRollingAverage, self).reset()
        self.buffer = CircularBuffer(size=self.meters_to_average)
        self.buffer.append(self.other_boat.pace)
        self.pace = 220
        self.current_distance = self.other_boat.distance
        self.next_update_at = self.current_distance
        self.next_update_pace_at = self.current_distance

    def move(self, timeGone):
        # time to record another pace?
        if self.other_boat.distance > self.next_update_at:
            self.next_update_at += 1
            self.buffer.append(self.other_boat.pace)
            log.debug("storing %s for dist %s"%(self.other_boat.pace, self.other_boat.distance))

        # time update this boat's pace to the current rolling average?
        if self.other_boat.distance > self.next_update_pace_at:
            self.next_update_pace_at += self.meters_between_pace_updates
            newPace = int(self.buffer.average+0.5)
            if newPace != self.pace and newPace != 0:
                log.debug("changing pace to %s"%newPace)
                self.changePace(newPace)

        super(BoatRollingAverage, self).move(timeGone)
