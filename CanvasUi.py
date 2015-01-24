
from Tkinter import *
from datetime import datetime

class CanvasUi():
    def __init__(self):
        # width and height of the window
        self.width = 800
        self.height = 600

        # the distance in meters which will be drawn
        self.sceneRange = 100
        self.sceneStartOffset = -(self.sceneRange/2) #where the scene starts
        self.sceneEndOffset = self.sceneRange #where the scene ends (put in a bit more meters than necessary)

        self.laneWidth = 10 # the steps where the distance will be shown
        self.laneWidthBig = 50 #the steps where more special marks are used to show the distance
        self.laneHeight = 50 # the height between the lanes

        self.cycleTime = 10
        self.currentDistance = 0.0
        self.canvasElements = []

        self.callbacks = []
        self.starttime = 0
        
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg='light steel blue')
        self.canvas.pack()

        #these attributes are needed to calc the FPS
        self.MAXTICKSAMPLES = 100
        self.tickIndex = 0
        self.tickSum = 0.0
        self.tickList = []
        for index in range(0,self.MAXTICKSAMPLES):
            self.tickList.append(0.0)
        self.tickStamp = datetime.now().second * 1000 + datetime.now().microsecond / 1000.0

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
        self.cycle()
        self.root.mainloop()
            
    def updateBackground(self, distance):
        #remove the previous drawn items (until I figure out a way to just update them instead of recreating them each update)
        for element in self.canvasElements:
            self.canvas.delete(element)
        del self.canvasElements[:]
        
        #this defines the start and end of the scene
        sceneStart = distance + self.sceneStartOffset
        sceneEnd = distance + self.sceneEndOffset

        #print the horizontal lines
        for y in range(0, self.height, self.laneHeight):
            #the offset is needed to "move" the dashed lines along with the rest of the scenery
            offset = (distance%self.sceneRange) * (self.width / self.sceneRange)
            self.canvasElements.append( self.canvas.create_line(0 - offset, y + self.laneHeight/2, self.width, y + self.laneHeight/2, fill="steel blue", dash=(1,1)) )

        for lineStep in range(int(sceneStart), int(sceneEnd), self.laneWidth):
            prevOffset = lineStep - (lineStep % self.laneWidth) #get the previous dividable laneWidth-step
            linePos = (prevOffset - sceneStart) * (self.width / self.sceneRange) #get the position and project the window size

            #create the actual marker
            for heightPos in range(0, self.height, self.laneHeight):
                if(prevOffset % self.laneWidthBig == 0):
                    self.canvasElements.append( self.canvas.create_oval(linePos-4, heightPos-4 + self.laneHeight/2, linePos+4, heightPos+4 + self.laneHeight/2, fill="firebrick") )
                else:
                    self.canvasElements.append( self.canvas.create_oval(linePos-2, heightPos-2 + self.laneHeight/2, linePos+2, heightPos+2 + self.laneHeight/2, fill="light grey") )

            
            #display the distance marker
            lineText = str(prevOffset)
            self.canvasElements.append( self.canvas.create_line(linePos, 0, linePos, 20, fill="navy") )
            self.canvasElements.append( self.canvas.create_text(linePos+15, 8, text=lineText, fill="navy") )
            
    def updatePlayer(self, distance):
        pos = {"posX": self.width/2, "posY": self.height/2}
        self.printBoat(pos, distance, "dark orange")
        
    def printBoat(self, position, distance, color):
        posX = position["posX"]
        posY = position["posY"]
        #the following polygon is calculated with offsets in metres, the offset than is multiplied to
        #match the current projection and windows size
        boatPolygon = [ posX-(8 * self.width / self.sceneRange), posY,
                        posX-(4 * self.width / self.sceneRange), posY-(1 * self.width / self.sceneRange),
                        posX, posY,
                        posX-(4 * self.width / self.sceneRange), posY+(1 * self.width / self.sceneRange)]

        #display the distance of each boat next to it
        distText = "%.2fm" % distance
        self.canvasElements.append( self.canvas.create_polygon(boatPolygon, outline='black', fill=color))
        self.canvasElements.append( self.canvas.create_text(posX-(12 * self.width / self.sceneRange), posY, text=distText, fill="navy") )
    
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
            self.printBoat(pos, boat.distance, "green")
        
    def registerCallback(self, callback):
        self.callbacks.append(callback)
        
    def setCycleTime(self, time):
        self.cycleTime = time

    def update(self, playground):
        #Get the current distance from the player boat
        self.currentDistance = playground.getPlayerBoat().distance
        
        #update the distlanes according to the distance
        self.updateBackground(self.currentDistance)
        self.updatePlayer(self.currentDistance)
        self.updateBoats(playground.boats)

        #display the current FPS in the title
        currentTickStamp = datetime.now().second * 1000 + datetime.now().microsecond / 1000.0
        if(currentTickStamp > self.tickStamp):
            deltaT = currentTickStamp - self.tickStamp
            self.root.wm_title( "%3.2f FPS" % self.calcFps(deltaT) )
        self.tickStamp = currentTickStamp

    def cycle(self):
        #if time hasn't been set yet do it now
        if(self.starttime == 0):
            curr = datetime.now()
            self.starttime = curr.day * 24*60*1000*1000 + curr.hour * 60*1000*1000 + curr.minute*60*1000 + curr.second*1000 + curr.microsecond / 1000

        #calc how much time has been gone
        curr = datetime.now()
        currTime = curr.day * 24*60*1000*1000 + curr.hour * 60*1000*1000 + curr.minute*60*1000 + curr.second*1000 + curr.microsecond / 1000
        timeGone = currTime - self.starttime

        for cb in self.callbacks:
            cb(timeGone)
        
        self.root.after(self.cycleTime, self.cycle)