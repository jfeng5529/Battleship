import unittest 
import mock
from player import Player

class player_test(unittest.TestCase):

    # Test some possible attack/ship placement points
    def test_input(self):
        test = Player()
        test_param =[5, 3,3,0,1]

        #user outputs that will work
        user_input = ["A5,A1","h2,j2","i3,g3", "i1", "j10"]

        #Output that the system should return
        expected_output =[[(0,0), (0,4), "h"],[(7,1),(9,1),"v"], [(6,2), (8,2), "v"], [(8,0),(8,0),"h"],[(9,9),(9,9),"h"]]
        for i in range (len(user_input)):
            with mock.patch('builtins.input', return_value=user_input[i]):
        #Tests will pass if the expected outputs and function outputs matches
                assert test.get_input_location(test_param[i],"") == expected_output[i]   
 

if __name__ == '__main__':
    unittest.main()