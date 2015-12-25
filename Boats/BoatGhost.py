
from Logic.Boat import Boat
from Storage.SQLiteStorage import SQLiteStorage

class BoatGhost(Boat):
    def __init__(self, name, filename, distance=0):
        super(BoatGhost, self).__init__(name, distance)
        self.storage = SQLiteStorage(filename)

    def move(self, timeGone):
        data = self.storage.getDataTuple(timeGone)
        if not data == None:
            self.distance = data[0]
            self.pace = data[2]
