There are 25 tests in the unittest file test.py\
Below are the names of the 12 functions being tested, the name(s) of the unittest function(s) testing that function, and the requirements for it to pass

Function:\
&emsp;addPlayerGames\
&emsp;testFunction:\
&emsp;&emsp;testAddPlayerGames\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;The test function calls AddPlayerGames with the username 'gmg1'. It then checks the games.csv file for all entries of gmg1 and counts how many entries the user has. It then removes all entries of gmg1 so as to not taint the next test nor the dataset. It then asserts whether the number of entries is 6, and that we have correctly looked at the expected archive\
&emsp;&emsp;&emsp;Pass Conditions:\
&emsp;&emsp;&emsp;1. The number of entries in games.csv for the user gmg1 is 6\
&emsp;&emsp;&emsp;2. The archive tested for user gmg1 was https://api.chess.com/pub/player/gmg1/games/2015/08

Function:\
&emsp;decodeb64\
&emsp;testFunction:\
&emsp;&emsp;testDecodeb64\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded test dataframe, with the values of the first entry for the user Hikaru, the test function applies the function to the dataframe. It then checks whether the decoded base64 from the test dataframe is equal to what was expected.\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. The decoded base64 from the function is equal to the known decoded base64 of the test dataframe.

Function:\
&emsp;extractTimesFromPgn\
&emsp;testFunction:\
&emsp;&emsp;testExtractTimesFromPgn\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using the same hard coded test dataframe as used in the test function testDecodeb64 (with the exception that the base64 has already been decoded), the test function applies the function to the dataframe. It then checks whether the returned time values correspond with what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. The returned clock times from the function is equal to the known clock times from the test dataframe

Function:\
&emsp;calculateUserTimeAdvantage\
&emsp;testFunction:\
&emsp;&emsp;testCalculateUserTimeAdvantage\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using the same hard coded test dataframe as used in the test function testExtractTimeFromPgn (with the exception that the clock times have already been extracted), the test function applies the function to the dataframe. It then checks whether the returned time differences correspond with what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. The returned difference in clock times from the function is equal to the known difference times from the rest dataframe.

Function:\
&emsp;applyControlClass\
&emsp;testFunctions:\
&emsp;&emsp;testApplyControlClass1\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded test dataframe with one column and one row, apply the function to the test data frame and check if the returned value is what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. With a value of 519+2 given, Blitz should be returned\
&emsp;&emsp;testApplyControlClass2\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded test dataframe with one column and one row, apply the function to the test data frame and check if the returned value is what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. With a value of 120+12 given, Rapid should be returned\
&emsp;&emsp;testApplyControlClass3\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded test dataframe with one column and one row, apply the function to the test data frame and check if the returned value is what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. With a value of 90+3 given, Blitz should be returned\
&emsp;&emsp;testApplyControlClass4\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded test dataframe with one column and one row, apply the function to the test data frame and check if the returned value is what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. With a value of 60+2 given, Bullet should be returned\
&emsp;&emsp;testApplyControlClass5\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded test dataframe with one column and one row, apply the function to the test data frame and check if the returned value is what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. With a value of 96+2 given, Bullet should be returned

Function:\
&emsp;calcTime\
&emsp;testFunctions:\
&emsp;&emsp;testCalcTime1\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded value of 12:34:02, after applying the function to it, check if the returned value is what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. The function returns 45242\
&emsp;&emsp;testCalcTime2\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded value of 00:00:10.9, after applying the function to it, check if the returned value is what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. The function returns 10.9\
&emsp;&emsp;testCalcTime3\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded value of 00:00:00.2, after applying the function to it, check if the returned value is what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. The function returns 0.2\
&emsp;&emsp;testCalcTime4\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded value of 00:00:30, after applying the function to it, check if the returned value is what was expected\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. The function returns 30

