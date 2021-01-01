from chips import Chips
from grid import Grid
import random

# Runs the game, controls the rules, and plays as the computer


class GameController():

    def __init__(self, SCREEN_SIZE, GRID_SIZE):

        self.player_name = ""

        self.GRID_SIZE = GRID_SIZE
        self.SCREEN_SIZE = SCREEN_SIZE

        self.spaces_per_row = SCREEN_SIZE / GRID_SIZE
        self.num_spaces = (SCREEN_SIZE / GRID_SIZE)**2

        self.grid = Grid(GRID_SIZE, self.spaces_per_row)
        self.chips = Chips(self.spaces_per_row, self.spaces_per_row)

        self.is_white_turn = False

        self.white_count = 2
        self.black_count = 2

        self.winner = None

        WAIT_SEC = 3
        self.FPS = 60
        self.timer = WAIT_SEC * self.FPS

        self.valid_move_list = []

        # Since the computer constanty checks if it's its turn in the display
        # method, this self.stop just acts as a switch that turns off
        # immediately during the first iteration of the computer's turn.
        self.stop = True

        # Counts how many times the turn has changed automatically, i.e. when
        # there are no moves for one player.
        # If both players cannot move, then the counter == 2,
        # and the game ends.
        self.change_turn_counter = 0

    def initial_chips(self):
        self.chips.initial_chips()

    def display(self):

        # A timer that goes down once per frame. Keeps players from playing
        # instantaneously (including the computer)
        self.timer -= 1

        self.grid.display()
        self.chips.display_chips()

        # If a winner has been decided, then display the winner
        if self.winner is not None:
            self.declare_winner()

        self.scoreboard()

        # The computer is always check if it is its turn. Several switches are
        # put in place to make sure it moves only when it is valid.
        self.computer_turn()

    def update(self, column, row):

        # Players can only go after waiting some seconds
        if self.timer <= 0:
            self.take_turn(column, row)

    def take_turn(self, column, row):

        # Checks if the clicked space is occupied
        space_occupied = self.check_if_occupied(column, row)
        # And if the move would flip a chip
        valid_move = self.is_valid_move(column, row)

        if space_occupied is False and valid_move is True:

            # Reset the counter, because someone made a move
            self.change_turn_counter = 0

            # Make the move and flip the chips
            self.add_chip(column, row)
            self.flip_chips()

            # Chance the turn and reset the move timer
            self.is_white_turn = not(self.is_white_turn)
            self.timer = 3*60

            # Before the next player moves, check that valid moves exist.
            # If they don't, that player's turn will be skipped
            self.valid_moves_exist()

            # After each turn, check it there is a winner
            self.keep_score()
            self.check_if_winner()
            if self.winner is not None:
                self.track_high_scores()

        # Another switch for the computer, in case it takes two turns in a row.
        # Don't want them both to be taken simultaneously.
        if self.is_white_turn:
            self.stop = False
        else:
            self.stop = True

    def valid_moves_exist(self):

        valid = False
        self.valid_move_list = []

        # Goes through all possible spaces and makes a list
        # of which ones are valid.
        for columns in range(self.spaces_per_row):
            for rows in range(self.spaces_per_row):

                occu = self.check_if_occupied(columns, rows)
                if occu is False:
                    check = self.is_valid_move(columns, rows)
                    if check is True:
                        valid = True
                        self.valid_move_list.append((columns, rows))

        # If there are no valid spaces, then skip the player's turn
        if valid is False:
            self.is_white_turn = not(self.is_white_turn)
            self.timer = 3*60
            self.change_turn_counter += 1

            # This is a recursion, but it only happen twice at maximum.
            # If one player's turn is skipped, make sure the next player has
            # valid moves.
            # As long as the turn does not change twice in a row, we can
            # continue playing
            if self.change_turn_counter < 2:
                self.valid_moves_exist()

    def check_if_occupied(self, column, row):

        space_occupied = False

        for chip in self.chips.chips_list:
            if chip.column == column and chip.row == row:
                space_occupied = True

        return space_occupied

    def is_valid_move(self, column, row):

        # Checks if a particular space is a valid move for a player

        # From every chip, look in every direction
        for direction in self.chips.directions_list:
            for chip in self.chips.chips_list:

                # If we find a chip of the opposite color that is adjacent
                # to our prospective move...
                if (column + direction[0] == chip.column
                    and row + direction[1] == chip.row
                        and chip.is_white is not self.is_white_turn):

                    # Keep looking in that direction...
                    pos_x = chip.column + direction[0]
                    pos_y = chip.row + direction[1]

                    # For as long as we remain on the board...
                    while 0 <= pos_x <= 7 and 0 <= pos_x <= 7:

                        found_chip = False

                        # Go through the list of chips again and look for a
                        # chip continuing in our direction
                        for line_chip in self.chips.chips_list:
                            if (line_chip.column == pos_x
                               and line_chip.row == pos_y):

                                # If we find a chip...
                                found_chip = True
                                # And the chip is our color
                                if line_chip.is_white is self.is_white_turn:
                                    # Then it is a good move
                                    return True
                                else:
                                    pos_x += direction[0]
                                    pos_y += direction[1]
                                    # Increment the direction and
                                    # restart while loop (end the for loop)
                                    break

                        # If we did not find a chip at a certain position,
                        # t hen that means that space is blank.
                        # In that case, this direction is hopeless, and we
                        # must look in another direction
                        if found_chip is False:
                            break
                            # Out of the while Loop and back to the top
                            # with our directions

        # If after all directions we found nothing, then this space is not
        # a valid move
        return False

    def computer_turn(self):

        # As long as our various switches/counters are valid...
        if (self.is_white_turn
            and self.stop is False
                and self.timer < -60
                and self.change_turn_counter < 2):

            # Immediately turn on "stop" so that we only run this method once
            self.stop = True

            # As long as there are valid moves
            if len(self.valid_move_list) > 0:

                # Choose a random move
                move = random.choice(self.valid_move_list)

                # Unless we can choose a peremeter space
                for peremeter_space in self.grid.peremeter_spaces:
                    if peremeter_space in self.valid_move_list:
                        move = peremeter_space

                # Or even better, a corner space
                for corner_space in self.grid.corner_spaces:
                    if corner_space in self.valid_move_list:
                        move = corner_space

                self.take_turn(*move)

        # If nobody has a valid move, end the game
        elif self.change_turn_counter > 5:
            self.check_if_winner()

    def add_chip(self, column, row):
        self.chips.add_chip(self.is_white_turn, column, row)

    def flip_chips(self):
        self.chips.flip_chips()

    def keep_score(self):

        white_count = 0
        black_count = 0

        for chip in self.chips.chips_list:
            if chip.is_white is True:
                white_count += 1
            else:
                black_count += 1

        self.white_count = white_count
        self.black_count = black_count
        self.total_count = white_count + black_count

    # Decideds if there is a winner
    def check_if_winner(self):

        if (self.total_count == self.num_spaces
            or self.change_turn_counter >= 2
            or self.black_count == 0
                or self.white_count == 0):

            if self.white_count > self.black_count:
                self.winner = "White"
            elif self.white_count < self.black_count:
                self.winner = "Black"
            else:
                self.winner = "Draw"

    # If there is a winner, then shout it from the mountaintop!
    def declare_winner(self):

        if self.winner == "Draw":
            declaration = "Draw"
        else:
            declaration = self.winner + " Wins!"

        fill(0, 0, 255)
        textSize(100)
        textAlign(CENTER)
        text(declaration, 400, 900)

    # Runs the scoreboard, displays details on turns and whatnot
    def scoreboard(self):

        if self.winner is None:

            countdown = self.timer / self.FPS + 1

            fill(0, 0, 255)
            textSize(70)
            textAlign(CENTER)

            if countdown > 0:
                if self.is_white_turn:
                    text("White's Turn In " + str(countdown) + "...", 400, 900)
                else:
                    text("Black's Turn In " + str(countdown) + "...", 400, 900)

            else:
                if self.is_white_turn:
                    text("White's Turn", 400, 900)
                else:
                    text("Black's Turn", 400, 900)

        fill(0, 0, 0)
        textSize(40)
        textAlign(LEFT)
        text("Black: " + str(self.black_count), 0, 975)

        fill(255, 255, 255)
        textSize(40)
        textAlign(RIGHT)
        text("White: " + str(self.white_count), 800, 975)

    # Takes the player's name. If it was a high score, the name goes at the
    # top. If not, goes to the bottom
    def track_high_scores(self):

        score_list = []

        with open("scores.txt", "r") as file:
            file_contents = file.readlines()

        header = file_contents[0] + "\n\n"
        file_contents = file_contents[3:]

        for line in file_contents:

            score_list.append(line)

        high_score = True
        for player in score_list:

            score_start = player.rindex(":")
            score = player[score_start+1:]
            score.strip()
            score = int(score)

            if self.black_count < score:
                high_score = False

        if high_score is True:
            score_list.insert(0, str(self.player_name) + ": "
                                                       + str(self.black_count)
                                                       + "\n")
        else:
            score_list.append(str(self.player_name) + ": "
                                                    + str(self.black_count)
                                                    + "\n")

        with open("scores.txt", "w") as update:

            update.write(header)
            for score in score_list:
                update.write(score)
