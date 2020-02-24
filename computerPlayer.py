from player import Player
from customExceptions import *
import random

class ComputerPlayer(Player):

    def __init__(self):
        super().__init__()

    def input_location(self, size):

        """ Take userinput and make sure they are valid range wise and format wise"""

        max = 65
        while True:
            try:
                #if single player then generate_map computes possible points
                user_input = self.generate_map(size)
                point1 = (abs(max - ord(user_input[0][0])), user_input[0][1])
                point2 = (abs(max - ord(user_input[1][0])), user_input[1][1])
                
                self.validate([point1[0], point1[1], point2[0], point2[1]],size)

            except (InvalidEntry, ValueError, TypeError) as _:
                print("please follow the format and enter the valid locations")
                continue
            except InvalidSize:
                print("ship is not able to fit on the given input")
                continue
            except AlreadyTaken:
                continue
            else:
                return

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
    
    #when player makes a hit if single then show the point
    def hit(self, x, y):
        print('Player2 choose to hit ({},{})'.format(x, y))
        print("You got attacked!")
        self.opponent_map[x][y] = "X"

    #when player makes a miss if single then show the point
    def miss(self, x, y):
        print('Player2 choose to hit ({},{})'.format(x, y))
        print("Yay! They missed!")
        self.opponent_map[x][y] = "O"
    
    #return if the attack is a hit or miss
    def check_round(self, opponent):
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        if opponent.player_map[x][y] == "X":
            self.hit(x, y)
        else:
            self.miss(x, y)

    