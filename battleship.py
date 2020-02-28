import random
from pandas import DataFrame
from player import Player
from computerPlayer import ComputerPlayer
from customExceptions import *
import os

#setting up Battleship class
class Battleship:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.mode = "single"
        self.game = True
        self.win = ""
        self.all_ships = 18
        self.location = {"Aircraft Carrier": [1, 5], "Battleship": [
            1, 4], "Crusier": [1, 3], "Destroyer": [2, 2], "Submarine": [2, 1]}

    def intialize_map_multi(self, player):

        """setting up map for multiplayer. Loops through all possible ship and calls get_input_location to ask for 
            userinput for placement of ships. Prints out the updated player map after each addition
        """
        for key in self.location.keys():
            for i in range(self.location[key][0]):
                coordinates = player.get_input_location( self.location[key][1],"Where do you want to place the {} ({} squares) in the format of ex A1,A5 or A1 for one square ".format(key, self.location[key][1]))
                player.set_up_map(coordinates[0:2], coordinates[2])
                print(player.print_player_map())
            
    def intialize_map_single(self, player):

        """setting up map for single player. Loops through all possible ship and calls get_input_location from computer player 
            to generate random ship placement
        """
        for key in self.location.keys():
            for i in range(self.location[key][0]):
                coordinates = player.get_input_location( self.location[key][1]) 
                player.set_up_map(coordinates[0:2], coordinates[2])

    def chose_mode(self, message):

        """ collect the game mode multi or singluar from user, loops until valid response is collected
            enter testsingle or testmulti to open the test mode of the application
        """

        while True:
            try:
                user_input = input(message).lower()
                if user_input == "multiplayer" or user_input == "singleplayer" or user_input == "testmulti" or user_input == "testsingle":
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

    
    def check_game_status(self):
        """ Check to see if any player wins
            there are total 18 squares occupied by ships
            if there are 18 x or hits, then game ends and winner is set to player
        """
        val = sum(x.count('X') for x in self.player1.opponent_map)
        if val == 18:
            self.game = False
            self.win = "Player1"
        else:
            val = sum(x.count('X') for x in self.player2.opponent_map)
            if val == 18:
                self.game = False
                self.win = "Player2"

    #General process of each game round
    # -if input is valid, and update player map with hit or miss
    # - end game is anyone wins
    def round(self, player, opponent, msg="none"):
        #if playing single mode computer's turn
        if msg == "none":
            player.attack(opponent)
            self.check_game_status() 
        # player's turn
        else:
            player.attack(opponent, msg)
            self.check_game_status() 
            self.print_map(player)
    

    # mutiplayer mode general process
    def mulit_game(self):

        # initialized players maps with their ships
        print("Player 1 get ready")
        print(self.player1.print_player_map()) #pre print the empty map, so player can see where to put the ship
        self.intialize_map_multi(self.player1) 
        os.system('cls||clear')  #clear terminal after player1 is done, so player2 cant view the ship locations

        #same for player2
        print("Player 2 get ready")
        print(self.player2.print_player_map())
        self.intialize_map_multi(self.player2)
        os.system('cls||clear')

        print("Player 1 get ready")
        self.mode = "multi"
        self.start_game()

    #single player mode
    def single_game(self):
        self.player2 = ComputerPlayer()
        #loop thru ships to set up computer map
        self.intialize_map_single(self.player2)

        #set up player map
        print(self.player1.print_player_map())
        self.intialize_map_multi(self.player1)
        os.system('cls||clear')
        print("Player 1 get ready")

        #start game loop
        self.start_game()

    #start main game loop
    def start_game(self):
        while(self.game):

            #alternate rounds between players
            msg = "Player 1 enter your attack"
            self.round(self.player1, self.player2, msg)
            print("===============================================================================")
            if self.game == False:
                break

            if self.mode == 'multi':
                self.round(self.player2, self.player1,"Player 2 enter your attack" )
            else:
                self.round(self.player2, self.player1)
            print("===============================================================================")

        print("Congrates! {} won the game! You can save the world".format(self.win))

        self.another_round()
    
    #if user wants another round
    def another_round(self):
        while True:
            try:
                user_input = input("Are you up for another round? Enter yes or no").upper()
                if user_input == "YES":
                    self.start()
                elif user_input == "NO":

                    raise InvalidEntry
            except (InvalidEntry, ValueError, TypeError) as _:
                print("please enter yes or no")
                continue
            else:
                if user_input == "YES":
                    self.start()
                    return
                else:
                    print("Bye bye")
                    return

    #test mode that prefills the player maps, so we can just test the attack portion
    def start_test_mode(self, mode):
    #Prefill the player map for player1
        self.player1.player_map = [["X", "X", "X", "X", "X", "-", "-", "-", "-", "-"],
                                  ["X", "X", "X", "X", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "X", "X", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["X", "X", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-"],
                                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]]
        #single mode, auto generate the computer map
        if mode =="single":
            self.player2=ComputerPlayer()
            self.intialize_map_single(self.player2)
        #multi mode, set player2 map the same as player1 map
        else:
            self.player2.player_map = self.player1.player_map
            self.mode = "multi"

        self.start_game()

    #start the game by picking single or multi
    def start(self):
        val=self.chose_mode("Which mode would you like to play? Enter multiplayer or singleplayer  ")
        if val == "multiplayer":
            print("You have chosen the multiplayer mode, let's get started")
            self.mulit_game()
        elif val == "singleplayer":
            print("You have chosen the singleplayer mode, let's get started")
            self.single_game()
        elif val == "testmulti":
            print("You have chosen the testing multi mode")
            self.start_test_mode("multi")
        else:
            print("You have chosen the testing single mode")
            self.start_test_mode("single")


game = Battleship()
game.start()

    
