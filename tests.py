import unittest
from collection import addPlayerGames
class Tests(unittest.TestCase):
    def testAddsGameInfo(self):
        result = addPlayerGames("gmg1")[0]
        count = 0
        with open("games.csv","r") as f:
            safeLines = []
            for line in f.readlines():
                if line.split(",")[0] == "gmg1" and line.split(",")[1] == "2015-08":
                    count += 1
                else:
                    safeLines.append(line)
        with open("games.csv","w") as f:
            f.writelines(safeLines)
                
        self.assertEqual(result,"https://api.chess.com/pub/player/gmg1/games/2015/08")
        self.assertEqual(count,6)

if __name__ == "__main__":
    unittest.main()