
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
        # width and height of the window
        self.width = 800
        self.height = 300

        # the distance in meters which will be drawn
        self.MINSCENERANGE = 50 #the minimum range which will be shown on screen
        self.MAXSCENERANGE = 100 #the maximum range which will be shown on screen
        self.borderDistance = self.MAXSCENERANGE / 10.0 #the distance at which the boat stay from the window-border when pushing the limit
        self.sceneRange = 50 #the current range which will be shown on screen
        self.sceneStartOffset = -(self.sceneRange/2) #where the scene starts
        self.sceneEndOffset = self.sceneRange #where the scene ends (put in a bit more meters than necessary)

        self.LANEWIDTH = 10 # the steps where the distance will be shown
        self.LANEWIDTHBIG = 50 #the steps where more special marks are used to show the distance
        self.laneHeight = 50 # the height between the lanes

        self.CYCLETIME = 10
        self.currentDistance = 0.0

        self.callbacks = [] #the callbacks which are called every cycle
        self.starttime = 0

        #these attributes are needed to calc the FPS
        self.MAXTICKSAMPLES = 100
        self.tickIndex = 0
        self.tickSum = 0.0
        self.tickList = []
        for index in range(0,self.MAXTICKSAMPLES):
            self.tickList.append(0.0)
        self.tickStamp = datetime.now().second * 1000 + datetime.now().microsecond / 1000.0

        pygame.init()
        size = [self.width, self.height]
        self.font = pygame.font.SysFont('Arial', 16)
        self.screen = pygame.display.set_mode(size)

    def calcFps(self, newTick):
        self.tickSum -= self.tickList[self.tickIndex]
        self.tickSum += newTick
        self.tickList[self.tickIndex] = newTick
        self.tickIndex += 1
        if(self.tickIndex == self.MAXTICKSAMPLES):
            self.tickIndex = 0
        deltaT = (self.tickSum / self.MAXTICKSAMPLES)
        return 1000.0 / deltaT

    def run(self):
        #Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()

        while not done:
            #let's lock to 60 FPS
            clock.tick(60)

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
                    continue #Why waste time to paint one last time?

            # Clear the screen and set the screen background
            self.screen.fill(LIGHTSTEELBLUE)

            #if time hasn't been set yet, do it now
            if(self.starttime == 0):
                curr = datetime.now()
                self.starttime = curr.day * 24*60*1000*1000 + curr.hour * 60*1000*1000 + curr.minute*60*1000 + curr.second*1000 + curr.microsecond / 1000

            #calc how much time has been gone
            curr = datetime.now()
            currTime = curr.day * 24*60*1000*1000 + curr.hour * 60*1000*1000 + curr.minute*60*1000 + curr.second*1000 + curr.microsecond / 1000
            timeGone = currTime - self.starttime

            for cb in self.callbacks:
                if(timeGone):
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

        #update the distlanes according to the distance
        self.updateBackground(self.currentDistance)
        self.updatePlayer(self.currentDistance)
        self.updateBoats(playground.boats)

        #display the current FPS in the title
        currentTickStamp = datetime.now().second * 1000 + datetime.now().microsecond / 1000.0
        if(currentTickStamp > self.tickStamp):
            deltaT = currentTickStamp - self.tickStamp
            self.screen.blit(self.font.render("%3.2f FPS" % self.calcFps(deltaT), True, NAVY), (50, 250))
            #pygame.display.set_caption("%3.2f FPS" % self.calcFps(deltaT))
        self.tickStamp = currentTickStamp

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

    def updateBackground(self, distance):
        #this defines the start and end of the scene

        sceneStart = distance + self.sceneStartOffset
        sceneEnd = distance + self.sceneEndOffset

        #print the horizontal lines
        for y in range(0, self.height, self.laneHeight):
            #the offset is needed to "move" the dashed lines along with the rest of the scenery
            #TODO: Adjust the height of lanes according to the current range
            pygame.draw.line(self.screen, STEELBLUE, [0, y + self.laneHeight/2],[self.width, y + self.laneHeight/2], 1)

        for lineStep in range(int(sceneStart), int(sceneEnd), self.LANEWIDTH):
            prevOffset = lineStep - (lineStep % self.LANEWIDTH) #get the previous dividable laneWidth-step
            linePos = (prevOffset - sceneStart) * (self.width / self.sceneRange) #get the position and project the window size

            #create the actual marker
            for heightPos in range(0, self.height, self.laneHeight):
                if(prevOffset % self.LANEWIDTHBIG == 0):
                    pygame.draw.circle(self.screen, FIREBRICK, [int(linePos), int(heightPos + self.laneHeight/2)], 4)
                    pygame.draw.circle(self.screen, BLACK, [int(linePos), int(heightPos + self.laneHeight/2)], 4, 1)
                else:
                    pygame.draw.circle(self.screen, LIGHTGREY, [int(linePos), int(heightPos + self.laneHeight/2)], 2)
                    pygame.draw.circle(self.screen, BLACK, [int(linePos), int(heightPos + self.laneHeight/2)], 2, 1)

            #display the distance marker
            lineText = str(prevOffset)
            pygame.draw.line(self.screen, NAVY, [linePos, 0], [linePos,20], 1)
            self.screen.blit(self.font.render(lineText, True, NAVY), (linePos+15, 8))

    def updatePlayer(self, distance):
        pos = {"posX": self.width/2, "posY": self.height/2}
        self.printBoat(pos, distance, DARKORANGE)

    def printBoat(self, position, distance, color):
        posX = position["posX"]
        posY = position["posY"]
        #the following polygon is calculated with offsets in metres, the offset than is multiplied to
        #match the current projection and windows size
        boatPolygon = [ [posX-(8 * self.width / self.sceneRange), posY],
                        [posX-(4 * self.width / self.sceneRange), posY-(1 * self.width / self.sceneRange)],
                        [posX, posY],
                        [posX-(4 * self.width / self.sceneRange), posY+(1 * self.width / self.sceneRange)]]

        #display the distance of each boat next to it
        distText = "%.2fm" % distance
        pygame.draw.polygon(self.screen, color, boatPolygon)
        pygame.draw.polygon(self.screen, BLACK, boatPolygon, 1)
        self.screen.blit(self.font.render(distText, True, NAVY), (posX-(16 * self.width / self.sceneRange), posY - (1 * self.width / self.sceneRange)))

    def updateBoats(self, boats):
        for index, boat in enumerate(boats):
            #calc the height
            currentLane = (index + 1) * self.laneHeight
            if(currentLane >= self.height/2): #do not use the players lane
                currentLane += self.laneHeight

            #calc the horizontal position
            relativeDistance = boat.distance-self.currentDistance
            boatPos = relativeDistance * (self.width / self.sceneRange) + self.width/2

            #print the boat
            pos = {"posX": boatPos, "posY": currentLane }
            self.printBoat(pos, boat.distance, GREEN)

    def registerCallback(self, callback):
        self.callbacks.append(callback)

    def setCycleTime(self, time):
        self.CYCLETIME = time

