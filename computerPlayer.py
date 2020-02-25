from player import Player
from customExceptions import *
import random

class ComputerPlayer(Player):

    def __init__(self):
        super().__init__()

    def get_input_location(self, size):

        """ Take userinput and make sure they are valid range wise and format wise"""

        while True:
            try:
                #if single player then genrate_point computes possible points
                user_input = self.genrate_point(size)
                point1 = (user_input[0][0], user_input[0][1])
                point2 = (user_input[1][0], user_input[1][1])
                
                x  = min(point1[0], point2[0])
                x2 = max(point1[0], point2[0])
                y  = min(point1[1], point2[1])
                y2 = max(point1[1], point2[1])

                point1 =(x,y)
                point2 = (x2,y2)

                direction = self.validate(size, point1, point2)

            except (InvalidEntry, ValueError, TypeError) as _:
                continue
            except InvalidSize:
                continue
            except AlreadyTaken:
                continue
            else:
                return [(point1), (point2), direction]

    #Auto generate ship placement for computer's ships
    def genrate_point(self, size):

        #pick if horizantal or vertical
        if random.randint(0, 1) == 1:
            #if horizantal then any row, but column is restricted
            start_x = random.randint(0, 9)
            start_y = random.randint(0, 9-(size-1))
            return [[start_x, start_y],
                [start_x, start_y+size - 1]]
        else:
            #if horizantal then any row, but row is restricted
            start_x = random.randint(0, 9-(size-1))
            start_y = random.randint(0, 9)
            return [(start_x, start_y),
                (start_x + size - 1, start_y)]
    
    #when player makes a hit if single then show the point
    def hit(self, x, y):
        print('Player2 choose to hit ({},{})'.format(chr(x+65), y+1))
        print("You got attacked!")
        self.opponent_map[x][y] = "X"

    #when player makes a miss if single then show the point
    def miss(self, x, y):
        print('Player2 choose to hit ({},{})'.format(chr(x+65), y+1))
        print("Yay! They missed!")
        self.opponent_map[x][y] = "O"
    
    #return if the attack is a hit or miss
    def attack(self, opponent):

        point = self.get_input_location(0)
        x,y = point[0]
        if opponent.player_map[x][y] == "X":
            self.hit(x, y)
        else:
            self.miss(x, y)

    