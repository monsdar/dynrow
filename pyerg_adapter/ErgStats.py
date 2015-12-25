import time, sys

import logbook

log=logbook.Logger("ErgStats")

try:
    import pyerg
except ImportError:
    print "Error importing pyerg"

erg_net = pyerg.ErgNet()


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
    rest_time_remaining = 0 # rest time remaing in interval rest
    interval_count = 0 # 0-based interval count or 0 if not doing intervals
    workout_state = 0  # workout state per Concept 2 API see below
    workout_state_text = [ "Waiting to begin",
                           "Workout row", 
                           "Countdown pause",
                           "Interval rest", 
                           "Work time interval", 
                           "Work distance interval", 
                           "Rest interval end to work time interval begin", 
                           "Rest interval end to work distance interval begin", 
                           "Work time interval end to rest interval begin", 
                           "Work distance interval end to rest interval begin",  
                           "Workout end", 
                           "Workout terminate", 
                           "Workout logged", 
                           "Workout rearm" ] 

    # internal stuff (how to hide?)
    prevTime = 0.0   # needed to see if the time has been updated (else the player is pausing or something similar)
    numQueries = 0   # the number of queries done to the ergometer. This is needed e.g. to calc the average pace
    erg = None           # This is the handle to the actual Ergometer-interface
    isConnected = False  # Determines whether the ergometer is connected or not (if no erg is available switch to testing mode)

    _state = pyerg.ErgState()

    @staticmethod
    def connectToErg():

        num_ergs=0

        try:
            while num_ergs == 0:
                num_ergs = erg_net.discoverErgs()

            ErgStats.erg = pyerg.Erg(0)
            ErgStats.isConnected = True
            log.debug("Connected to erg")
        except NameError:
            log.error("Error initing the Concept2, pyerg not available")

    @staticmethod
    def isWorkoutActive():
        #if there is no erg we can skip all the workout init stuff...
        if not ErgStats.isConnected:
            return True
        # Loop until workout has begun
        return ErgStats.erg.hasStartedRowing()


    @staticmethod
    def resetStatistics():
        log.debug("resetStatistics()")
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

        ErgStats.rest_time_remaining = 0
        ErgStats.interval_count = 0
        ErgStats.workout_state = 0


    @staticmethod
    def update():
        log.debug("update() ErgStats.isConnected=%s"%ErgStats.isConnected)
        if ErgStats.isConnected:
            # Get the distance from the Concept2 ergo. Do nothing if errors occur
            try:
                log.debug("updating from ErgStats.erg....")
                ErgStats.distance = ErgStats.erg.getDistanceRowedSoFar()
                ErgStats.spm = ErgStats.erg.getCadence()
                ErgStats.pace = ErgStats.erg.getPaceInSecondsPer500()
                ErgStats.power = ErgStats.erg.getPower()
                ErgStats.calhr = 0
                ErgStats.calories = ErgStats.erg.getAccumulatedCalories()
                ErgStats.heartrate = ErgStats.erg.getHeartRate()
                ErgStats.time = ErgStats.erg.getSecondsIntoThePiece()
                ErgStats.rest_time_remaining = ErgStats.erg.getRestTime()
                ErgStats.interval_count = ErgStats.erg.getWorkoutIntervalCount()
                ErgStats.workout_state = ErgStats.erg.getWorkoutState()

                log.debug("ErgStats updated: interval_count:%s time:%s dist:%s rest_time:%s"%(ErgStats.interval_count, ErgStats.time, ErgStats.distance, ErgStats.rest_time_remaining))

            except AttributeError as e:
                log.error("Error receiving monitor status: %s"%e)

            # calc the average pace
            # init the value at the first time we're in here
            if ErgStats.avgPace <= 0.000001:
                ErgStats.avgPace = ErgStats.pace

            # just update the average if the time has changed
            log.debug("ErgStats.time:%s  ErgStats.prevTime:%s  diff=%s if > 0.1 will update"%(ErgStats.time, ErgStats.prevTime, ErgStats.time-ErgStats.prevTime))
            if ErgStats.time - ErgStats.prevTime > 0.01:  # check if some time has passed
                ErgStats.avgPace = ((ErgStats.avgPace * ErgStats.numQueries) + ErgStats.pace) / (ErgStats.numQueries + 1)
                ErgStats.numQueries += 1
                log.debug("updated ErgStats.avgPace=%s ErgStats.numQueries=%s"%(ErgStats.avgPace, ErgStats.numQueries))

            # set the prevTime to be able to compare it next cycle
            ErgStats.prevTime = ErgStats.time


        else:
            # TODO: This is just testing code which activates if no erg is available
            # assuming stable 62.5 FPS
            # NOTE: The following plays the simulation at higher speed for testing purposes
            log.debug("no erg available so testing")
            speed = 10.0
            ErgStats.distance += 0.0591715976331361 * speed
            ErgStats.time += 0.016 * speed
