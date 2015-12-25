# http://stackoverflow.com/questions/4151320/efficient-circular-buffer
from collections import deque
class CircularBuffer(deque):
    def __init__(self, size=0):
            super(CircularBuffer, self).__init__(maxlen=size)
    @property
    def average(self):  # TODO: Make type check for integer or floats
            return float(sum(self))/len(self)


