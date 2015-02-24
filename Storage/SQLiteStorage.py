
import sqlite3
import datetime

from PyRow.ErgStats import ErgStats

class SQLiteStorage(object):
    '''
    If dbName is empty a new file will be created
    Use dbName to load a existing db
    '''
    def __init__(self, dbName=""):
        if dbName == "":
            filename = datetime.datetime.now().strftime("session_%y-%m-%d_%H-%M-%S.db")
        else:
            filename = dbName

        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

        #init the database with all the needed tables if the file has been created
        if dbName == "":
            self.cursor.execute('''CREATE TABLE rowdata (   timestamp real,
                                                            distance real,
                                                            spm int,
                                                            pace real,
                                                            avgpace real,
                                                            calhr real,
                                                            power int,
                                                            calories int,
                                                            heartrate int);''')

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    '''
    Stores the current ErgStats data
    '''
    def storeState(self, timestamp):
        data = (timestamp, ErgStats.distance, ErgStats.spm, ErgStats.pace, ErgStats.avgPace, ErgStats.calhr, ErgStats.power, ErgStats.calories, ErgStats.heartrate)
        self.cursor.execute("INSERT INTO rowdata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", data)

    def getDataTuple(self, timestamp):
        try:
            self.cursor.execute("SELECT distance, spm, pace, avgpace, calhr, power, calories, heartrate FROM rowdata WHERE timestamp >= ? LIMIT 1;", (timestamp,))
            return self.cursor.fetchone()
        except sqlite3.OperationalError:
            return (0.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0, 0)