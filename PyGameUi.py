
import math
import pygame
from datetime import datetime

# Define the colors we will use in RGB format
LIGHTSTEELBLUE  = (135, 206, 250)
STEELBLUE       = ( 70, 130, 180)
LIGHTGREY       = (211, 211, 211)
FIREBRICK       = (178,  34,  34)
NAVY            = (  0,   0, 128)
DARKORANGE      = (255, 140,   0)
BLACK           = (  0,   0,   0)
GREEN           = (  0, 128,   0)

class PyGameUi():
    def __init__(self):
        self.MINSCENERANGE = 50 #the minimum range which will be shown on screen
        self.MAXSCENERANGE = 100 #the maximum range which will be shown on screen
        self.borderDistance = self.MAXSCENERANGE / 10.0 #the distance at which the boat stay from the window-border when pushing the limit
        self.sceneRange = 50 #the current range which will be shown on screen
        self.sceneStartOffset = -(self.sceneRange/2) #where the scene starts
        self.sceneEndOffset = self.sceneRange #where the scene ends (put in a bit more meters than necessary)

        self.LANEWIDTH = 10 # the steps where the distance will be shown
        self.LANEWIDTHBIG = 50 #the steps where more special marks are used to show the distance
        self.laneHeight = 10.0 # the height between the lanes
        self.playerLane = 2 #the lane where the player is located (counting starts with 0)

        self.CYCLETIME = 10
        self.currentDistance = 0.0

        self.callbacks = [] #the callbacks which are called every cycle
        self.starttime = 0

        #init PyGame
        pygame.init()

        # width and height of the fullscreen window
        modes = pygame.display.list_modes()
        print 'Using fullscreen resolution:', modes[0]
        #self.screen = pygame.display.set_mode(modes[0], pygame.FULLSCREEN)
        #self.width = modes[0][0]
        #self.height = modes[0][1]
        self.screen = pygame.display.set_mode([1366, 768])
        self.width = 1366
        self.height = 768
        self.statPanelHeight = 300
        self.racePanelHeight = self.height - self.statPanelHeight

        #this is the font we're using throughout the game
        self.font = pygame.font.SysFont('Arial', 32)

    def getTimestamp(self):
        curr = datetime.now()
        return curr.day * 24 * 60 * 1000 * 1000 + curr.hour * 60 * 1000 * 1000 + curr.minute * 60 * 1000 + curr.second * 1000 + curr.microsecond / 1000

    def run(self):
        #Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()

        while not done:
            #let's lock to 60 FPS
            clock.tick(60)
            pygame.display.set_caption("%3.2f FPS" % clock.get_fps())

            for event in pygame.event.get(): # User did something
                if (event.type == pygame.QUIT) or (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done=True # Flag that we are done so we exit this loop
                    continue #Why waste time to paint one last time?

            # Clear the screen and set the screen background
            self.screen.fill(LIGHTSTEELBLUE)

            #if time hasn't been set yet, do it now
            if(self.starttime == 0):
                self.starttime = self.getTimestamp()

            #calc how much time has been gone
            currTime = self.getTimestamp()
            timeGone = currTime - self.starttime

            for cb in self.callbacks:
                cb(timeGone)

            # Go ahead and update the screen with what we've drawn.
            # This MUST happen after all the other drawing commands.
            pygame.display.flip()

        #Quit everything after the GameLoop ends
        pygame.quit()

    def update(self, playground):
        #Get the current distance from the player boat
        self.currentDistance = playground.getPlayerBoat().distance
        self.adjustDistance(playground.boats, self.currentDistance)

        #update the racing section
        self.updateRaceBackground(self.currentDistance)
        self.updatePlayer(self.currentDistance)
        self.updateBoats(playground.boats)

        #update the stat section
        self.updateStatBackground(self.currentDistance)

    def adjustDistance(self, boats, distance):
        #check the distance from player to the first boat
        distToFirst = 0.0
        for boat in boats:
            dist = (boat.distance + self.borderDistance) - distance
            if(dist > (self.MAXSCENERANGE / 2.0)):
                dist = (self.MAXSCENERANGE / 2.0) - (dist - (self.MAXSCENERANGE / 2.0))
            if( dist > 0.0 and dist > distToFirst ):
                distToFirst = dist

        #check the distance from player to last boat
        distToLast = 0.0
        for boat in boats:
            dist = (boat.distance - self.borderDistance) - distance
            if(dist < -(self.MAXSCENERANGE / 2.0)):
                dist = -(self.MAXSCENERANGE / 2.0) - (dist + (self.MAXSCENERANGE / 2.0))
            if(dist < 0.0 and dist < distToLast):
                distToLast = dist

        #get the total distance between boats and calc the new sceneRange
        totalDist = 0.0
        if(distToFirst > -distToLast):
            totalDist = distToFirst * 2.0
        else:
            totalDist = -(distToLast * 2.0)

        if(totalDist > self.MINSCENERANGE and totalDist < self.MAXSCENERANGE):
            self.sceneRange = totalDist
            self.sceneStartOffset = -(self.sceneRange/2)
            self.sceneEndOffset = self.sceneRange

    def updateStatBackground(self, currentDistance):
        self.screen.fill(LIGHTGREY, [[0, 0], [self.width, self.statPanelHeight]])

    def updateRaceBackground(self, distance):
        #this defines the start and end of the scene
        sceneStart = distance + self.sceneStartOffset
        sceneEnd = distance + self.sceneEndOffset

        #the following factors are used to calculate from a distance in meters into a distance on the
        #screen (1m in our simulation is not 1px on the screen, depends on the sceneRange we've got)
        heightFactor = self.racePanelHeight / self.sceneRange
        widthFactor = self.width / self.sceneRange

        #print the horizontal lines
        for y in range(self.statPanelHeight, self.height, int(self.laneHeight * heightFactor)):
            pygame.draw.line(self.screen, STEELBLUE, [0, y + (self.laneHeight/2) * heightFactor],[self.width, y + (self.laneHeight/2) * heightFactor], 1)

        for lineStep in range(int(sceneStart), int(sceneEnd), self.LANEWIDTH):
            prevOffset = lineStep - (lineStep % self.LANEWIDTH) #get the previous dividable laneWidth-step
            linePos = (prevOffset - sceneStart) * widthFactor #get the position and project the window size

            #create the actual marker
            for heightPos in range(self.statPanelHeight, self.height, int(self.laneHeight * heightFactor)):
                if(prevOffset % self.LANEWIDTHBIG == 0):
                    pygame.draw.circle(self.screen, FIREBRICK, [int(linePos), int(heightPos + (self.laneHeight/2) * heightFactor)], 4)
                    pygame.draw.circle(self.screen, BLACK, [int(linePos), int(heightPos + (self.laneHeight/2) * heightFactor)], 4, 1)
                else:
                    pygame.draw.circle(self.screen, LIGHTGREY, [int(linePos), int(heightPos + (self.laneHeight/2) * heightFactor)], 2)
                    pygame.draw.circle(self.screen, BLACK, [int(linePos), int(heightPos + (self.laneHeight/2) * heightFactor)], 2, 1)

            #display the distance marker
            lineText = str(prevOffset)
            pygame.draw.line(self.screen, NAVY, [linePos, self.statPanelHeight], [linePos, self.statPanelHeight+20], 1)
            self.screen.blit(self.font.render(lineText, True, NAVY), (linePos+15, self.statPanelHeight+8))

    def updatePlayer(self, distance):
        #the following factors are used to calculate from a distance in meters into a distance on the
        #screen (1m in our simulation is not 1px on the screen, depends on the sceneRange we've got)
        heightFactor = self.racePanelHeight / self.sceneRange

        currentHeight = (self.playerLane + 1) * self.laneHeight * heightFactor + self.statPanelHeight
        pos = {"posX": self.width/2 , "posY": currentHeight}
        self.printBoat(pos, distance, DARKORANGE)

    def printBoat(self, position, distance, color):
        #the following factors are used to calculate from a distance in meters into a distance on the
        #screen (1m in our simulation is not 1px on the screen, depends on the sceneRange we've got)
        heightFactor = self.racePanelHeight / self.sceneRange
        widthFactor = self.width / self.sceneRange

        posX = position["posX"]
        posY = position["posY"]
        #this is how the boat looks:
        boatPolygon = [ [posX-(8 * widthFactor), posY],
                        [posX-(4 * widthFactor), posY-(1.5 * heightFactor)],
                        [posX, posY],
                        [posX-(4 * widthFactor), posY+(1.5 * heightFactor)]]

        #display the distance of each boat next to it
        pygame.draw.polygon(self.screen, color, boatPolygon)
        pygame.draw.polygon(self.screen, BLACK, boatPolygon, 1)

        if(distance == self.currentDistance):
            distText = "%.0fm" % distance
        else:
            distText = "%.0fm" % float(distance - self.currentDistance)
        txtX = posX - (10 * widthFactor)
        if(txtX < 10):
            txtX = 10
        elif(txtX > (self.width - 100)):
            txtX = (self.width - 100)
        txtY = posY - (1.0 * heightFactor)
        self.screen.blit(self.font.render(distText, True, NAVY), (txtX, txtY))

    def updateBoats(self, boats):
        #the following factors are used to calculate from a distance in meters into a distance on the
        #screen (1m in our simulation is not 1px on the screen, depends on the sceneRange we've got)
        heightFactor = self.racePanelHeight / self.sceneRange
        widthFactor = self.width / self.sceneRange

        for index, boat in enumerate(boats):
            #calc the height
            if(index >= self.playerLane):
                index += 1
            currentLane = (index + 1) * self.laneHeight * heightFactor + self.statPanelHeight

            #calc the horizontal position
            relativeDistance = boat.distance-self.currentDistance
            boatPos = relativeDistance * widthFactor + self.width/2

            #print the boat
            pos = {"posX": boatPos, "posY": currentLane }
            self.printBoat(pos, boat.distance, GREEN)

    def registerCallback(self, callback):
        self.callbacks.append(callback)

    def setCycleTime(self, time):
        self.CYCLETIME = time


