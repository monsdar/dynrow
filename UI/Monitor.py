
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

    def updateStats(self, playground):
        self.screen.fill(Colors.LIGHTGREY, [[0, 0], [self.width, self.statPanelHeight]])
        pygame.draw.line(self.screen, Colors.BLACK, [0, self.statPanelHeight],[self.width, self.statPanelHeight], 3)

        leftDividerX = (self.width/3)*1
        leftHeightDividerY = self.statPanelHeight / 2.0
        leftSubDividerX = leftDividerX/2.0
        midHeightDivider = self.statPanelHeight / 2.0
        pygame.draw.line(self.screen, Colors.BLACK, [leftDividerX, 0],[leftDividerX, self.statPanelHeight], 1)
        pygame.draw.line(self.screen, Colors.BLACK, [0, leftHeightDividerY],[leftDividerX, leftHeightDividerY], 1)
        pygame.draw.line(self.screen, Colors.BLACK, [leftSubDividerX, leftHeightDividerY],[leftSubDividerX, self.statPanelHeight], 1)

        rightDividerX = (self.width/3)*2
        rightHeightDivider = self.statPanelHeight / 2.0
        pygame.draw.line(self.screen, Colors.BLACK, [rightDividerX, 0],[rightDividerX, self.statPanelHeight], 1)
        pygame.draw.line(self.screen, Colors.BLACK, [rightDividerX, rightHeightDivider],[self.width, rightHeightDivider], 1)

        #display the workout time
        #use the time given by ergometer, it pauses when the player pauses etc
        timeGone = ErgStats.time
        txt = "%.2i:%.2i:%.2i.%.1i" % (int((timeGone/3600)%24), int((timeGone/60)%60), int((timeGone)%60), int((timeGone * 100)%10) )
        timeTxt = Fonts.font72.render(txt, True, Colors.BLACK)
        #NOTE: outcommented the generic approach here because it wasn't in a fixed position (text would jitter left and right)
        #timePosX = leftDividerX/2 - (timeTxt.get_size()[0] / 2.0)
        timePosX = 58
        timePosY = leftHeightDividerY/2.0 - (timeTxt.get_size()[1] / 2.0)
        self.screen.blit(timeTxt, (timePosX, timePosY))

        timeDescTxt = Fonts.font16.render("Workout Time", True, Colors.BLACK)
        timeDescPosX = leftDividerX/2 - (timeDescTxt.get_size()[0]/2.0)
        timeDescPosY = timePosY- 16
        self.screen.blit(timeDescTxt, (timeDescPosX, timeDescPosY))

        #display the strokes per minute
        txt = "%i" % ErgStats.spm
        spmTxt = Fonts.font72.render(txt, True, Colors.BLACK)
        spmPosX = leftSubDividerX/2 - (spmTxt.get_size()[0] / 2.0)
        spmPosY = (leftHeightDividerY + (self.statPanelHeight - leftHeightDividerY)/2.0) - (spmTxt.get_size()[1]/2.0)
        self.screen.blit(spmTxt, (spmPosX, spmPosY))

        spmDescTxt = Fonts.font16.render("Strokes per Minute", True, Colors.BLACK)
        spmDescPosX = leftSubDividerX/2 - (spmDescTxt.get_size()[0]/2.0)
        spmDescPosY = spmPosY- 16
        self.screen.blit(spmDescTxt, (spmDescPosX, spmDescPosY))

        #display the heart rate
        txt = "%i" % ErgStats.heartrate
        pulseTxt = Fonts.font72.render(txt, True, Colors.BLACK)
        pulsePosX = leftSubDividerX + leftSubDividerX/2 - (pulseTxt.get_size()[0] / 2.0)
        pulsePosY = (leftHeightDividerY + (self.statPanelHeight - leftHeightDividerY)/2.0) - (pulseTxt.get_size()[1]/2.0)
        self.screen.blit(pulseTxt, (pulsePosX, pulsePosY))

        pulseDescTxt = Fonts.font16.render("Heart Rate", True, Colors.BLACK)
        pulseDescPosX = leftSubDividerX + leftSubDividerX/2 - (pulseDescTxt.get_size()[0]/2.0)
        pulseDescPosY = pulsePosY- 16
        self.screen.blit(pulseDescTxt, (pulseDescPosX, pulseDescPosY))

        #display the 500m pace
        pace = ErgStats.pace
        txt = "%.2i:%.2i.%.1i" % (int((pace/60)%60), int((pace)%60), int((pace*10)%10) )
        paceTxt = Fonts.font96.render(txt, True, Colors.BLACK)
        #NOTE: outcommented the generic approach here because it wasn't in a fixed position (text would jitter left and right)
        #pacePosX = leftDividerX + leftDividerX/2 - (paceTxt.get_size()[0] / 2.0)
        pacePosX = leftDividerX + 67.0
        pacePosY = midHeightDivider - (paceTxt.get_size()[1])
        self.screen.blit(paceTxt, (pacePosX, pacePosY))

        paceDescTxt = Fonts.font16.render("Pace /500m", True, Colors.BLACK)
        paceDescPosX = leftDividerX + leftDividerX/2 - (paceDescTxt.get_size()[0]/2.0)
        paceDescPosY = pacePosY- 16
        self.screen.blit(paceDescTxt, (paceDescPosX, paceDescPosY))

        #display the avg 500m avgPace
        minutes = int((ErgStats.avgPace/60)%60)
        seconds = int((ErgStats.avgPace)%60)
        millsecs = int(((ErgStats.avgPace*1000)%1000) + 0.000001) #need to add a small value to equalize floating point inconsistencies
        txt = "%.2i:%.2i.%.3i" % (minutes, seconds, millsecs)
        avgPaceTxt = Fonts.font48.render(txt, True, Colors.BLACK)

        #NOTE: outcommented the generic approach here because it wasn't in a fixed position (text would jitter left and right)
        #avgPacePosX = leftDividerX + leftDividerX/2 - (avgPaceTxt.get_size()[0] / 2.0)
        avgPacePosX = leftDividerX + 121.0
        avgPacePosY = midHeightDivider
        self.screen.blit(avgPaceTxt, (avgPacePosX, avgPacePosY))

        avgPaceDescTxt = Fonts.font16.render("Avg Pace /500m", True, Colors.BLACK)
        avgPaceDescPosX = leftDividerX + leftDividerX/2 - (avgPaceDescTxt.get_size()[0]/2.0)
        avgPaceDescPosY = avgPacePosY + avgPaceDescTxt.get_size()[1] + 40
        self.screen.blit(avgPaceDescTxt, (avgPaceDescPosX, avgPaceDescPosY))

        #display the rowed distance
        distTxt = Fonts.font72.render("%im" % ErgStats.distance, True, Colors.BLACK)
        distPosX = rightDividerX + (self.width-rightDividerX)/2 - (distTxt.get_size()[0] / 2.0)
        distPosY = rightHeightDivider + (self.statPanelHeight - rightHeightDivider)/2.0 - (distTxt.get_size()[1]/2.0)
        self.screen.blit(distTxt, (distPosX, distPosY))

        distDescTxt = Fonts.font16.render("Distance", True, Colors.BLACK)
        distDescPosX = rightDividerX + (self.width-rightDividerX)/2 - (distDescTxt.get_size()[0] / 2.0)
        distDescPosY = distPosY- 16
        self.screen.blit(distDescTxt, (distDescPosX, distDescPosY))

        #display the ranking list on the right panel
        orderedBoats = list(playground.boats)             #copy the list, this one will be sorted
        playerBoat = Boat(playground.getPlayerBoat().name, ErgStats.distance) #create a lightweight player-clone to display in this list
        orderedBoats.append(playerBoat)
        orderedBoats.sort()                               #sort the boats to display them ordered by distance

        currentHeight = 0 #this is the offset in height where the list starts
        for index, boat in enumerate(orderedBoats):
            #display position and name
            txt = "%i - %s" % (index+1, boat.name)
            boatNameTxt = Fonts.font32.render(txt, True, Colors.BLACK)
            boatNamePosX = rightDividerX + 16
            boatNamePosY = currentHeight
            self.screen.blit(boatNameTxt, (boatNamePosX, boatNamePosY))

            #display delta to player distance
            if not(boat.distance - ErgStats.distance == 0):
                txt = "%+im" % (boat.distance - ErgStats.distance)
                boatRelDistTxt = Fonts.font32.render(txt, True, Colors.BLACK)
                boatRelDistPosX = self.width - 32 - boatRelDistTxt.get_size()[0]
                boatRelDistPosY = currentHeight + 4
                self.screen.blit(boatRelDistTxt, (boatRelDistPosX, boatRelDistPosY))

            currentHeight += boatNameTxt.get_size()[1]




