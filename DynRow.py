from UI.PyGameUi import PyGameUi
from Boats.BoatConstant import BoatConstant
from Boats.BoatConcept2 import BoatConcept2
from Boats.BoatBoomerang import BoatBoomerang
from Logic.Playground import Playground
from PyRow.ErgStats import ErgStats

DELTAT = 16  # run with ~60FPS
playground = Playground()  # the playground is a class which holds all the information (all the boats etc)
ui = PyGameUi() # the UI which will display the playground on a graphical interface


def gameLoop(timeGone):
    playground.update(timeGone)
    ui.update(playground)

def main():
    # The Concept2-boat needs to get initialized
    # This is a blocking call which only returns after the workout has been started
    ErgStats.initialize()

    # init the player boat
    player = BoatConcept2("Nils")
    playground.setPlayerBoat(player)

    #init the other boats
    playground.addBoat(BoatBoomerang("Armin", 130, 20, 20))
    playground.addBoat(BoatBoomerang("Bahne", 135, 22, 20))
    playground.addBoat(BoatBoomerang("Matthias", 140, 26, 20))

    #init the UI, register the GameLoop and run it
    ui.registerCallback(gameLoop)
    ui.setCycleTime(DELTAT)
    ui.run()


if __name__ == "__main__":
    main()

