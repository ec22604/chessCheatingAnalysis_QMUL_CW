#necessary imports
import unittest
import pandas as pd

#functions to test from files
from collection import addPlayerGames
from analysis import extractTimesFromPGN,calculateUserTimeAdvantage,decodeb64,applyControlClass,calcTime,timeSpent

#FUNCTIONS TODO:
#avgTimeSpentUser
#avgTimeSpentPerTimeControl
#distinguishCheatersByColour
#winRatio
#largestWinStreak
#

#my unittest class
class Tests(unittest.TestCase):

    #tests that the addPlayerGames function works
    def testAddPlayerGames(self):
        #constants for this unittest
        EXPECTED_FIRST_ARCHIVE = "https://api.chess.com/pub/player/gmg1/games/2015/08"
        EXPECTED_NUMBER_OF_ENTRIES_IN_ARCHIVE_ONE = 6
        ARCHIVE_PERIOD = EXPECTED_FIRST_ARCHIVE[-7:].replace("/","-")
        TEST_USERNAME = "gmg1"

        #at the time of coding, gmg1 has only 1 archive, but if they were to play again, they would have more, so get the first result from the list
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

    #tests that the decodeb4 function works
    def testDecodeb64(self):
        #constants
        TEST_DATAFRAME = pd.DataFrame({"user":["hikaru"],"period":["2014-01"],"userColour":["white"],"userResult":["win"],"opponentResult":["resigned"],"timeControl":["180"],"pgn":["J1tFdmVudCAiTGl2ZSBDaGVzcyJdXG5bU2l0ZSAiQ2hlc3MuY29tIl1cbltEYXRlICIyMDE0LjAxLjA2Il1cbltSb3VuZCAiLSJdXG5bV2hpdGUgIkhpa2FydSJdXG5bQmxhY2sgIkdvZHN3aWxsIl1cbltSZXN1bHQgIjEtMCJdXG5bQ3VycmVudFBvc2l0aW9uICI2azEvMXAyUjMvcDFwNS84LzJQMUIzLzFQMVAxcDFQL1A2Sy84IGIgLSAtIl1cbltUaW1lem9uZSAiVVRDIl1cbltFQ08gIkMyNSJdXG5bRUNPVXJsICJodHRwczovL3d3dy5jaGVzcy5jb20vb3BlbmluZ3MvVmllbm5hLUdhbWUtTWF4LUxhbmdlLVBhdWxzZW4tVmFyaWF0aW9uLTMuLi5nNi00LkJnMi1CZzciXVxuW1VUQ0RhdGUgIjIwMTQuMDEuMDYiXVxuW1VUQ1RpbWUgIjIzOjUwOjE3Il1cbltXaGl0ZUVsbyAiMjM1NCJdXG5bQmxhY2tFbG8gIjIxNjciXVxuW1RpbWVDb250cm9sICIxODAiXVxuW1Rlcm1pbmF0aW9uICJIaWthcnUgd29uIGJ5IHJlc2lnbmF0aW9uIl1cbltTdGFydFRpbWUgIjIzOjUwOjE3Il1cbltFbmREYXRlICIyMDE0LjAxLjA2Il1cbltFbmRUaW1lICIyMzo1NDozOSJdXG5bTGluayAiaHR0cHM6Ly93d3cuY2hlc3MuY29tL2dhbWUvbGl2ZS82OTI2Njc4MjMiXVxuXG4xLiBlNCB7WyVjbGsgMDowMzowMF19IDEuLi4gZTUge1slY2xrIDA6MDM6MDBdfSAyLiBOYzMge1slY2xrIDA6MDI6NTcuNl19IDIuLi4gTmM2IHtbJWNsayAwOjAyOjU3LjJdfSAzLiBnMyB7WyVjbGsgMDowMjo0Mi40XX0gMy4uLiBnNiB7WyVjbGsgMDowMjo1Mi41XX0gNC4gQmcyIHtbJWNsayAwOjAyOjQwLjhdfSA0Li4uIEJnNyB7WyVjbGsgMDowMjo1MS44XX0gNS4gTmdlMiB7WyVjbGsgMDowMjozOC4zXX0gNS4uLiBOZ2U3IHtbJWNsayAwOjAyOjUwLjhdfSA2LiBPLU8ge1slY2xrIDA6MDI6MzcuNl19IDYuLi4gTy1PIHtbJWNsayAwOjAyOjQ5LjddfSA3LiBkMyB7WyVjbGsgMDowMjozNy4xXX0gNy4uLiBkNiB7WyVjbGsgMDowMjo0OC43XX0gOC4gaDMge1slY2xrIDA6MDI6MzYuNl19IDguLi4gaDYge1slY2xrIDA6MDI6NDYuOV19IDkuIEJlMyB7WyVjbGsgMDowMjozNS41XX0gOS4uLiBCZTYge1slY2xrIDA6MDI6NDUuNV19IDEwLiBRZDIge1slY2xrIDA6MDI6MzVdfSAxMC4uLiBRZDcge1slY2xrIDA6MDI6NDRdfSAxMS4gS2gyIHtbJWNsayAwOjAyOjMzXX0gMTEuLi4gS2g3IHtbJWNsayAwOjAyOjQyLjVdfSAxMi4gTmQ1IHtbJWNsayAwOjAyOjMyLjJdfSAxMi4uLiBOZDQge1slY2xrIDA6MDI6MzcuNF19IDEzLiBOeGU3IHtbJWNsayAwOjAyOjIxLjhdfSAxMy4uLiBReGU3IHtbJWNsayAwOjAyOjMzXX0gMTQuIGMzIHtbJWNsayAwOjAyOjIxLjFdfSAxNC4uLiBOeGUyIHtbJWNsayAwOjAyOjMxLjddfSAxNS4gUXhlMiB7WyVjbGsgMDowMjoyMC4zXX0gMTUuLi4gYzYge1slY2xrIDA6MDI6MzAuNV19IDE2LiBmNCB7WyVjbGsgMDowMjoxOC45XX0gMTYuLi4gZjUge1slY2xrIDA6MDI6MjguOF19IDE3LiBSYWUxIHtbJWNsayAwOjAyOjE2LjNdfSAxNy4uLiBhNiB7WyVjbGsgMDowMjoxOC4xXX0gMTguIGZ4ZTUge1slY2xrIDA6MDI6MTMuMV19IDE4Li4uIGR4ZTUge1slY2xrIDA6MDI6MTYuNl19IDE5LiBleGY1IHtbJWNsayAwOjAyOjExLjhdfSAxOS4uLiBCeGY1IHtbJWNsayAwOjAyOjE1LjhdfSAyMC4gZzQge1slY2xrIDA6MDI6MTEuMl19IDIwLi4uIEJlNiB7WyVjbGsgMDowMjoxNC44XX0gMjEuIGM0IHtbJWNsayAwOjAyOjEwLjddfSAyMS4uLiBSYWQ4IHtbJWNsayAwOjAyOjEyLjRdfSAyMi4gQmU0IHtbJWNsayAwOjAyOjA5LjZdfSAyMi4uLiBCZjcge1slY2xrIDA6MDI6MDQuM119IDIzLiBiMyB7WyVjbGsgMDowMjowNy40XX0gMjMuLi4gUWg0IHtbJWNsayAwOjAxOjM4LjhdfSAyNC4gQmYyIHtbJWNsayAwOjAyOjA0LjhdfSAyNC4uLiBRZzUge1slY2xrIDA6MDE6MzddfSAyNS4gQmM1IHtbJWNsayAwOjAyOjAzLjZdfSAyNS4uLiBCZTYge1slY2xrIDA6MDE6MjIuN119IDI2LiBCeGY4IHtbJWNsayAwOjAxOjQ3LjRdfSAyNi4uLiBSeGY4IHtbJWNsayAwOjAxOjIwLjldfSAyNy4gUnhmOCB7WyVjbGsgMDowMTo0NS4xXX0gMjcuLi4gQnhmOCB7WyVjbGsgMDowMToyMC4xXX0gMjguIFFmMiB7WyVjbGsgMDowMTo0NC40XX0gMjguLi4gQmU3IHtbJWNsayAwOjAxOjA5LjZdfSAyOS4gUmYxIHtbJWNsayAwOjAxOjQyXX0gMjkuLi4gaDUge1slY2xrIDA6MDE6MDUuMl19IDMwLiBneGg1IHtbJWNsayAwOjAxOjQwLjFdfSAzMC4uLiBReGg1IHtbJWNsayAwOjAxOjA0LjVdfSAzMS4gUWYzIHtbJWNsayAwOjAxOjM5LjNdfSAzMS4uLiBRZzUge1slY2xrIDA6MDA6NTkuNF19IDMyLiBSZzEge1slY2xrIDA6MDE6MzQuMV19IDMyLi4uIFFmNCsge1slY2xrIDA6MDA6NDguNl19IDMzLiBReGY0IHtbJWNsayAwOjAxOjI5LjhdfSAzMy4uLiBleGY0IHtbJWNsayAwOjAwOjQ3LjhdfSAzNC4gUnhnNiB7WyVjbGsgMDowMToyOS40XX0gMzQuLi4gZjMge1slY2xrIDA6MDA6MzIuOV19IDM1LiBSeGU2KyB7WyVjbGsgMDowMToyNy4yXX0gMzUuLi4gS2c4IHtbJWNsayAwOjAwOjMyXX0gMzYuIFJ4ZTcge1slY2xrIDA6MDE6MjYuM119IDEtMFxuJw=="],"rules":["chess"],"userRating":["2354"],"opponentRating":["2167"],"endTime":["1389052479"]})
        EXPECTED_VALUE = "'[Event \"Live Chess\"]\\n[Site \"Chess.com\"]\\n[Date \"2014.01.06\"]\\n[Round \"-\"]\\n[White \"Hikaru\"]\\n[Black \"Godswill\"]\\n[Result \"1-0\"]\\n[CurrentPosition \"6k1/1p2R3/p1p5/8/2P1B3/1P1P1p1P/P6K/8 b - -\"]\\n[Timezone \"UTC\"]\\n[ECO \"C25\"]\\n[ECOUrl \"https://www.chess.com/openings/Vienna-Game-Max-Lange-Paulsen-Variation-3...g6-4.Bg2-Bg7\"]\\n[UTCDate \"2014.01.06\"]\\n[UTCTime \"23:50:17\"]\\n[WhiteElo \"2354\"]\\n[BlackElo \"2167\"]\\n[TimeControl \"180\"]\\n[Termination \"Hikaru won by resignation\"]\\n[StartTime \"23:50:17\"]\\n[EndDate \"2014.01.06\"]\\n[EndTime \"23:54:39\"]\\n[Link \"https://www.chess.com/game/live/692667823\"]\\n\\n1. e4 {[%clk 0:03:00]} 1... e5 {[%clk 0:03:00]} 2. Nc3 {[%clk 0:02:57.6]} 2... Nc6 {[%clk 0:02:57.2]} 3. g3 {[%clk 0:02:42.4]} 3... g6 {[%clk 0:02:52.5]} 4. Bg2 {[%clk 0:02:40.8]} 4... Bg7 {[%clk 0:02:51.8]} 5. Nge2 {[%clk 0:02:38.3]} 5... Nge7 {[%clk 0:02:50.8]} 6. O-O {[%clk 0:02:37.6]} 6... O-O {[%clk 0:02:49.7]} 7. d3 {[%clk 0:02:37.1]} 7... d6 {[%clk 0:02:48.7]} 8. h3 {[%clk 0:02:36.6]} 8... h6 {[%clk 0:02:46.9]} 9. Be3 {[%clk 0:02:35.5]} 9... Be6 {[%clk 0:02:45.5]} 10. Qd2 {[%clk 0:02:35]} 10... Qd7 {[%clk 0:02:44]} 11. Kh2 {[%clk 0:02:33]} 11... Kh7 {[%clk 0:02:42.5]} 12. Nd5 {[%clk 0:02:32.2]} 12... Nd4 {[%clk 0:02:37.4]} 13. Nxe7 {[%clk 0:02:21.8]} 13... Qxe7 {[%clk 0:02:33]} 14. c3 {[%clk 0:02:21.1]} 14... Nxe2 {[%clk 0:02:31.7]} 15. Qxe2 {[%clk 0:02:20.3]} 15... c6 {[%clk 0:02:30.5]} 16. f4 {[%clk 0:02:18.9]} 16... f5 {[%clk 0:02:28.8]} 17. Rae1 {[%clk 0:02:16.3]} 17... a6 {[%clk 0:02:18.1]} 18. fxe5 {[%clk 0:02:13.1]} 18... dxe5 {[%clk 0:02:16.6]} 19. exf5 {[%clk 0:02:11.8]} 19... Bxf5 {[%clk 0:02:15.8]} 20. g4 {[%clk 0:02:11.2]} 20... Be6 {[%clk 0:02:14.8]} 21. c4 {[%clk 0:02:10.7]} 21... Rad8 {[%clk 0:02:12.4]} 22. Be4 {[%clk 0:02:09.6]} 22... Bf7 {[%clk 0:02:04.3]} 23. b3 {[%clk 0:02:07.4]} 23... Qh4 {[%clk 0:01:38.8]} 24. Bf2 {[%clk 0:02:04.8]} 24... Qg5 {[%clk 0:01:37]} 25. Bc5 {[%clk 0:02:03.6]} 25... Be6 {[%clk 0:01:22.7]} 26. Bxf8 {[%clk 0:01:47.4]} 26... Rxf8 {[%clk 0:01:20.9]} 27. Rxf8 {[%clk 0:01:45.1]} 27... Bxf8 {[%clk 0:01:20.1]} 28. Qf2 {[%clk 0:01:44.4]} 28... Be7 {[%clk 0:01:09.6]} 29. Rf1 {[%clk 0:01:42]} 29... h5 {[%clk 0:01:05.2]} 30. gxh5 {[%clk 0:01:40.1]} 30... Qxh5 {[%clk 0:01:04.5]} 31. Qf3 {[%clk 0:01:39.3]} 31... Qg5 {[%clk 0:00:59.4]} 32. Rg1 {[%clk 0:01:34.1]} 32... Qf4+ {[%clk 0:00:48.6]} 33. Qxf4 {[%clk 0:01:29.8]} 33... exf4 {[%clk 0:00:47.8]} 34. Rxg6 {[%clk 0:01:29.4]} 34... f3 {[%clk 0:00:32.9]} 35. Rxe6+ {[%clk 0:01:27.2]} 35... Kg8 {[%clk 0:00:32]} 36. Rxe7 {[%clk 0:01:26.3]} 1-0\\n'"
        ALTERED_DATAFRAME = TEST_DATAFRAME["pgn"].apply(decodeb64)

        #after applying the function. does it give what is expected?
        self.assertEqual(ALTERED_DATAFRAME.loc[0],EXPECTED_VALUE)
    
    #tests that the extractTimesFromPgn function works
    def testExtractTimesFromPgn(self):
        #constants
        TEST_DATAFRAME = pd.DataFrame({"user":["hikaru"],"period":["2014-01"],"userColour":["white"],"userResult":["win"],"opponentResult":["resigned"],"timeControl":["180"],"pgn":["'[Event \"Live Chess\"]\\n[Site \"Chess.com\"]\\n[Date \"2014.01.06\"]\\n[Round \"-\"]\\n[White \"Hikaru\"]\\n[Black \"Godswill\"]\\n[Result \"1-0\"]\\n[CurrentPosition \"6k1/1p2R3/p1p5/8/2P1B3/1P1P1p1P/P6K/8 b - -\"]\\n[Timezone \"UTC\"]\\n[ECO \"C25\"]\\n[ECOUrl \"https://www.chess.com/openings/Vienna-Game-Max-Lange-Paulsen-Variation-3...g6-4.Bg2-Bg7\"]\\n[UTCDate \"2014.01.06\"]\\n[UTCTime \"23:50:17\"]\\n[WhiteElo \"2354\"]\\n[BlackElo \"2167\"]\\n[TimeControl \"180\"]\\n[Termination \"Hikaru won by resignation\"]\\n[StartTime \"23:50:17\"]\\n[EndDate \"2014.01.06\"]\\n[EndTime \"23:54:39\"]\\n[Link \"https://www.chess.com/game/live/692667823\"]\\n\\n1. e4 {[%clk 0:03:00]} 1... e5 {[%clk 0:03:00]} 2. Nc3 {[%clk 0:02:57.6]} 2... Nc6 {[%clk 0:02:57.2]} 3. g3 {[%clk 0:02:42.4]} 3... g6 {[%clk 0:02:52.5]} 4. Bg2 {[%clk 0:02:40.8]} 4... Bg7 {[%clk 0:02:51.8]} 5. Nge2 {[%clk 0:02:38.3]} 5... Nge7 {[%clk 0:02:50.8]} 6. O-O {[%clk 0:02:37.6]} 6... O-O {[%clk 0:02:49.7]} 7. d3 {[%clk 0:02:37.1]} 7... d6 {[%clk 0:02:48.7]} 8. h3 {[%clk 0:02:36.6]} 8... h6 {[%clk 0:02:46.9]} 9. Be3 {[%clk 0:02:35.5]} 9... Be6 {[%clk 0:02:45.5]} 10. Qd2 {[%clk 0:02:35]} 10... Qd7 {[%clk 0:02:44]} 11. Kh2 {[%clk 0:02:33]} 11... Kh7 {[%clk 0:02:42.5]} 12. Nd5 {[%clk 0:02:32.2]} 12... Nd4 {[%clk 0:02:37.4]} 13. Nxe7 {[%clk 0:02:21.8]} 13... Qxe7 {[%clk 0:02:33]} 14. c3 {[%clk 0:02:21.1]} 14... Nxe2 {[%clk 0:02:31.7]} 15. Qxe2 {[%clk 0:02:20.3]} 15... c6 {[%clk 0:02:30.5]} 16. f4 {[%clk 0:02:18.9]} 16... f5 {[%clk 0:02:28.8]} 17. Rae1 {[%clk 0:02:16.3]} 17... a6 {[%clk 0:02:18.1]} 18. fxe5 {[%clk 0:02:13.1]} 18... dxe5 {[%clk 0:02:16.6]} 19. exf5 {[%clk 0:02:11.8]} 19... Bxf5 {[%clk 0:02:15.8]} 20. g4 {[%clk 0:02:11.2]} 20... Be6 {[%clk 0:02:14.8]} 21. c4 {[%clk 0:02:10.7]} 21... Rad8 {[%clk 0:02:12.4]} 22. Be4 {[%clk 0:02:09.6]} 22... Bf7 {[%clk 0:02:04.3]} 23. b3 {[%clk 0:02:07.4]} 23... Qh4 {[%clk 0:01:38.8]} 24. Bf2 {[%clk 0:02:04.8]} 24... Qg5 {[%clk 0:01:37]} 25. Bc5 {[%clk 0:02:03.6]} 25... Be6 {[%clk 0:01:22.7]} 26. Bxf8 {[%clk 0:01:47.4]} 26... Rxf8 {[%clk 0:01:20.9]} 27. Rxf8 {[%clk 0:01:45.1]} 27... Bxf8 {[%clk 0:01:20.1]} 28. Qf2 {[%clk 0:01:44.4]} 28... Be7 {[%clk 0:01:09.6]} 29. Rf1 {[%clk 0:01:42]} 29... h5 {[%clk 0:01:05.2]} 30. gxh5 {[%clk 0:01:40.1]} 30... Qxh5 {[%clk 0:01:04.5]} 31. Qf3 {[%clk 0:01:39.3]} 31... Qg5 {[%clk 0:00:59.4]} 32. Rg1 {[%clk 0:01:34.1]} 32... Qf4+ {[%clk 0:00:48.6]} 33. Qxf4 {[%clk 0:01:29.8]} 33... exf4 {[%clk 0:00:47.8]} 34. Rxg6 {[%clk 0:01:29.4]} 34... f3 {[%clk 0:00:32.9]} 35. Rxe6+ {[%clk 0:01:27.2]} 35... Kg8 {[%clk 0:00:32]} 36. Rxe7 {[%clk 0:01:26.3]} 1-0\\n'"],"rules":["chess"],"userRating":["2354"],"opponentRating":["2167"],"endTime":["1389052479"]})
        ALTERED_DATAFRAME = TEST_DATAFRAME["pgn"].apply(extractTimesFromPGN)
        EXPECTED_VALUE = "0:03:00,0:03:00,0:02:57.6,0:02:57.2,0:02:42.4,0:02:52.5,0:02:40.8,0:02:51.8,0:02:38.3,0:02:50.8,0:02:37.6,0:02:49.7,0:02:37.1,0:02:48.7,0:02:36.6,0:02:46.9,0:02:35.5,0:02:45.5,0:02:35,0:02:44,0:02:33,0:02:42.5,0:02:32.2,0:02:37.4,0:02:21.8,0:02:33,0:02:21.1,0:02:31.7,0:02:20.3,0:02:30.5,0:02:18.9,0:02:28.8,0:02:16.3,0:02:18.1,0:02:13.1,0:02:16.6,0:02:11.8,0:02:15.8,0:02:11.2,0:02:14.8,0:02:10.7,0:02:12.4,0:02:09.6,0:02:04.3,0:02:07.4,0:01:38.8,0:02:04.8,0:01:37,0:02:03.6,0:01:22.7,0:01:47.4,0:01:20.9,0:01:45.1,0:01:20.1,0:01:44.4,0:01:09.6,0:01:42,0:01:05.2,0:01:40.1,0:01:04.5,0:01:39.3,0:00:59.4,0:01:34.1,0:00:48.6,0:01:29.8,0:00:47.8,0:01:29.4,0:00:32.9,0:01:27.2,0:00:32,0:01:26.3"

        #after applying the function, does it give what is expected?
        self.assertEqual(ALTERED_DATAFRAME.loc[0],EXPECTED_VALUE)
    
    #tests that the calculateUserTimeAdvatage function works
    def testCalculateUserTimeAdvantage(self):
        #constants
        TEST_DATAFRAME = pd.DataFrame({"user":["hikaru"],"period":["2014-01"],"userColour":["white"],"userResult":["win"],"opponentResult":["resigned"],"timeControl":["180"],"pgn":["'[Event \"Live Chess\"]\\n[Site \"Chess.com\"]\\n[Date \"2014.01.06\"]\\n[Round \"-\"]\\n[White \"Hikaru\"]\\n[Black \"Godswill\"]\\n[Result \"1-0\"]\\n[CurrentPosition \"6k1/1p2R3/p1p5/8/2P1B3/1P1P1p1P/P6K/8 b - -\"]\\n[Timezone \"UTC\"]\\n[ECO \"C25\"]\\n[ECOUrl \"https://www.chess.com/openings/Vienna-Game-Max-Lange-Paulsen-Variation-3...g6-4.Bg2-Bg7\"]\\n[UTCDate \"2014.01.06\"]\\n[UTCTime \"23:50:17\"]\\n[WhiteElo \"2354\"]\\n[BlackElo \"2167\"]\\n[TimeControl \"180\"]\\n[Termination \"Hikaru won by resignation\"]\\n[StartTime \"23:50:17\"]\\n[EndDate \"2014.01.06\"]\\n[EndTime \"23:54:39\"]\\n[Link \"https://www.chess.com/game/live/692667823\"]\\n\\n1. e4 {[%clk 0:03:00]} 1... e5 {[%clk 0:03:00]} 2. Nc3 {[%clk 0:02:57.6]} 2... Nc6 {[%clk 0:02:57.2]} 3. g3 {[%clk 0:02:42.4]} 3... g6 {[%clk 0:02:52.5]} 4. Bg2 {[%clk 0:02:40.8]} 4... Bg7 {[%clk 0:02:51.8]} 5. Nge2 {[%clk 0:02:38.3]} 5... Nge7 {[%clk 0:02:50.8]} 6. O-O {[%clk 0:02:37.6]} 6... O-O {[%clk 0:02:49.7]} 7. d3 {[%clk 0:02:37.1]} 7... d6 {[%clk 0:02:48.7]} 8. h3 {[%clk 0:02:36.6]} 8... h6 {[%clk 0:02:46.9]} 9. Be3 {[%clk 0:02:35.5]} 9... Be6 {[%clk 0:02:45.5]} 10. Qd2 {[%clk 0:02:35]} 10... Qd7 {[%clk 0:02:44]} 11. Kh2 {[%clk 0:02:33]} 11... Kh7 {[%clk 0:02:42.5]} 12. Nd5 {[%clk 0:02:32.2]} 12... Nd4 {[%clk 0:02:37.4]} 13. Nxe7 {[%clk 0:02:21.8]} 13... Qxe7 {[%clk 0:02:33]} 14. c3 {[%clk 0:02:21.1]} 14... Nxe2 {[%clk 0:02:31.7]} 15. Qxe2 {[%clk 0:02:20.3]} 15... c6 {[%clk 0:02:30.5]} 16. f4 {[%clk 0:02:18.9]} 16... f5 {[%clk 0:02:28.8]} 17. Rae1 {[%clk 0:02:16.3]} 17... a6 {[%clk 0:02:18.1]} 18. fxe5 {[%clk 0:02:13.1]} 18... dxe5 {[%clk 0:02:16.6]} 19. exf5 {[%clk 0:02:11.8]} 19... Bxf5 {[%clk 0:02:15.8]} 20. g4 {[%clk 0:02:11.2]} 20... Be6 {[%clk 0:02:14.8]} 21. c4 {[%clk 0:02:10.7]} 21... Rad8 {[%clk 0:02:12.4]} 22. Be4 {[%clk 0:02:09.6]} 22... Bf7 {[%clk 0:02:04.3]} 23. b3 {[%clk 0:02:07.4]} 23... Qh4 {[%clk 0:01:38.8]} 24. Bf2 {[%clk 0:02:04.8]} 24... Qg5 {[%clk 0:01:37]} 25. Bc5 {[%clk 0:02:03.6]} 25... Be6 {[%clk 0:01:22.7]} 26. Bxf8 {[%clk 0:01:47.4]} 26... Rxf8 {[%clk 0:01:20.9]} 27. Rxf8 {[%clk 0:01:45.1]} 27... Bxf8 {[%clk 0:01:20.1]} 28. Qf2 {[%clk 0:01:44.4]} 28... Be7 {[%clk 0:01:09.6]} 29. Rf1 {[%clk 0:01:42]} 29... h5 {[%clk 0:01:05.2]} 30. gxh5 {[%clk 0:01:40.1]} 30... Qxh5 {[%clk 0:01:04.5]} 31. Qf3 {[%clk 0:01:39.3]} 31... Qg5 {[%clk 0:00:59.4]} 32. Rg1 {[%clk 0:01:34.1]} 32... Qf4+ {[%clk 0:00:48.6]} 33. Qxf4 {[%clk 0:01:29.8]} 33... exf4 {[%clk 0:00:47.8]} 34. Rxg6 {[%clk 0:01:29.4]} 34... f3 {[%clk 0:00:32.9]} 35. Rxe6+ {[%clk 0:01:27.2]} 35... Kg8 {[%clk 0:00:32]} 36. Rxe7 {[%clk 0:01:26.3]} 1-0\\n'"],"rules":["chess"],"userRating":["2354"],"opponentRating":["2167"],"endTime":["1389052479"],"timestamps":["0:03:00,0:03:00,0:02:57.6,0:02:57.2,0:02:42.4,0:02:52.5,0:02:40.8,0:02:51.8,0:02:38.3,0:02:50.8,0:02:37.6,0:02:49.7,0:02:37.1,0:02:48.7,0:02:36.6,0:02:46.9,0:02:35.5,0:02:45.5,0:02:35,0:02:44,0:02:33,0:02:42.5,0:02:32.2,0:02:37.4,0:02:21.8,0:02:33,0:02:21.1,0:02:31.7,0:02:20.3,0:02:30.5,0:02:18.9,0:02:28.8,0:02:16.3,0:02:18.1,0:02:13.1,0:02:16.6,0:02:11.8,0:02:15.8,0:02:11.2,0:02:14.8,0:02:10.7,0:02:12.4,0:02:09.6,0:02:04.3,0:02:07.4,0:01:38.8,0:02:04.8,0:01:37,0:02:03.6,0:01:22.7,0:01:47.4,0:01:20.9,0:01:45.1,0:01:20.1,0:01:44.4,0:01:09.6,0:01:42,0:01:05.2,0:01:40.1,0:01:04.5,0:01:39.3,0:00:59.4,0:01:34.1,0:00:48.6,0:01:29.8,0:00:47.8,0:01:29.4,0:00:32.9,0:01:27.2,0:00:32,0:01:26.3"]})
        ALTERED_DATAFRAME = list(TEST_DATAFRAME.apply(calculateUserTimeAdvantage,axis=1))[0]
        EXPECTED_RESULT = "0,0.0,0.4000000000000057,-10.099999999999994,-11.0,-12.5,-12.099999999999994,-11.599999999999994,-10.300000000000011,-10.0,-9.0,-9.5,-5.200000000000017,-11.199999999999989,-10.599999999999994,-10.199999999999989,-9.900000000000006,-1.799999999999983,-3.5,-4.0,-3.6000000000000227,-1.700000000000017,5.299999999999997,28.60000000000001,27.799999999999997,40.89999999999999,26.5,25.0,34.80000000000001,36.8,35.599999999999994,39.9,45.49999999999999,42.0,56.50000000000001,55.2,54.3"
        
        #after applying the function, does it give what is expected?
        self.assertEqual(ALTERED_DATAFRAME,EXPECTED_RESULT)

    #test 1 to check that the applyControlClass function works
    def testApplyControlClass1(self):
        #constants
        TEST_DATAFRAME = pd.DataFrame({"timeControl":["519+2"]})
        ALTERED_DATAFRAME = list(TEST_DATAFRAME.apply(applyControlClass,axis=1))[0]
        EXPECTED_RESULT = "Blitz"

        #after applying the function, does it give what is expected?
        self.assertEqual(ALTERED_DATAFRAME,EXPECTED_RESULT)

    #test 2 to check that the applyControlClass function works
    def testApplyControlClass2(self):
        #constants
        TEST_DATAFRAME = pd.DataFrame({"timeControl":["120+12"]})
        ALTERED_DATAFRAME = list(TEST_DATAFRAME.apply(applyControlClass,axis=1))[0]
        EXPECTED_RESULT = "Rapid"

        #after applying the function, does it give what is expected?
        self.assertEqual(ALTERED_DATAFRAME,EXPECTED_RESULT)

    #test 3 to check that the applyControlClass function works
    def testApplyControlClass3(self):
        #constants
        TEST_DATAFRAME = pd.DataFrame({"timeControl":["90+3"]})
        ALTERED_DATAFRAME = list(TEST_DATAFRAME.apply(applyControlClass,axis=1))[0]
        EXPECTED_RESULT = "Blitz"

        #after applying the function, does it give what is expected?
        self.assertEqual(ALTERED_DATAFRAME,EXPECTED_RESULT)

    #test 4 to check that the applyControlClass function works
    def testApplyControlClass4(self):
        #constants
        TEST_DATAFRAME = pd.DataFrame({"timeControl":["60+2"]})
        ALTERED_DATAFRAME = list(TEST_DATAFRAME.apply(applyControlClass,axis=1))[0]
        EXPECTED_RESULT = "Bullet"

        #after applying the function, does it give what is expected?
        self.assertEqual(ALTERED_DATAFRAME,EXPECTED_RESULT)

    #test 5 to check that the applyControlClass function works
    def testApplyControlClass5(self):
        #constants
        TEST_DATAFRAME = pd.DataFrame({"timeControl":["96+2"]})
        ALTERED_DATAFRAME = list(TEST_DATAFRAME.apply(applyControlClass,axis=1))[0]
        EXPECTED_RESULT = "Bullet"

        #after applying the function, does it give what is expected?
        self.assertEqual(ALTERED_DATAFRAME,EXPECTED_RESULT)

    #test 1 to check that the calcTime function worlks
    def testCalcTime1(self):
        #constants
        TEST_TIME = "12:34:02"
        EXPECTED_RESULT = 12*60*60+34*60+2

        #check if the function returns what was expected
        self.assertEqual(calcTime(TEST_TIME),EXPECTED_RESULT)
    
    #test 2 to check that the calcTime function worlks
    def testCalcTime2(self):
        #constants
        TEST_TIME = "00:00:10.9"
        EXPECTED_RESULT = 10.9

        #check if the function returns what was expected
        self.assertEqual(calcTime(TEST_TIME),EXPECTED_RESULT)

    #test 3 to check that the calcTime function worlks
    def testCalcTime3(self):
        #constants
        TEST_TIME = "00:00:00.2"
        EXPECTED_RESULT = 0.2

        #check if the function returns what was expected
        self.assertEqual(calcTime(TEST_TIME),EXPECTED_RESULT)

    #test 4 to check that the calcTime function worlks
    def testCalcTime4(self):
        #constants
        TEST_TIME = "00:00:30"
        EXPECTED_RESULT = 30

        #check if the function returns what was expected
        self.assertEqual(calcTime(TEST_TIME),EXPECTED_RESULT)

    #tests that the timeSpent function works
    def testTimeSpent(self):
        #constants
        TEST_DATAFRAME = pd.DataFrame({"user":["hikaru"],"period":["2014-01"],"userColour":["white"],"userResult":["win"],"opponentResult":["resigned"],"timeControl":["180"],"pgn":["'[Event \"Live Chess\"]\\n[Site \"Chess.com\"]\\n[Date \"2014.01.06\"]\\n[Round \"-\"]\\n[White \"Hikaru\"]\\n[Black \"Godswill\"]\\n[Result \"1-0\"]\\n[CurrentPosition \"6k1/1p2R3/p1p5/8/2P1B3/1P1P1p1P/P6K/8 b - -\"]\\n[Timezone \"UTC\"]\\n[ECO \"C25\"]\\n[ECOUrl \"https://www.chess.com/openings/Vienna-Game-Max-Lange-Paulsen-Variation-3...g6-4.Bg2-Bg7\"]\\n[UTCDate \"2014.01.06\"]\\n[UTCTime \"23:50:17\"]\\n[WhiteElo \"2354\"]\\n[BlackElo \"2167\"]\\n[TimeControl \"180\"]\\n[Termination \"Hikaru won by resignation\"]\\n[StartTime \"23:50:17\"]\\n[EndDate \"2014.01.06\"]\\n[EndTime \"23:54:39\"]\\n[Link \"https://www.chess.com/game/live/692667823\"]\\n\\n1. e4 {[%clk 0:03:00]} 1... e5 {[%clk 0:03:00]} 2. Nc3 {[%clk 0:02:57.6]} 2... Nc6 {[%clk 0:02:57.2]} 3. g3 {[%clk 0:02:42.4]} 3... g6 {[%clk 0:02:52.5]} 4. Bg2 {[%clk 0:02:40.8]} 4... Bg7 {[%clk 0:02:51.8]} 5. Nge2 {[%clk 0:02:38.3]} 5... Nge7 {[%clk 0:02:50.8]} 6. O-O {[%clk 0:02:37.6]} 6... O-O {[%clk 0:02:49.7]} 7. d3 {[%clk 0:02:37.1]} 7... d6 {[%clk 0:02:48.7]} 8. h3 {[%clk 0:02:36.6]} 8... h6 {[%clk 0:02:46.9]} 9. Be3 {[%clk 0:02:35.5]} 9... Be6 {[%clk 0:02:45.5]} 10. Qd2 {[%clk 0:02:35]} 10... Qd7 {[%clk 0:02:44]} 11. Kh2 {[%clk 0:02:33]} 11... Kh7 {[%clk 0:02:42.5]} 12. Nd5 {[%clk 0:02:32.2]} 12... Nd4 {[%clk 0:02:37.4]} 13. Nxe7 {[%clk 0:02:21.8]} 13... Qxe7 {[%clk 0:02:33]} 14. c3 {[%clk 0:02:21.1]} 14... Nxe2 {[%clk 0:02:31.7]} 15. Qxe2 {[%clk 0:02:20.3]} 15... c6 {[%clk 0:02:30.5]} 16. f4 {[%clk 0:02:18.9]} 16... f5 {[%clk 0:02:28.8]} 17. Rae1 {[%clk 0:02:16.3]} 17... a6 {[%clk 0:02:18.1]} 18. fxe5 {[%clk 0:02:13.1]} 18... dxe5 {[%clk 0:02:16.6]} 19. exf5 {[%clk 0:02:11.8]} 19... Bxf5 {[%clk 0:02:15.8]} 20. g4 {[%clk 0:02:11.2]} 20... Be6 {[%clk 0:02:14.8]} 21. c4 {[%clk 0:02:10.7]} 21... Rad8 {[%clk 0:02:12.4]} 22. Be4 {[%clk 0:02:09.6]} 22... Bf7 {[%clk 0:02:04.3]} 23. b3 {[%clk 0:02:07.4]} 23... Qh4 {[%clk 0:01:38.8]} 24. Bf2 {[%clk 0:02:04.8]} 24... Qg5 {[%clk 0:01:37]} 25. Bc5 {[%clk 0:02:03.6]} 25... Be6 {[%clk 0:01:22.7]} 26. Bxf8 {[%clk 0:01:47.4]} 26... Rxf8 {[%clk 0:01:20.9]} 27. Rxf8 {[%clk 0:01:45.1]} 27... Bxf8 {[%clk 0:01:20.1]} 28. Qf2 {[%clk 0:01:44.4]} 28... Be7 {[%clk 0:01:09.6]} 29. Rf1 {[%clk 0:01:42]} 29... h5 {[%clk 0:01:05.2]} 30. gxh5 {[%clk 0:01:40.1]} 30... Qxh5 {[%clk 0:01:04.5]} 31. Qf3 {[%clk 0:01:39.3]} 31... Qg5 {[%clk 0:00:59.4]} 32. Rg1 {[%clk 0:01:34.1]} 32... Qf4+ {[%clk 0:00:48.6]} 33. Qxf4 {[%clk 0:01:29.8]} 33... exf4 {[%clk 0:00:47.8]} 34. Rxg6 {[%clk 0:01:29.4]} 34... f3 {[%clk 0:00:32.9]} 35. Rxe6+ {[%clk 0:01:27.2]} 35... Kg8 {[%clk 0:00:32]} 36. Rxe7 {[%clk 0:01:26.3]} 1-0\\n'"],"rules":["chess"],"userRating":["2354"],"opponentRating":["2167"],"endTime":["1389052479"],"timestamps":["0:03:00,0:03:00,0:02:57.6,0:02:57.2,0:02:42.4,0:02:52.5,0:02:40.8,0:02:51.8,0:02:38.3,0:02:50.8,0:02:37.6,0:02:49.7,0:02:37.1,0:02:48.7,0:02:36.6,0:02:46.9,0:02:35.5,0:02:45.5,0:02:35,0:02:44,0:02:33,0:02:42.5,0:02:32.2,0:02:37.4,0:02:21.8,0:02:33,0:02:21.1,0:02:31.7,0:02:20.3,0:02:30.5,0:02:18.9,0:02:28.8,0:02:16.3,0:02:18.1,0:02:13.1,0:02:16.6,0:02:11.8,0:02:15.8,0:02:11.2,0:02:14.8,0:02:10.7,0:02:12.4,0:02:09.6,0:02:04.3,0:02:07.4,0:01:38.8,0:02:04.8,0:01:37,0:02:03.6,0:01:22.7,0:01:47.4,0:01:20.9,0:01:45.1,0:01:20.1,0:01:44.4,0:01:09.6,0:01:42,0:01:05.2,0:01:40.1,0:01:04.5,0:01:39.3,0:00:59.4,0:01:34.1,0:00:48.6,0:01:29.8,0:00:47.8,0:01:29.4,0:00:32.9,0:01:27.2,0:00:32,0:01:26.3"]})
        ALTERED_DATAFRAME = list(TEST_DATAFRAME.apply(timeSpent,axis=1))[0]
        EXPECTED_RESULT = [2.4000000000000057, 15.199999999999989, 1.5999999999999943, 2.5, 0.700000000000017, 0.5, 0.5, 1.0999999999999943, 0.5, 2.0, 0.8000000000000114, 10.399999999999977, 0.700000000000017, 0.799999999999983, 1.4000000000000057, 2.5999999999999943, 3.200000000000017, 1.299999999999983, 0.6000000000000227, 0.5, 1.0999999999999943, 2.1999999999999886, 2.6000000000000085, 1.2000000000000028, 16.19999999999999, 2.3000000000000114, 0.6999999999999886, 2.4000000000000057, 1.9000000000000057, 0.7999999999999972, 5.200000000000003, 4.299999999999997, 0.3999999999999915, 2.200000000000003, 0.9000000000000057]
        self.assertEqual(ALTERED_DATAFRAME,EXPECTED_RESULT)

#test using this pgn https://api.chess.com/pub/player/mohssenbinaddi/games/2020/04 line 726 for extractTimesFromPgn

if __name__ == "__main__":
    unittest.main()