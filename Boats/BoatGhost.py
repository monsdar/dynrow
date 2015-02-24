
from Logic.Boat import Boat
from Storage.SQLiteStorage import SQLiteStorage

class BoatGhost(Boat):
    def __init__(self, name, filename, distance=0):
        Boat.__init__(self, name, distance)
        self.storage = SQLiteStorage(filename)

    def reset(self):
        pass

    def move(self, timeGone):
        data = self.storage.getDataTuple(timeGone)
        if not data == None:
            self.distance = data[0]
            self.pace = data[2]
