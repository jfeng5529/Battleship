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
            temp was kept as a holder for subarray to be replaced
            if the wholw entire spaced called by the two points are not taken
            then replaced the subarray with temp
        """
        #order the coordinates, so smaller one comes first
        x  = min(location[0][0], location[1][0])
        x2 = max(location[0][0], location[1][0])
        y  = min(location[0][1], location[1][1])
        y2 = max(location[0][1], location[1][1])

        #If the direction is horizantal, then x stays constant, used to temp to hold change to map
        if direction == "h":
            temp = []
            for i in range(y, y2+1):
                if self.player_map[x][i] != "-":
                    return False
                else:
                    temp.append("X")
            self.player_map[x][y:y2+1] = temp
            return True
        #If the direction is horizantal, then x stays constant, loop through to make sure all spots 
        #user picked are valid before making change to map
        else:
            for i in range(x, x2+1):
                if self.player_map[i][y] != "-":
                    return False
            for i in range(x, x2+1):
                self.player_map[i][y] = "X"
            return True

    #return if the attack is a hit or miss
    def check_round(self, opponent, msg):
        #generate random attacks
        point = self.input_location(0, msg)
        x = point[0]
        y = point[1]

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

    def input_location(self, size, msg="none"):

        """ Take userinput and make sure they are valid range wise and format wise"""

        max = 65
        while True:
            try:
                # if multi player then parse point from user input using ascii code
                
                user_input = input(msg).upper()
                if size == 0:
                    if len(user_input) < 2:
                        raise InvalidEntry
                    else:
                        points = [abs(max - ord(user_input[0])), int(user_input[1:])-1]
                        self.validate(points, size)
                        return points
                    
                else:
                    if size == 1:
                        user_input = [user_input, user_input]
                    else:
                        user_input = user_input.upper().split(",")

                    if len(user_input) != 2:
                        raise InvalidEntry

                    #convert characters into actual array point tuples
                    point1 = (abs(max - ord(user_input[0][0])), int(user_input[0][1:])-1)
                    point2 = (abs(max - ord(user_input[1][0])), int(user_input[1][1:])-1)

                    #if size is 0, then its is an attack point, so only one point is collected
                
                    self.validate([point1[0], point1[1], point2[0], point2[1]], size)

            except (InvalidEntry, ValueError, TypeError) as _:
                print("please follow the format and enter the valid locations")
                continue
            except InvalidSize:
                print("ship is not able to fit on the given input")
                continue
            except AlreadyTaken:
                print("Spot is already occupied, find another one")
                continue
            else:
                return 


    def validate(self, points, size):

        """validates if the input for placement of ship is correct"""

        #if point is not in the range of (10,10), the raise out of bound error
        if not all( 0 <= value <= 9 for value in points):
            raise InvalidEntry
        
        if size == 0:
            #It is an attack point check to see if point is chosen before - True if not, False if it has
            if self.opponent_map[points[0]][points[1]] != "-":
                raise AlreadyTaken
        else:
            # It is a ship placement coordinates
            point1 = (points[0], points[1])
            point2 = (points[2], points[3])

            #if valid then attempt to set up map with coordinates for horizontal
            #if set_up_map returns false if spot is taken, exception raised

            if point1[0] == point2[0] and abs(point1[1] - point2[1]) == size-1:
                coordinates = [(point1[0],
                        point1[1]), (point2[0], point2[1])]

                if self.set_up_map(coordinates, "h") == False:
                    raise AlreadyTaken
                
            #if valid then attempt to set up map with coordinates for vertical
            #if set_up_map returns false if spot is taken, exception raised

            elif point1[1] == point2[1] and abs(point1[0] - point2[0]) == size-1:
                coordinates = [( point1[0], point1[1]),
                                   ( point2[0], point1[1])]
                if self.set_up_map(coordinates, "v") == False:
                    raise AlreadyTaken

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
