

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
    avgPace = 0.0  #the average pace for the current session
    calhr = 10     #TODO: What format does the ergo return?
    power = 150    #Power in Watts
    calories = 0   #Calories burned away
    heartrate = 155#Heartrate
    time = 0.0     #the time of the ergometer, this is important to use because it pauses if the user pauses etc
    prevTime = 0.0 #needed to see if the time has been updated (else the player is pausing or something similar)

    numQueries = 0 #the number of queries done to the ergometer. This is needed e.g. to calc the average pace

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
            ErgStats.time = monitor['time']

        except:
            #print "Error receiving monitor status"
            pass

        #calc the average pace
        #init the value at the first time we're in here
        if(ErgStats.avgPace <= 0.000001):
            ErgStats.avgPace = ErgStats.pace

        #just update the average if the time has changed
        if(ErgStats.time != ErgStats.prevTime):
            ErgStats.avgPace = ((ErgStats.avgPace * ErgStats.numQueries) + ErgStats.pace) / (ErgStats.numQueries + 1)
            ErgStats.numQueries += 1

        #TODO: This is just for testing purposes. It simulates a moving boat by increasing the distance every cycle
        if (ErgStats.erg == None):
            #assuming stable 62.5 FPS
            #NOTE: The following plays the simulation at 10x speed
            ErgStats.distance += (0.0591715976331361) * 10.0
            ErgStats.time += 0.016 * 10.0
            #ErgStats.distance += (0.0591715976331361)
            #ErgStats.time += 0.016
            return