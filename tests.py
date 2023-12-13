#necessary imports
import unittest

#functions to test from files
from collection import addPlayerGames

#my unittest class
class Tests(unittest.TestCase):
    #tests that the addPlayerGames function works
    def testAddPlaerGames(self):
        #constants for this unittest
        EXPECTED_FIRST_ARCHIVE = "https://api.chess.com/pub/player/gmg1/games/2015/08"
        EXPECTED_NUMBER_OF_ENTRIES_IN_ARCHIVE_ONE = 6
        ARCHIVE_PERIOD = EXPECTED_FIRST_ARCHIVE[-7:].replace("/","-")
        TEST_USERNAME = "gmg1"

        #a the time of coding, gmg1 has only 1 archive, but if they were to play again, they would have more, so get the first result from the list
        result = addPlayerGames(TEST_USERNAME)[0]
        count = 0
        
        #checks how many lines in games.csv contain an entry for test user in the expected time period. This will never change and so we can see if the function has worked
        with open("games.csv","r") as f:
            safeLines = []
            for line in f.readlines():
                if line.split(",")[0] == TEST_USERNAME and line.split(",")[1] == ARCHIVE_PERIOD:
                    count += 1
                else:
                    safeLines.append(line)
        
        #removes the test user from the dataset as they are not a useful addition to the dataset
        with open("games.csv","w") as f:
            f.writelines(safeLines)
        
        #checks that the function has worked as expected
        self.assertEqual(result,EXPECTED_FIRST_ARCHIVE)
        self.assertEqual(count,EXPECTED_NUMBER_OF_ENTRIES_IN_ARCHIVE_ONE)

#test using this pgn https://api.chess.com/pub/player/mohssenbinaddi/games/2020/04 line 726 for extractTimesFromPgn

if __name__ == "__main__":
    unittest.main()