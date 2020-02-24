import random
from pandas import DataFrame

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

    #when player makes a hit if single then show the point
    def hit(self, x, y, msg ):

        if msg == "player":
            print("You hit their ship!")
        else:
            print('Player2 choose to hit ({},{})'.format(x, y))
            print("You got attacked!")
        self.opponent_map[x][y] = "X"

    #when player makes a miss if single then show the point
    def miss(self, x, y, msg ):

        if msg == "player":
            print("You missed oh no!")
        else:
            print('Player2 choose to hit ({},{})'.format(x, y))
            print("Yay! They missed!")
        self.opponent_map[x][y] = "O"

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
