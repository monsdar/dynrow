from datetime import datetime

import pygame
pygame.init() #is it a good place to init pygame here?

import Colors
import Fonts

from PyRow.ErgStats import ErgStats
from UI.Monitor import Monitor

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

        self.callbacks = [] #the callbacks which are called every cycle
        self.lastFpsUpdate = 0 #used to update the FPS every now and then

        # width and height of the fullscreen window
        modes = pygame.display.list_modes()
        #TODO: This is just for debugging purposes, but'll probably fuck up the resolution for everyone not using my system setup
        if(modes[0][0] == 1366):
            print 'Using fullscreen resolution:', modes[0]
            self.screen = pygame.display.set_mode(modes[0], pygame.FULLSCREEN)
            self.width = modes[0][0]
            self.height = modes[0][1]
        else:
            self.screen = pygame.display.set_mode([1366, 768])
            self.width = 1366
            self.height = 768
            print 'Using windowed resolution: %i x %i' % (self.width, self.height)
        self.monitorHeight = 300
        self.racePanelHeight = self.height - self.monitorHeight

        self.monitor = Monitor(self.screen, self.width, self.monitorHeight)

    def run(self):
        #Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()

        while not done:
            #let's lock to 60 FPS
            clock.tick(60)

            for event in pygame.event.get(): # User did something
                if (event.type == pygame.QUIT) or (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done=True # Flag that we are done so we exit this loop

            # Clear the screen and set the screen background
            self.screen.fill(Colors.LIGHTSTEELBLUE)

            #update the FPS every second in the window-title (updating too often costs too much performance)
            if not (int(ErgStats.time) == self.lastFpsUpdate):
                pygame.display.set_caption("%3.2f FPS" % clock.get_fps())
                self.lastFpsUpdate = int(ErgStats.time)

            for cb in self.callbacks:
                cb(ErgStats.time)

            # Go ahead and update the screen with what we've drawn.
            # This MUST happen after all the other drawing commands.
            pygame.display.flip()

        #Quit everything after the GameLoop ends
        pygame.quit()

    def update(self, playground):
        #Get the current distance from the player boat
        self.adjustDistance(playground.boats, ErgStats.distance)

        #update the racing section
        self.updateRaceBackground(ErgStats.distance)
        self.updatePlayer()
        self.updateBoats(playground.boats)

        #update the stat section
        self.monitor.updateStats(playground)

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

    def updateRaceBackground(self, distance):
        #this defines the start and end of the scene
        sceneStart = distance + self.sceneStartOffset
        sceneEnd = distance + self.sceneEndOffset

        #the following factors are used to calculate from a distance in meters into a distance on the
        #screen (1m in our simulation is not 1px on the screen, depends on the sceneRange we've got)
        heightFactor = self.racePanelHeight / self.sceneRange
        widthFactor = self.width / self.sceneRange

        #print the horizontal lines
        for y in range(self.monitorHeight, self.height, int(self.laneHeight * heightFactor)):
            pygame.draw.line(self.screen, Colors.STEELBLUE, [0, y + (self.laneHeight/2) * heightFactor],[self.width, y + (self.laneHeight/2) * heightFactor], 1)

        for lineStep in range(int(sceneStart), int(sceneEnd), self.LANEWIDTH):
            prevOffset = lineStep - (lineStep % self.LANEWIDTH) #get the previous dividable laneWidth-step
            linePos = (prevOffset - sceneStart) * widthFactor #get the position and project the window size

            #create the actual marker
            for heightPos in range(self.monitorHeight, self.height, int(self.laneHeight * heightFactor)):
                if(prevOffset % self.LANEWIDTHBIG == 0):
                    pygame.draw.circle(self.screen, Colors.FIREBRICK, [int(linePos), int(heightPos + (self.laneHeight/2) * heightFactor)], 4)
                    pygame.draw.circle(self.screen, Colors.BLACK, [int(linePos), int(heightPos + (self.laneHeight/2) * heightFactor)], 4, 1)
                else:
                    pygame.draw.circle(self.screen, Colors.LIGHTGREY, [int(linePos), int(heightPos + (self.laneHeight/2) * heightFactor)], 2)
                    pygame.draw.circle(self.screen, Colors.BLACK, [int(linePos), int(heightPos + (self.laneHeight/2) * heightFactor)], 2, 1)

            #display the distance markers
            lineText = str(prevOffset)
            markerTxt = Fonts.font16.render(lineText, True, Colors.NAVY)
            markerTxtX = linePos+15
            markerTxtY = self.monitorHeight+16 - markerTxt.get_size()[1]/2.0
            pygame.draw.line(self.screen, Colors.NAVY, [linePos, self.monitorHeight], [linePos, self.monitorHeight+20], 1)

            self.screen.blit(markerTxt, (markerTxtX, markerTxtY))

    def updatePlayer(self):
        #the following factors are used to calculate from a distance in meters into a distance on the
        #screen (1m in our simulation is not 1px on the screen, depends on the sceneRange we've got)
        heightFactor = self.racePanelHeight / self.sceneRange

        currentHeight = (self.playerLane + 1) * self.laneHeight * heightFactor + self.monitorHeight
        pos = {"posX": self.width/2 , "posY": currentHeight}
        self.printBoat(pos, "Player", Colors.DARKORANGE, ErgStats.pace)

    def printBoat(self, position, name, color, pace):
        #the following factors are used to calculate from a distance in meters into a distance on the
        #screen (1m in our simulation is not 1px on the screen, depends on the sceneRange we've got)
        heightFactor = self.racePanelHeight / self.sceneRange
        widthFactor = self.width / self.sceneRange

        posX = position["posX"]
        posY = position["posY"]
        #this is how the boat looks:
        boatPolygon = [ [posX-(6 * widthFactor), posY-(1.0 * heightFactor)],
                        [posX-(5 * widthFactor), posY-(1.5 * heightFactor)],
                        [posX-(3 * widthFactor), posY-(1.5 * heightFactor)],
                        [posX, posY],
                        [posX-(3 * widthFactor), posY+(1.5 * heightFactor)],
                        [posX-(5 * widthFactor), posY+(1.5 * heightFactor)],
                        [posX-(6 * widthFactor), posY+(1.0 * heightFactor)]]

        #display the name of each boat on its lane to the left
        nameTxt = Fonts.font32.render(name, True, Colors.NAVY)
        txtX = 10
        txtY = posY - nameTxt.get_size()[1] / 2.0
        self.screen.blit(nameTxt, (txtX, txtY))

        #display the pace of each boat on its lane to the right
        txt = "%.2i:%.2i.%.1i" % (int((pace/60)%60), int((pace)%60), int((pace*10)%10) )
        paceTxt = Fonts.font32.render(str(txt), True, Colors.NAVY)
        txtX = self.width - paceTxt.get_size()[0] - 10
        txtY = posY - paceTxt.get_size()[1] / 2.0
        self.screen.blit(paceTxt, (txtX, txtY))

        #display the boat
        pygame.draw.polygon(self.screen, color, boatPolygon)
        pygame.draw.polygon(self.screen, Colors.BLACK, boatPolygon, 2)

    def updateBoats(self, boats):
        #the following factors are used to calculate from a distance in meters into a distance on the
        #screen (1m in our simulation is not 1px on the screen, depends on the sceneRange we've got)
        heightFactor = self.racePanelHeight / self.sceneRange
        widthFactor = self.width / self.sceneRange

        for index, boat in enumerate(boats):
            #calc the height
            if(index >= self.playerLane):
                index += 1
            currentLane = (index + 1) * self.laneHeight * heightFactor + self.monitorHeight

            #calc the horizontal position
            relativeDistance = boat.distance-ErgStats.distance
            boatPos = relativeDistance * widthFactor + self.width/2

            #print the boat
            pos = {"posX": boatPos, "posY": currentLane }
            self.printBoat(pos, boat.name, Colors.GREEN, boat.pace)

    def registerCallback(self, callback):
        self.callbacks.append(callback)

    def setCycleTime(self, time):
        self.CYCLETIME = time


