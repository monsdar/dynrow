

import time

try:
    from PyRow import pyrow
except Exception as e:
    print "Error importing Pyrow: " + str(e)


class ErgStats:
    erg = None
    distance = 0.0 #distance in m
    spm = 20       #Strokes per Minute
    pace = 135.2   #pace in seconds (2:15.0 equals 135.0)
    calhr = 10     #TODO: What format does the ergo return?
    power = 150    #Power in Watts
    calories = 0   #Calories burned away
    heartrate = 155#Heartrate

    @staticmethod
    def initialize():
        try:
            # connect to the ergometer, this call could block some time...
            ergs = []
            while (len(ergs) == 0):
                ergs = pyrow.find()
            ErgStats.erg = pyrow.pyrow(ergs[0])
            print "Connected to erg"

            #Loop until workout has begun
            print "Waiting for workout to start ..."
            workout = ErgStats.erg.getWorkout()
            while workout['state'] == 0:
                time.sleep(0.1)
                try:
                    workout = ErgStats.erg.getWorkout()
                except:
                    continue
            print "Workout has begun"
        except Exception as e:
            print "Error initing the Concept2: " + str(e)
            return

    @staticmethod
    def update():
        #TODO: This is just for testing purposes. It simulates a moving boat by increasing the distance every cycle
        if (ErgStats.erg == None):
            ErgStats.distance += 0.0591715976331361
            return

        #Get the distance from the Concept2 ergo. Do nothing if errors occur
        try:
            monitor = ErgStats.erg.getMonitor() #get monitor data for start of stroke
            ErgStats.distance = monitor['distance']
            ErgStats.spm = monitor['spm']
            ErgStats.pace = monitor['pace']
            ErgStats.power = monitor['power']
            ErgStats.calhr = monitor['calhr']
            ErgStats.calories = monitor['calories']
            ErgStats.heartrate = monitor['heartrate']
        except:
            print "Error receiving monitor status"
