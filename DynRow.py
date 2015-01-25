from PyGameUi import PyGameUi
from BoatConstant import BoatConstant
from BoatConcept2 import BoatConcept2
from Playground import Playground

import time

DELTAT = 16  # run with ~60FPS
playground = Playground()  # the playground is a class which holds all the information (all the boats etc)
ui = PyGameUi() # the UI which will display the playground on a graphical interface


def gameLoop(timeGone):
    playground.update(timeGone)
    ui.update(playground, timeGone)

def main():
    # init the player
    player = BoatConcept2("Player")
    # The Concept2-boat needs to get initialized
    # This is a blocking call which only returns after the workout has been started
    player.initialize()
    playground.setPlayerBoat(player)

    #init the boats
    playground.addBoat(BoatConstant("Max Mustermann", 190, 35))
    playground.addBoat(BoatConstant("Jonny Langsam", 500, 24))
    playground.addBoat(BoatConstant("Speedy Gonzales", 120, 22))

    #init the UI, register the GameLoop and run it
    ui.registerCallback(gameLoop)
    ui.setCycleTime(DELTAT)
    ui.run()


if __name__ == "__main__":
    main()

