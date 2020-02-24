import random
from pandas import DataFrame

#setting up player class
class Player:
    def __init__(self):
        self.player_map = [["-"]*10 for i in range(10)]
        self.opponent_map = [['-']*10 for i in range(10)]

    def setUpMap(self, location, direction):
        """setting up player map base on two points"""
        x, y = location[0]
        x2, y2 = location[1]
        if direction == "h":
            temp = []
            for i in range(y, y2):
                if self.player_map[x][i] != "-":
                    return False
                else:
                    temp.append("X")
            self.player_map[x][min(y, y2):max(y, y2)] = temp
            return True
        else:
            for i in range(x, x2):
                if self.player_map[i][y] != "-":
                    return False
            for i in range(x, x2+1):
                self.player_map[i][y] = "X"
            return True

    def hit(self, x, y, msg ):
        if msg == "player":
            print("You hit their ship!")
        else:
            print('Player2 choose to hit ({},{})'.format(x, y))
            print("You got attacked!")
        self.opponent_map[x][y] = "X"

    def miss(self, x, y, msg ):
        if msg == "player":
            print("You missed oh no!")
        else:
            print('Player2 choose to hit ({},{})'.format(x, y))
            print("Yay! They missed!")
        self.opponent_map[x][y] = "O"

    def printOpponentMap(self):
        return DataFrame(self.opponent_map)

    def printPlayerMap(self):
        return DataFrame(self.player_map)



class InvalidEntry(Exception):
    pass


class InvalidSize(Exception):
    pass


class AlreadyTaken(Exception):
    pass


class Battleship:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.game = True
        self.win = ""
        self.allShips = 18
        self.location = {"Aircraft Carrier": [1, 5], "Battleship": [
            1, 4], "Crusier": [1, 3], "Destroyer": [2, 2], "Submarine": [2, 1]}
        # self.player1.player_map = [["X", "X", "X", "X", "X", "-", "-", "-", "-", "-"],
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

    def inputLocation(self, size, player, message="none"):
        max = 65

        while True:
            try:
                if message == "none":
                    userInput = self.generateMap(size)
                    point1 = (userInput[0][0], userInput[0][1])
                    point2 = (userInput[1][0], userInput[1][1])
                else:
                    userInput = input(message)
                    userInput = userInput.upper().split(",")
                    if len(userInput) != 2:
                        raise InvalidEntry
                    point1 = (userInput[0][0], int(userInput[0][1:])-1)
                    point2 = (userInput[1][0], int(userInput[1][1:])-1)

                if point1[0] > 'J' or point1[1] > 10 or point2[0] > 'J' or point2[1] > 10:
                    raise InvalidEntry
                elif point1[0] == point2[0] and abs(point1[1] - point2[1]) == size-1:
                    constant = abs(max - ord(point1[0]))
                    coordinates = [(constant,
                        point1[1]), (constant, point2[1])]
                    if player.setUpMap(coordinates, "h") == False:
                        raise AlreadyTaken
                elif point1[1] == point2[1] and abs(ord(point1[0]) - ord(point2[0])) == size-1:
                    constant = point1[1]
                    coordinates = [(abs(max - ord(point1[0])), constant),
                                   (abs(max - ord(point2[0])), constant)]
                    if player.setUpMap(coordinates, "v") == False:
                        raise AlreadyTaken
                else:
                    raise InvalidSize

            except InvalidEntry:
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

    def intializeMap(self, player):
        for key in self.location.keys():
            for i in range(self.location[key][0]):
                self.inputLocation(
                     self.location[key][1], player, "Where do you want to place the {} ({} squares) in the format of (point, point)".format(key, self.location[key][1]))
                print(player.printPlayerMap())

    def choseMode(self, message):
        while True:

            try:
                userInput = input(message).lower()
                print(userInput)
                if userInput == "multiplayer" or userInput == "singleplayer":
                    return userInput
                else:
                    raise InvalidEntry

            except InvalidEntry:
                print("Please enter multiplayer or singleplayer")
                continue

    def printMap(self, player):
        print("Opponent Map")
        print(player.printOpponentMap())

    def getInput(self, msg):
        max = 65
        while True:
            try:
                userInput = input(msg).upper()
                point = [userInput[0], int(userInput[1:])-1]
                if len(userInput) > 3 or point[0] > "J" or point[1] > 9 or point[1] < 0:
                    raise InvalidEntry
            except (TypeError, InvalidEntry) as _:
                print("Please enter a valid point")
                continue
            else:
                point[0] = abs(max - ord(userInput[0]))
                return (point)

    def checkRound(self, point, player, opponent, msg ="player"):
        x = point[0]
        y = point[1]
        def repeated(x, y):
            if player.opponent_map[x][y] != "-":
                return True
            else:
                return False

        if repeated(x, y):
            print("Already attacked this point before, try another one")
        else:
            if opponent.player_map[x][y] == "X":
                player.hit(x, y, msg)
            else:
                player.miss(x, y, msg)

    def checkGameStatus(self):
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

    def round(self, player, opponent, msg="none"):
        if msg == "none":
            val = [random.randint(0, 9), random.randint(0, 9)]
            self.checkRound(val, player, opponent, msg)
            self.checkGameStatus()
        else:
            val = self.getInput(msg)
            self.checkRound(val, player, opponent)
            self.printMap(player)
    

    def mulitGame(self):
        print("Player 1 get ready")
        self.intializeMap(self.player1)

        print("Player 2 get ready")
        self.intializeMap(self.player2)

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

    def generateMap(self, size):
        if random.randint(0, 1) == 1:
            startLetter = random.choice("ABCDEFGHIJ")
            startNumber = random.randint(0, 4)
            return [[startLetter, startNumber],
                [startLetter, startNumber+size - 1]]
        else:
            startLetter = random.choice("ABCDE")
            startNumber = random.randint(0, 9)
            return [[startLetter, startNumber],
                [chr(ord(startLetter) + size - 1), startNumber]]

    def singleGame(self):
        for key in self.location.keys():
            for i in range(self.location[key][0]):
                 self.inputLocation(self.location[key][1], self.player2)

        self.intializeMap(self.player1)
        print("Player 1 get ready")

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


    def start(self):
        val=self.choseMode("Which mode would you like to play? Enter multiplayer or singleplayer  ")
        if val == "multiplayer":
            print("You have chosen the multiplayer game, let's get started")
            self.mulitGame()
        else:
            self.singleGame()


game = Battleship()
game.start()


    
