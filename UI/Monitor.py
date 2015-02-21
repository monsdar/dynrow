
import pygame

import Colors
import Fonts

from PyRow.ErgStats import ErgStats
from Logic.Boat import Boat

class Monitor:
    def __init__(self, screenHandle, width, height):
        self.screen = screenHandle
        self.statPanelHeight = height
        self.width = width

        self.leftDividerX = (self.width/3)*1
        self.leftHeightDividerY = self.statPanelHeight / 2.0
        self.leftSubDividerX = self.leftDividerX/2.0
        self.midHeightDivider = self.statPanelHeight / 2.0
        self.rightDividerX = (self.width/3)*2
        self.rightHeightDivider = self.statPanelHeight / 2.0

    '''
    This method updates the ranking in the top right corner
    Incoming list won't get resorted, items will displayed in the incoming order
    Items with a distance of ErgStats.distance won't get their distance displayed
    Currently the max number of names is 4, every item more won't be painted in the right section anymore
     Input: List of Tuples: [(Name, Distance), (..., ...), ...]
     Example: [("Max", 30), ("Player", 15), ("Testy", 15), ("John", 5)]
     Result:    1 Max     +15
                2 Player
                3 Testy
                4 John    -10
    '''
    def updateRanking(self, givenRanking):
        currentHeight = 0 #this is the offset in height where the list starts
        for index, boat in enumerate(givenRanking):
            #display position and name
            txt = "%i - %s" % (index+1, boat[0])
            boatNameTxt = Fonts.font32.render(txt, True, Colors.BLACK)
            boatNamePosX = self.rightDividerX + 16
            boatNamePosY = currentHeight
            self.screen.blit(boatNameTxt, (boatNamePosX, boatNamePosY))

            #display delta to player distance
            if not(boat[1] - ErgStats.distance == 0):
                txt = "%+im" % (boat[1] - ErgStats.distance)
                boatRelDistTxt = Fonts.font32.render(txt, True, Colors.BLACK)
                boatRelDistPosX = self.width - 32 - boatRelDistTxt.get_size()[0]
                boatRelDistPosY = currentHeight + 4
                self.screen.blit(boatRelDistTxt, (boatRelDistPosX, boatRelDistPosY))

            currentHeight += boatNameTxt.get_size()[1]

    '''
    Draws the grey background and all the needed lines
    '''
    def drawBackground(self):
        self.screen.fill(Colors.LIGHTGREY, [[0, 0], [self.width, self.statPanelHeight]])
        pygame.draw.line(self.screen, Colors.BLACK, [0, self.statPanelHeight],[self.width, self.statPanelHeight], 3)
        pygame.draw.line(self.screen, Colors.BLACK, [self.leftDividerX, 0],[self.leftDividerX, self.statPanelHeight], 1)
        pygame.draw.line(self.screen, Colors.BLACK, [0, self.leftHeightDividerY],[self.leftDividerX, self.leftHeightDividerY], 1)
        pygame.draw.line(self.screen, Colors.BLACK, [self.leftSubDividerX, self.leftHeightDividerY],[self.leftSubDividerX, self.statPanelHeight], 1)
        pygame.draw.line(self.screen, Colors.BLACK, [self.rightDividerX, 0],[self.rightDividerX, self.statPanelHeight], 1)
        pygame.draw.line(self.screen, Colors.BLACK, [self.rightDividerX, self.rightHeightDivider],[self.width, self.rightHeightDivider], 1)


    '''
    Returns the string to a given time

    Input: Time in seconds. Use floating point to use a higher precision than seconds
    Output: String in the Format mm:ss.n (n being the first decimal place)
            Enabling withHour adds hh: in front
            Changing decDigits controls how many decimal places after second will be displayed
    '''
    def getTimeStr(self, timeInSec, withHour=False, decDigits=1,):
        resultStr = ""

        if withHour:
            resultStr += "%.2i:" % int((timeInSec/3600)%24)

        #add minutes
        resultStr += "%.2i:" % int((timeInSec/60)%60)
        #add the seconds
        resultStr += "%.2i" % int((timeInSec)%60)
        #add the micsecs (some additional calc is needed to generate different decDigits
        micStr = ".%." + str(decDigits) + "i"
        micBase = pow(10, decDigits)
        mics = timeInSec * (pow(10, decDigits))
        resultStr += micStr % int( mics % micBase )

        return resultStr

    def updateStats(self, playground):

        self.drawBackground()

        #display the workout time
        #use the time given by ergometer, it pauses when the player pauses etc
        txt = self.getTimeStr(ErgStats.time, withHour=True)
        timeTxt = Fonts.font72.render(txt, True, Colors.BLACK)
        #NOTE: outcommented the generic approach here because it wasn't in a fixed position (text would jitter left and right)
        #timePosX = leftDividerX/2 - (timeTxt.get_size()[0] / 2.0)
        timePosX = 58
        timePosY = self.leftHeightDividerY/2.0 - (timeTxt.get_size()[1] / 2.0)
        self.screen.blit(timeTxt, (timePosX, timePosY))

        timeDescTxt = Fonts.font16.render("Workout Time", True, Colors.BLACK)
        timeDescPosX = self.leftDividerX/2 - (timeDescTxt.get_size()[0]/2.0)
        timeDescPosY = timePosY- 16
        self.screen.blit(timeDescTxt, (timeDescPosX, timeDescPosY))

        #display the strokes per minute
        txt = "%i" % ErgStats.spm
        spmTxt = Fonts.font72.render(txt, True, Colors.BLACK)
        spmPosX = self.leftSubDividerX/2 - (spmTxt.get_size()[0] / 2.0)
        spmPosY = (self.leftHeightDividerY + (self.statPanelHeight - self.leftHeightDividerY)/2.0) - (spmTxt.get_size()[1]/2.0)
        self.screen.blit(spmTxt, (spmPosX, spmPosY))

        spmDescTxt = Fonts.font16.render("Strokes per Minute", True, Colors.BLACK)
        spmDescPosX = self.leftSubDividerX/2 - (spmDescTxt.get_size()[0]/2.0)
        spmDescPosY = spmPosY- 16
        self.screen.blit(spmDescTxt, (spmDescPosX, spmDescPosY))

        #display the heart rate
        txt = "%i" % ErgStats.heartrate
        pulseTxt = Fonts.font72.render(txt, True, Colors.BLACK)
        pulsePosX = self.leftSubDividerX + self.leftSubDividerX/2 - (pulseTxt.get_size()[0] / 2.0)
        pulsePosY = (self.leftHeightDividerY + (self.statPanelHeight - self.leftHeightDividerY)/2.0) - (pulseTxt.get_size()[1]/2.0)
        self.screen.blit(pulseTxt, (pulsePosX, pulsePosY))

        pulseDescTxt = Fonts.font16.render("Heart Rate", True, Colors.BLACK)
        pulseDescPosX = self.leftSubDividerX + self.leftSubDividerX/2 - (pulseDescTxt.get_size()[0]/2.0)
        pulseDescPosY = pulsePosY- 16
        self.screen.blit(pulseDescTxt, (pulseDescPosX, pulseDescPosY))

        #display the 500m pace
        txt = self.getTimeStr(ErgStats.pace)
        paceTxt = Fonts.font96.render(txt, True, Colors.BLACK)
        #NOTE: outcommented the generic approach here because it wasn't in a fixed position (text would jitter left and right)
        #pacePosX = leftDividerX + leftDividerX/2 - (paceTxt.get_size()[0] / 2.0)
        pacePosX = self.leftDividerX + 67.0
        pacePosY = self.midHeightDivider - (paceTxt.get_size()[1])
        self.screen.blit(paceTxt, (pacePosX, pacePosY))

        paceDescTxt = Fonts.font16.render("Pace /500m", True, Colors.BLACK)
        paceDescPosX = self.leftDividerX + self.leftDividerX/2 - (paceDescTxt.get_size()[0]/2.0)
        paceDescPosY = pacePosY- 16
        self.screen.blit(paceDescTxt, (paceDescPosX, paceDescPosY))

        #display the avg 500m avgPace
        txt = self.getTimeStr(ErgStats.avgPace + 0.000001, decDigits=3 ) #need to add a small value to equalize floating point inconsistencies
        avgPaceTxt = Fonts.font48.render(txt, True, Colors.BLACK)

        #NOTE: outcommented the generic approach here because it wasn't in a fixed position (text would jitter left and right)
        #avgPacePosX = leftDividerX + leftDividerX/2 - (avgPaceTxt.get_size()[0] / 2.0)
        avgPacePosX = self.leftDividerX + 121.0
        avgPacePosY = self.midHeightDivider
        self.screen.blit(avgPaceTxt, (avgPacePosX, avgPacePosY))

        avgPaceDescTxt = Fonts.font16.render("Avg Pace /500m", True, Colors.BLACK)
        avgPaceDescPosX = self.leftDividerX + self.leftDividerX/2 - (avgPaceDescTxt.get_size()[0]/2.0)
        avgPaceDescPosY = avgPacePosY + avgPaceDescTxt.get_size()[1] + 40
        self.screen.blit(avgPaceDescTxt, (avgPaceDescPosX, avgPaceDescPosY))

        #display the rowed distance
        distTxt = Fonts.font72.render("%im" % ErgStats.distance, True, Colors.BLACK)
        distPosX = self.rightDividerX + (self.width-self.rightDividerX)/2 - (distTxt.get_size()[0] / 2.0)
        distPosY = self.rightHeightDivider + (self.statPanelHeight - self.rightHeightDivider)/2.0 - (distTxt.get_size()[1]/2.0)
        self.screen.blit(distTxt, (distPosX, distPosY))

        distDescTxt = Fonts.font16.render("Distance", True, Colors.BLACK)
        distDescPosX = self.rightDividerX + (self.width-self.rightDividerX)/2 - (distDescTxt.get_size()[0] / 2.0)
        distDescPosY = distPosY- 16
        self.screen.blit(distDescTxt, (distDescPosX, distDescPosY))

        #display the ranking, therefore get the actual boat-tuples needed
        orderedBoats = list(playground.boats)             #copy the list, this one will be sorted
        playerBoat = Boat(playground.getPlayerBoat().name, ErgStats.distance) #create a lightweight player-clone to display in this list
        orderedBoats.append(playerBoat)
        orderedBoats.sort()                               #sort the boats to display them ordered by distance

        ranking = []
        for boat in orderedBoats:
            ranking.append( (boat.name, boat.distance) )
        self.updateRanking(ranking)





