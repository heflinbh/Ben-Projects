# The gameboard itself.
# Keeps track of the total number of spaces, and also defines the corner
# and peremeter spaces.
class Grid():

    def __init__(self, width, tiles_per_row):

        self.width = width
        self.tiles_per_row = tiles_per_row
        self.num_tiles = tiles_per_row * tiles_per_row

        self.tiles = [_ for _ in range(self.tiles_per_row)]

        # These spaces are particularly important in Othello. The computer
        # player uses these to make prioritized decisions.
        TR_SPACE = (0, 0)
        TL_SPACE = (0, 7)
        BR_SPACE = (7, 0)
        BL_SPACE = (7, 7)

        LEFT_1 = (0, 1)
        LEFT_2 = (0, 2)
        LEFT_3 = (0, 3)
        LEFT_4 = (0, 4)
        LEFT_5 = (0, 5)
        LEFT_6 = (0, 6)

        RIGHT_1 = (7, 1)
        RIGHT_2 = (7, 2)
        RIGHT_3 = (7, 3)
        RIGHT_4 = (7, 4)
        RIGHT_5 = (7, 5)
        RIGHT_6 = (7, 6)

        TOP_1 = (1, 0)
        TOP_2 = (2, 0)
        TOP_3 = (3, 0)
        TOP_4 = (4, 0)
        TOP_5 = (5, 0)
        TOP_6 = (6, 0)

        BOTTOM_1 = (1, 7)
        BOTTOM_2 = (2, 7)
        BOTTOM_3 = (3, 7)
        BOTTOM_4 = (4, 7)
        BOTTOM_5 = (5, 7)
        BOTTOM_6 = (6, 7)

        self.corner_spaces = [TR_SPACE, TL_SPACE, BR_SPACE, BL_SPACE]

        self.peremeter_spaces = [
            LEFT_1, LEFT_2, LEFT_3, LEFT_4, LEFT_5, LEFT_6,
            RIGHT_1, RIGHT_2, RIGHT_3, RIGHT_4, RIGHT_5, RIGHT_6,
            TOP_1, TOP_2, TOP_3, TOP_4, TOP_5, TOP_6,
            BOTTOM_1, BOTTOM_2, BOTTOM_3, BOTTOM_4, BOTTOM_5, BOTTOM_6
                                                                      ]

    # Displaying of the board. The "x" and "y" coorespond to coordinates of
    # the board, from the top-left to bottom-right.
    def display(self):

        x, y = 0, 0

        for row in self.tiles:
            for col in self.tiles:

                fill(34, 139, 34)
                rect(x, y, self.width, self.width)
                x += self.width

            y += self.width
            x = 0

        fill(100, 100, 100)
        rect(0, 800, 800, 200)
