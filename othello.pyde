# This files sets up the initial screensize,
# and passes this information to the GameController, which handles the rest.

from game_controller import GameController

SCREEN_SIZE = 800
SCOREBOARD_SIZE = 200
GRID_SIZE = 100

gc = GameController(SCREEN_SIZE, GRID_SIZE)


def setup():

    # Sets up a screen withthe board on top and the scoreboard on bottom
    size(SCREEN_SIZE, SCREEN_SIZE + SCOREBOARD_SIZE)

    # Sets up the initial four chips of the game
    gc.initial_chips()

    # Asks for a name from the user for high-score tracking
    answer = input('enter your name')
    gc.player_name = str(answer)


def draw():

    gc.display()


def mousePressed():

    # Sets up the coordinates of the spaces of the board
    column_coord = mouseX/GRID_SIZE
    row_coord = mouseY/GRID_SIZE

    # As long as the click is within the game board
    # (i.e. not on the scoreboard)
    if row_coord <= 7:
        gc.update(column_coord, row_coord)


def input(message=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)
