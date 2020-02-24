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
        self.game = True
        self.win = ""
        self.all_ships = 18
        self.location = {"Aircraft Carrier": [1, 5], "Battleship": [
            1, 4], "Crusier": [1, 3], "Destroyer": [2, 2], "Submarine": [2, 1]}

    def intialize_map(self, player):

        """setting up map. Loops through all possible ship and calls input_location to ask for 
            userinput for placement of ships. Prints out the updated player map after each addition
        """
        for key in self.location.keys():
            for i in range(self.location[key][0]):
                player.input_location( self.location[key][1],"Where do you want to place the {} ({} squares) in the format of ex (A1, A5) or A1 for one square ".format(key, self.location[key][1]))
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
            player.check_round(opponent)
            self.check_game_status() 
        # player's turn
        else:
            player.check_round(opponent, msg)
            self.print_map(player)
    
    # mutiplayer mode general process
    def mulit_game(self):

        # initialized players maps with their ships
        print("Player 1 get ready")
        print(self.player1.print_player_map()) #pre print the empty map, so player can see where to put the ship
        self.intialize_map(self.player1) 
        os.system('cls||clear')  #clear terminal after player1 is done, so player2 cant view the ship locations

        #same for player2
        print("Player 2 get ready")
        print(self.player2.print_player_map())
        self.intialize_map(self.player2)
        os.system('cls||clear')

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

    #single player mode
    def single_game(self):
        self.player2 = ComputerPlayer()
        #loop thru ships to set up computer map
        for key in self.location.keys():
            for i in range(self.location[key][0]):
                self.player2.input_location( self.location[key][1])

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
        self.player2 = ComputerPlayer()
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
        for key in self.location.keys():
            for i in range(self.location[key][0]):
                self.player2.input_location(self.location[key][1])
        
        print(self.player2.print_player_map())

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
game.start()

#uncomment if u want to do test mode
#game.start_test_mode('single')

    
