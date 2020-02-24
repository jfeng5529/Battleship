import random
from pandas import DataFrame
from player import Player
from customExceptions import *

#setting up Battleship class
class Battleship:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.game = True
        self.win = ""
        self.all_ships = 18
        self.location = {"Aircraft Carrier": [1, 5], "Battleship": [
            1, 4], "Crusier": [1, 3], "Destroyer": [2, 2], "Submarine": [2, 1]}
        # self.player1.player_map = [[X", "X", "X", "X", "X", "-", "-", "-", "-", "-"],
        #                           ["X", "X", "X", "X", "-",
        #                               "-", "-", "-", "-", "-"],
        #                           ["X", "X", "X", "-", "-",
        #                               "-", "-", "-", "-", "-"],
        #                           ["X", "X", "-", "-", "-",
        #                               "-", "-", "-", "-", "-"],
        #                           ["X", "X", "-", "-", "-",
        #                               "-", "-", "-", "-", "-"],
        #                           ["X", "-", "-", "-", "-",
        #                               "-", "-", "-", "-", "-"],
        #                           ["X", "-", "-", "-", "-",
        #                               "-", "-", "-", "-", "-"],
        #                           ["-", "-", "-", "-", "-",
        #                               "-", "-", "-", "-", "-"],
        #                           ["-", "-", "-", "-", "-",
        #                               "-", "-", "-", "-", "-"],
        #                           ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]]

        # self.player2.player_map = [["X","X", "X", "X", "X", "-","-","-","-","-"],
        #                           ["X","X", "X", "X", "-", "-","-","-","-","-"],
        #                           ["X","X", "X", "-", "-", "-","-","-","-","-"],
        #                           ["X","X", "-", "-", "-", "-","-","-","-","-"],
        #                           ["X","X", "-", "-", "-", "-","-","-","-","-"],
        #                           ["X","-", "-", "-", "-", "-","-","-","-","-"],
        #                           ["X","-", "-", "-", "-", "-","-","-","-","-"],
        #                           ["-", "-", "-", "-", "-","-","-","-","-","-"],
        #                           ["-", "-", "-", "-", "-","-","-","-","-","-"],
        #                           ["-", "-", "-", "-", "-","-","-","-","-","-"]]

    def input_location(self, size, player, message="none"):

        """ Take userinput and make sure they are valid range wise and format wise"""

        max = 65
        while True:
            try:
                #if single player then generate_map computes possible points
                if message == "none":
                    user_input = self.generate_map(size)
                    point1 = (abs(max - ord(user_input[0][0])), user_input[0][1])
                    point2 = (abs(max - ord(user_input[1][0])), user_input[1][1])
                else:
                # if multi player then parse point from user input using ascii code
                    user_input = input(message)
                    if size == 1:
                        user_input = [user_input.upper(), user_input.upper()]
                    else:
                        user_input = user_input.upper().split(",")
                    
                    if len(user_input) != 2:
                        raise InvalidEntry
                    point1 = (abs(max - ord(user_input[0][0])), int(user_input[0][1:])-1)
                    point2 = (abs(max - ord(user_input[1][0])), int(user_input[1][1:])-1)
                
                #if point is not in the range of (10,10), the raise out of bound error
                if not all( 0 <= value <= 9 for value in [point1[0], point1[1], point2[0], point2[1]]):
                    raise InvalidEntry

                #if valid then attempt to set up map with coordinates for horizontal
                #if set_up_map returns false if spot is taken, exception raised

                elif point1[0] == point2[0] and abs(point1[1] - point2[1]) == size-1:
                    coordinates = [(point1[0],
                        point1[1]), (point2[0], point2[1])]

                    if player.set_up_map(coordinates, "h") == False:
                        raise AlreadyTaken
                
                #if valid then attempt to set up map with coordinates for vertical
                #if set_up_map returns false if spot is taken, exception raised

                elif point1[1] == point2[1] and abs(point1[0] - point2[0]) == size-1:
                    coordinates = [( point1[0], point1[1]),
                                   ( point2[0], point1[1])]
                    if player.set_up_map(coordinates, "v") == False:
                        raise AlreadyTaken

                #user selected spots not equal to the squares of the ship, exception raised
                else:
                    raise InvalidSize

            except (InvalidEntry, ValueError) as _:
                print("please follow the format and enter the valid locations")
                continue
            except InvalidSize:
                print("ship is not able to fit on the given input")
                continue
            except AlreadyTaken:
                if message != "none":
                    print("Spot is already occupied, find another one")
                continue
            else:
                return

    def intialize_map(self, player):

        """setting up map. Loops through all possible ship and calls input_location to ask for 
            userinput for placement of ships. Prints out the updated player map after each addition
        """
        for key in self.location.keys():
            for i in range(self.location[key][0]):
                self.input_location(
                     self.location[key][1], player, "Where do you want to place the {} ({} squares) in the format of (point, point) ex A1,A5 or A1 for one square".format(key, self.location[key][1]))
                print(player.print_player_map())

    def chose_mode(self, message):

        """ collect the game mode multi or singluar from user, loops until valid response is collected """

        while True:
            try:
                user_input = input(message).lower()
                if user_input == "multiplayer" or user_input == "singleplayer":
                    return user_input
                else:
                    raise InvalidEntry

            except InvalidEntry:
                print("Please enter multiplayer or singleplayer")
                continue

    # prints out current player's opponenet map
    def print_map(self, player):
        print("Opponent Map")
        print(player.print_opponent_map())

    def get_input(self, msg, player):

        """ get valid attack inputs from user"""

        max_row = 65 # the row starts at A or 65
        while True:
            try:
                #collected user input and stored parsed points
                user_input = input(msg).upper()
                point = [abs(max_row - ord(user_input[0])), int(user_input[1:])-1]

                #raise exception is input is out of bound or already chosen
                if len(user_input) > 3 or point[0] > 9 or point[1] > 9 or point[1] < 0:
                    raise InvalidEntry
                if self.repeated(point[0], point[1],player):
                    raise AlreadyTaken

            except (TypeError, InvalidEntry) as _:
                print("Please enter a valid point")
                continue
            except AlreadyTaken:
                print("Already attacked this point before, try another one")
                continue
            else:
                point[0] = abs(max_row - ord(user_input[0]))
                return (point)

    #check to see if point is chosen before - True if not, False if it has
    def repeated(self,x, y, player):
            if player.opponent_map[x][y] != "-":
                return True
            else:
                return False

    #return if the attack is a hit or miss
    def check_round(self, point, player, opponent, msg ="player"):
        x = point[0]
        y = point[1]

        if opponent.player_map[x][y] == "X":
            player.hit(x, y, msg)
        else:
            player.miss(x, y, msg)

    def check_game_status(self):
        """ Check to see if any player wins
            there are total 18 squares occupied by ships
            if there are 18 x or hits, then game ends and winner is set to player
        """
        val = sum(x.count('X') for x in self.player1.opponent_map)
        if val == 18:
            self.game = False
            self.win = "Player1"
            return
        val = sum(x.count('X') for x in self.player2.opponent_map)
        if val == 18:
            self.game = False
            self.win = "Player2"
            return

    #General process of each game round
    # -if input is valid, and update player map with hit or miss
    # - end game is anyone wins
    def round(self, player, opponent, msg="none"):
        #if playing single mode computer's turn
        if msg == "none":
            val = [random.randint(0, 9), random.randint(0, 9)] #generate random attacks
            self.check_round(val, player, opponent, msg)
            self.check_game_status() 
        # player's turn
        else:
            val = self.get_input(msg, player)
            self.check_round(val, player, opponent)
            self.print_map(player)
    
    # mutiplayer mode general process
    def mulit_game(self):

        # initialized players maps with their ships
        print("Player 1 get ready")
        print(self.player1.print_player_map())
        self.intialize_map(self.player1)

        print("Player 2 get ready")
        print(self.player1.print_player_map())
        self.intialize_map(self.player2)

        #start game loop alterating between player one and two
        #loop breaks if anyone wins
        while(self.game):

            msg = "Player 1 enter your attack"
            self.round(self.player1, self.player2, msg)
            if self.game == False:
                break
            
            msg = "Player 2 enter your attack"
            self.round(self.player2, self.player1, msg)
            if self.game == False:
                self.win = "Player2"

        print("Congrates! {} won the game! You can save the world".format(self.win))

    #Auto generate ship placement for computer's ships
    def generate_map(self, size):

        #pick if horizantal or vertical
        if random.randint(0, 1) == 1:
            #if horizantal then any row, but column is restricted
            start_letter = random.choice("ABCDEFGHIJ")
            start_number = random.randint(0, 4)
            return [[start_letter, start_number],
                [start_letter, start_number+size - 1]]
        else:
            #if horizantal then any row, but row is restricted
            start_letter = random.choice("ABCDE")
            start_number = random.randint(0, 9)
            return [[start_letter, start_number],
                [chr(ord(start_letter) + size - 1), start_number]]

    #single player mode
    def single_game(self):
        #loop thru ships to set up computer map
        for key in self.location.keys():
            for i in range(self.location[key][0]):
                self.input_location(self.location[key][1], self.player2)

        #set up player map
        print(self.player1.print_player_map())
        self.intialize_map(self.player1)
        print("Player 1 get ready")

        #start game loop
        while(self.game):

            #alternate rounds between players
            msg = "Player 1 enter your attack"
            self.round(self.player1, self.player2, msg)
            if self.game == False:
                break
            print('\n')

            print("It's player2's turn")
            self.round(self.player2, self.player1)
            if self.game == False:
                self.win ="Player2"
            print("===============================================================================\n")

    #test mode so no need to set up maps
    def start_test_mode(self, mode):
        self.player1.player_map = [["X", "X", "X", "X", "X", "-", "-", "-", "-", "-"],
                                  ["X", "X", "X", "X", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "X", "X", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "X", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "X", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]]
        if mode == 'single':
            while(self.game):

                msg = "Player 1 enter your attack"
                self.round(self.player1, self.player2, msg)
                if self.game == False:
                    break
                print('\n')

                print("It's player2's turn")
                self.round(self.player2, self.player1)
                if self.game == False:
                    self.win ="Player2"
                print("===============================================================================\n")
        else:
            self.player1.player_map = [["X", "X", "X", "X", "X", "-", "-", "-", "-", "-"],
                                  ["X", "X", "X", "X", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "X", "X", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "X", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "X", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]]
            self.mulit_game()

    #start the game by picking single or multi
    def start(self):
        val=self.chose_mode("Which mode would you like to play? Enter multiplayer or singleplayer  ")
        if val == "multiplayer":
            print("You have chosen the multiplayer mode, let's get started")
            self.mulit_game()
        else:
            print("You have chosen the singleplayer mode, let's get started")
            self.single_game()


game = Battleship()
game.start_test_mode("single")


    
