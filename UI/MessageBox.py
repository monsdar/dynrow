
import pygame

import Colors
import Fonts

class MessageBox:
    def __init__(self, screenHandle, width, height):
        self.screen = screenHandle
        self.width = width
        self.height = height

    def renderText(self, text):
        renderedText = Fonts.font48.render(text, True, Colors.BLACK)
        posX = self.width/2.0 - renderedText.get_size()[0] / 2.0
        posY = self.height/2.0 - renderedText.get_size()[1] / 2.0
        self.screen.blit(renderedText, (posX, posY))

    def renderBackground(self):
        #fill the background
        topLeftX = (self.width / 2.0) - ((self.width / 2.0) / 2.0)
        topLeftY = (self.height / 2.0) - ((self.height / 2.0) / 2.0)
        sizeX = 2.0 * topLeftX
        sizeY = 2.0 * topLeftY
        self.screen.fill(Colors.STEELBLUE, [[topLeftX, topLeftY], [sizeX, sizeY]])

        #outer boundary
        bottomRightX = topLeftX + sizeX
        bottomRightY = topLeftY + sizeY
        pygame.draw.line(self.screen, Colors.BLACK, [topLeftX, topLeftY],[topLeftX, bottomRightY], 3)
        pygame.draw.line(self.screen, Colors.BLACK, [topLeftX, topLeftY],[bottomRightX, topLeftY], 3)
        pygame.draw.line(self.screen, Colors.BLACK, [bottomRightX, bottomRightY],[topLeftX, bottomRightY], 3)
        pygame.draw.line(self.screen, Colors.BLACK, [bottomRightX, bottomRightY],[bottomRightX, topLeftY], 3)

        #inner boundary
        topLeftX += 3
        topLeftY += 3
        bottomRightX -= 3
        bottomRightY -= 3
        pygame.draw.line(self.screen, Colors.BLACK, [topLeftX, topLeftY],[topLeftX, bottomRightY], 1)
        pygame.draw.line(self.screen, Colors.BLACK, [topLeftX, topLeftY],[bottomRightX, topLeftY], 1)
        pygame.draw.line(self.screen, Colors.BLACK, [bottomRightX, bottomRightY],[topLeftX, bottomRightY], 1)
        pygame.draw.line(self.screen, Colors.BLACK, [bottomRightX, bottomRightY],[bottomRightX, topLeftY], 1)

    def renderMessage(self, text):
        self.renderBackground()
        self.renderText(text)


