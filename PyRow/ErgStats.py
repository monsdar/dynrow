

import time

try:
    from PyRow import pyrow
except ImportError:
    print "Error importing Pyrow"


class ErgStats(object):
    distance = 0.0   # distance in m
    spm = 0          # Strokes per Minute
    pace = 0.0       # pace in seconds (2:15.0 equals 135.0)
    avgPace = 0.0    # the average pace for the current session
    calhr = 0.0      # These are the approx. calories per hour the user burns
    power = 0        # Power in Watts
    calories = 0     # Calories burned away
    heartrate = 0    # Heartrate
    time = 0.0       # the time of the ergometer, this is important to use because it pauses if the user pauses etc

    # internal stuff (how to hide?)
    prevTime = 0.0   # needed to see if the time has been updated (else the player is pausing or something similar)
    numQueries = 0   # the number of queries done to the ergometer. This is needed e.g. to calc the average pace
    erg = None           # This is the handle to the actual Ergometer-interface
    isConnected = False  # Determines whether the ergometer is connected or not (if no erg is available switch to testing mode)

    @staticmethod
    def connectToErg():
        ergs = []

        try:
            while len(ergs) == 0:
                ergs = pyrow.find()
            ErgStats.erg = pyrow.pyrow(ergs[0])
            ErgStats.isConnected = True
            print "Connected to erg"
        except NameError:
            print "Error initing the Concept2, PyRow not available"

    @staticmethod
    def isWorkoutActive():
        #if there is no erg we can skip all the workout init stuff...
        if not ErgStats.isConnected:
            return True

        # Loop until workout has begun
        workout = ErgStats.erg.getWorkout()
        if workout['state'] == 0:
            return False
        else:
            return True

    @staticmethod
    def resetStatistics():
        ErgStats.distance = 0.0
        ErgStats.spm = 0
        ErgStats.pace = 0.0
        ErgStats.avgPace = 0.0
        ErgStats.calhr = 0.0
        ErgStats.power = 0
        ErgStats.calories = 0
        ErgStats.heartrate = 0
        ErgStats.time = 0.0

        ErgStats.prevTime = 0.0
        ErgStats.numQueries = 0

    @staticmethod
    def update():
        if ErgStats.isConnected:
            # Get the distance from the Concept2 ergo. Do nothing if errors occur
            try:
                monitor = ErgStats.erg.getMonitor()  # get monitor data for start of stroke
                ErgStats.distance = monitor['distance']
                ErgStats.spm = monitor['spm']
                ErgStats.pace = monitor['pace']
                ErgStats.power = monitor['power']
                ErgStats.calhr = monitor['calhr']
                ErgStats.calories = monitor['calories']
                ErgStats.heartrate = monitor['heartrate']
                ErgStats.time = monitor['time']
            except AttributeError:
                # print "Error receiving monitor status"
                pass

            # calc the average pace
            # init the value at the first time we're in here
            if ErgStats.avgPace <= 0.000001:
                ErgStats.avgPace = ErgStats.pace

            # just update the average if the time has changed
            if ErgStats.time - ErgStats.prevTime > 0.01:  # check if some time has passed
                ErgStats.avgPace = ((ErgStats.avgPace * ErgStats.numQueries) + ErgStats.pace) / (ErgStats.numQueries + 1)
                ErgStats.numQueries += 1

            # set the prevTime to be able to compare it next cycle
            ErgStats.prevTime = ErgStats.time

        else:
            # TODO: This is just testing code which activates if no erg is available
            # assuming stable 62.5 FPS
            # NOTE: The following plays the simulation at higher speed for testing purposes
            speed = 10.0
            ErgStats.distance += 0.0591715976331361 * speed
            ErgStats.time += 0.016 * speed
