# An individual chip
# Has attributes for location (coordinates)
# and also for "is_white" and "color."
# "is_white" defines who has contol of the chip.
# "color" determines the display setting.

class Chip():

    def __init__(self, is_white, column, row):

        self.is_white = is_white

        if self.is_white is True:
            self.color = 255
        else:
            self.color = 0

        self.column = column
        self.row = row

        self.SIZE = 90

    def display(self):

        GRID_SIZE = 100

        fill(self.color)
        ellipse(self.column * GRID_SIZE + GRID_SIZE / 2,
                self.row * GRID_SIZE + GRID_SIZE / 2, self.SIZE, self.SIZE)

    def change_color(self):

        self.is_white = not(self.is_white)
