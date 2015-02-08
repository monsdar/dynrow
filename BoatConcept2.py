from Boat import Boat
import time

try:
    import pyrow
except Exception as e:
    print "Error importing Pyrow: " + str(e)


class BoatConcept2(Boat):
    def __init__(self, name, distance=0):
        Boat.__init__(self, name, distance)
        self.erg = None
        self.spm = 20       #Strokes per Minute
        self.pace = 135.2   #pace in seconds (2:15.0 equals 135.0)
        self.calhr = 10     #TODO: What format does the ergo return?
        self.power = 150    #Power in Watts
        self.calories = 0   #Calories burned away
        self.heartrate = 155#Heartrate

    def initialize(self):
        try:
            # connect to the boat, this could block some time...
            ergs = []
            while (len(ergs) == 0):
                ergs = pyrow.find()
            self.erg = pyrow.pyrow(ergs[0])
            print "Connected to erg"

            #Loop until workout has begun
            print "Waiting for workout to start ..."
            workout = self.erg.getWorkout()
            while workout['state'] == 0:
                time.sleep(0.1)
                try:
                    workout = self.erg.getWorkout()
                except:
                    continue
            print "Workout has begun"
        except Exception as e:
            print "Error initing the Concept2: " + str(e)
            return

    def move(self, timeGone):
        if (self.erg == None):
            self.distance += 0.05
            return

        #Get the distance from the Concept2 ergo. Do nothing if errors occur
        try:
            monitor = self.erg.getMonitor() #get monitor data for start of stroke
            self.distance = monitor['distance']
            self.spm = monitor['spm']
            self.pace = monitor['pace']
            self.power = monitor['power']
            self.calhr = monitor['calhr']
            self.calories = monitor['calories']
            self.heartrate = monitor['heartrate']
        except:
            print "Error receiving monitor status"