Function:\
&emsp;timeSpent\
&emsp;testFunction:\
&emsp;&emsp;testTimeSpent\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded dataframe, with all of the required columns for this function, and one row of data, after applying the function to the dataframe, the test function checks whether the returned value correctly calculates the time difference between each move\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. The time difference between each move is returned by the function

Function:\
&emsp;avgTimeSpentUser\
&emsp;testFunction:\
&emsp;&emsp;testAvgTimeSpentUser\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded dataframe, with all of the required columns for this function, the test function checks if the returned value is the averaged values returned from the timeSpent function\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. The returned averaged value is equal to 2.677142857142857

Function:\
&emsp;avgTimeSpentPerTimeControl\
&emsp;testFunction:\
&emsp;&emsp;testAvgTimeSpentPerTimeControl\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded dataframe, with all of the required columns for this function, the test function checks if the returned value is equal to the averaged value from the avgTimeSpentUser function divided by the number of seconds in the time control\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. The returned value is equal to 0.5 

Function:\
&emsp;distinguishCheatersByColour\
&emsp;testFunction:\
&emsp;&emsp;testDistinguishCheatersByColour1\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded dataframe, with two columns 'users' and 'isCheater', test if the function (with an input of [True,False,False,True], user inputs of [userA,userB,userC,userD] and colour inputs colourA, colourB) correctly associates the cheater colour with the cheaters, and the non cheater colour with the non cheaters\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. function returns [colourA,colourB,colourB,colourA]\
&emsp;&emsp;testDistinguishCheatersByColour2\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded dataframe, with two columns 'users' and 'isCheater', test if the function (with an input of [], user inputs of [] and colour inputs colourA, colourB) correctly associates the cheater colour with the cheaters, and the non cheater colour with the non cheaters\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. function returns []\
&emsp;&emsp;testDistinguishCheatersByColour3\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded dataframe, with two columns 'users' and 'isCheater', test if the function (with an input of [True,False,False,True], user inputs of [userA,userB,userC,userA] and colour inputs colourA, colourB) correctly associates the cheater colour with the cheaters, and the non cheater colour with the non cheaters\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. function returns [colourA,colourB,colourB]

Function:\
&emsp;winRatio\
&emsp;testFunction:\
&emsp;&emsp;testWinRatio1\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded dataframe, with the necessary columns including 'users' and 'userResult', test if the function (with an input of [win,loss,loss,loss]) correctly returns the win percentage\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. returns 25\
&emsp;&emsp;testWinRatio2\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded dataframe, with the necessary columns including 'users' and 'userResult', test if the function (with an input of [loss,loss,loss,loss]) correctly returns the win percentage\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. returns 0\
&emsp;&emsp;testWinRatio3\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using a hard coded dataframe, with the necessary columns including 'users' and 'userResult', test if the function (with an input of []) correctly returns the win percentage\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. returns []

Function:\
&emsp;largestWinStreak\
&emsp;testFunction:\
&emsp;&emsp;testLargestWinStreak1\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using hard coded dataframe with the necessary columns including 'userResult', test if the function (with an input of [win,win,win,loss,win,win,win,win,loss,win,win,win,win,loss,win,win]) correctly returns the largest win streak\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. returns 4\
&emsp;&emsp;testLargestWinStreak2\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using hard coded dataframe with the necessary columns including 'userResult', test if the function (with an input of [win,win,win,win,win,win,win,win,loss,win,win,win,win,loss,win,win]) correctly returns the largest win streak\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. returns 8\
&emsp;&emsp;testLargestWinStreak3\
&emsp;&emsp;&emsp;description:\
&emsp;&emsp;&emsp;using hard coded dataframe with the necessary columns including 'userResult', test if the function (with an input of [loss,loss,loss,loss,loss,loss,loss,loss,loss,loss,loss,loss,loss,loss,loss,loss]) correctly returns the largest win streak\
&emsp;&emsp;&emsp;Pass Condition:\
&emsp;&emsp;&emsp;1. returns 0