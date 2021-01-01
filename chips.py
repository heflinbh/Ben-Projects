from chip import Chip

# Keeps track of the collecton of chips, and also defines their relationships
# (i.e. which direction they are in relation to each other)


class Chips():

    def __init__(self, num_columns, num_rows):

        self.columns = num_columns
        self.rows = num_rows

        self.chips_list = []

        # The board is an even number of spaces wide and tall.
        # Therefore, the starting positon is on the top left portion of this
        # middle square.
        # num / 2 gives the center, and the -1 gives the left/top side
        self.starting_chip_x = num_columns / 2 - 1
        self.starting_chip_y = num_rows / 2 - 1

        DIR_NN = (0, -1)
        DIR_NW = (-1, -1)
        DIR_NE = (1, -1)

        DIR_WW = (-1, 0)
        DIR_EE = (1, 0)

        DIR_SS = (0, 1)
        DIR_SW = (-1, 1)
        DIR_SE = (1, 1)

        self.directions_list = [DIR_NN, DIR_NW, DIR_NE,
                                DIR_WW, DIR_EE,
                                DIR_SS, DIR_SW, DIR_SE]

    def display_chips(self):

        for chip in self.chips_list:

            # Chips have atribtutes "is_white" and "color"
            # "is_white" defines who has contol of the chip.
            # "color" determines the display setting.
            # In this way, we can have chips "fade" into
            # another color when they flip.
            if chip.is_white and chip.color < 255:
                chip.color += 2
                if chip.color == 254:
                    chip.color = 255

            elif not(chip.is_white) and chip.color > 0:
                chip.color -= 2
                if chip.color == 1:
                    chip.color = 0

            chip.display()

    # Sets up the inital four chips, and changes two of their colors to make
    # the correct starting position for each player.
    def initial_chips(self):

        IS_WHITE = True

        for row in range(self.rows / 4):
            for column in range(self.columns / 4):

                start_chip = Chip(IS_WHITE,
                                  self.starting_chip_x, self.starting_chip_y)
                self.chips_list.append(start_chip)

                self.starting_chip_x += 1

            self.starting_chip_x = self.columns / 2 - 1
            self.starting_chip_y += 1

        self.chips_list[1].change_color()
        self.chips_list[1].color = 0
        self.chips_list[2].change_color()
        self.chips_list[2].color = 0

    def add_chip(self, is_white, column, row):

        new_chip = Chip(is_white, column, row)
        self.chips_list.append(new_chip)

    # Changes the chip's color when it is captured
    def flip_chips(self):

        # Takes the last chip made
        new_chip = self.chips_list[-1]

        # Looks in each of the eight possible directions
        for direction in self.directions_list:
            flip_list = []

            # Find a chip that is both in that direction
            # and of the opposite color
            for chip in self.chips_list:
                if (chip.column == new_chip.column + direction[0]
                    and chip.row == new_chip.row + direction[1]
                        and chip.is_white is not new_chip.is_white):

                    flip_list.append(chip)

                    # If an enemy chip was found in that direction, keep
                    # looking in that direction
                    pos_x = chip.column + direction[0]
                    pos_y = chip.row + direction[1]

                    blank = False

                    # As long as we're still on the board,
                    # and we haven't met a blank space...
                    while (0 <= pos_x <= 7
                            and 0 <= pos_y <= 7
                            and blank is False):

                        blank = True

                        # Look at all the chips again and find
                        # the next chip in our direction
                        for line_chip in self.chips_list:
                            if (line_chip.column == pos_x
                               and line_chip.row == pos_y):

                                # Add that chip to out flip list
                                flip_list.append(line_chip)

                                # If we found a chip with our "for" loop, then
                                # it could not be a blank space. Therefore,
                                # continue the "while" loop.
                                blank = False

                        # Look in the next spot in our direction
                        pos_x += direction[0]
                        pos_y += direction[1]

            # After finding all the chips in that direction, check their colors
            end_flips = True

            # We flip chips in this direction unitl we find one of our color.
            # T hat's when we stop and do the same thing in a different
            # direction.
            for check_chip in flip_list:
                if check_chip.is_white is new_chip.is_white:
                    end_flips = False

            for flip_chip in flip_list:
                if end_flips is False:
                    if flip_chip.is_white is not new_chip.is_white:
                        flip_chip.change_color()
                    else:
                        end_flips = True
