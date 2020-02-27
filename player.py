import random
from pandas import DataFrame
from customExceptions import *

#setting up player class
class Player:
    def __init__(self):
        self.player_map = [["-"]*10 for i in range(10)]
        self.opponent_map = [['-']*10 for i in range(10)]

    def set_up_map(self, location, direction):
        """
            setting up player map base on two points
            loop thru the selected points and placed 
        """
        x, y = location[0]
        x2, y2 = location[1]
        #If the direction is horizantal, then x stays constant, used to temp to hold change to map
        if direction == "h":
            for i in range(y, y2+1):
                self.player_map[x][i] = "X"
        #If the direction is horizantal, then x stays constant, loop through to make sure all spots 
        #user picked are valid before making change to map
        else:
            for i in range(x, x2+1):
                self.player_map[i][y] = "X"

    #checks if any of the sqauares are already taken       
    def is_taken(self, location, direction):
        x,y = location[0]
        x2,y2 = location[1]
        if direction == "h":
            for i in range(y, y2+1):
                if self.player_map[x][i] != "-":
                    return True
        else:
            for i in range(x, x2+1):
                if self.player_map[i][y] != "-":
                    return True  
        return False

    #return if the attack is a hit or miss
    def attack(self, opponent, msg):
        #generate random attacks
        point = self.get_input_location(0, msg)
        x = point[0][0]
        y = point[0][1]

        if opponent.player_map[x][y] == "X":
            self.hit(x, y)
        else:
            self.miss(x, y)

    #when player makes a hit if single then show the point
    def hit(self, x, y):
        print("You hit their ship!")
        self.opponent_map[x][y] = "X"

    #when player makes a miss if single then show the point
    def miss(self, x, y):
        print("You missed oh no!")
        self.opponent_map[x][y] = "O"


    def get_input_location(self, size, msg):
        """Generate or ask user for point inputs"""
        max_row = 65
        while True:
            try:
                val = input(msg).upper()
                # if multi player then parse point from user input using ascii code
                if size == 1 or size == 0:
                    val = [val, val]
                else:
                    val = val.split(",")

                    if len(val) != 2: raise InvalidEntry

                #convert characters into actual array point tuples
                point1 = (abs(max_row - ord(val[0][0])), int(val[0][1:])-1)
                point2 = (abs(max_row - ord(val[1][0])), int(val[1][1:])-1)

                #order the coordinates, so smaller one comes first
                x  = min(point1[0], point2[0])
                x2 = max(point1[0], point2[0])
                y  = min(point1[1], point2[1])
                y2 = max(point1[1], point2[1])

                point1 =(x,y)
                point2 = (x2,y2)
                direction = self.validate(size,point1, point2)

            except (InvalidEntry, ValueError, TypeError, IndexError) as _:
                print("please follow the format and enter the valid locations")
                continue
            except InvalidSize:
                print("ship is not able to fit on the given input")
                continue
            except AlreadyTaken:
                print("Spot is already occupied, find another one")
                continue
            else:
                return [point1, point2, direction]
     

    def validate(self, size, point1, point2):

        """ Take userinput and make sure they are valid range wise and format wise"""
        #if point is not in the range of (10,10), the raise out of bound error
        if not all( 0 <= value <= 9 for value in [point1[0], point1[1], point2[0], point2[1]]):
            raise InvalidEntry

        #checking for attacks
        if size == 0:
            if self.opponent_map[point1[0]][point1[1]] != "-":
                raise AlreadyTaken
            else:
                return "h"

        #if valid then attempt to set up map with coordinates for horizontal
        #if set_up_map returns false if spot is taken, exception raised

        if point1[0] == point2[0] and point2[1] - point1[1] == size-1:

            if self.is_taken([point1, point2], "h"):
                raise AlreadyTaken
            else:
                return "h"
    
        #if valid then attempt to set up map with coordinates for vertical
        #if set_up_map returns false if spot is taken, exception raised

        elif point1[1] == point2[1] and point2[0] - point1[0] == size-1:
            if self.is_taken([point1, point2], "v"):
                raise AlreadyTaken
            else:
                return "v"
        #user selected spots not equal to the squares of the ship, exception raised
        else:
            raise InvalidSize


    # print opponenet map using dataframe from Pandas
    def print_opponent_map(self):
        df = DataFrame(self.opponent_map)
        df.index=['A', 'B', 'C','D','E', 'F', 'G', 'H', 'I', 'J']
        df.columns =[1,2,3,4,5,6,7,8,9,10]
        return df

     # print player map using dataframe from Pandas
    def print_player_map(self):
        df = DataFrame(self.player_map)
        df.index=['A', 'B', 'C','D','E', 'F', 'G', 'H', 'I', 'J']
        df.columns =[1,2,3,4,5,6,7,8,9,10]
        return df
