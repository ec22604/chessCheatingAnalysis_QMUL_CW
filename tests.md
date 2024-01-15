There are 23 tests in the unittest file test.py\
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
        testExtractTimesFromPgn\
            description:\
            using the same hard coded test dataframe as used in the test function testDecodeb64 (with the exception that the base64 has already been decoded), the test function applies the function to the dataframe. It then checks whether the returned time values correspond with what was expected\
            Pass Condition:\
            1. The returned clock times from the function is equal to the known clock times from the test dataframe

Function:\
    calculateUserTimeAdvantage\
    testFunction:\
        testCalculateUserTimeAdvantage\
            description:\
            using the same hard coded test dataframe as used in the test function testExtractTimeFromPgn (with the exception that the clock times have already been extracted), the test function applies the function to the dataframe. It then checks whether the returned time differences correspond with what was expected\
            Pass Condition:\
            1. The returned difference in clock times from the function is equal to the known difference times from the rest dataframe.

Function:\
    applyControlClass\
    testFunctions:\
        testApplyControlClass1\
            description:\
            using a hard coded test dataframe with one column and one row, apply the function to the test data frame and check if the returned value is what was expected\
            Pass Condition:\
            1.
        testApplyControlClass2\
            description:\
            \
            Pass Condition:\
            1. 
        testApplyControlClass3\
            description:\
            \
            Pass Condition:\
            1. 
        testApplyControlClass4\
            description:\
            \
            Pass Condition:\
            1. 
        testApplyControlClass5\
            description:\
            \
            Pass Condition:\
            1. 
Function:\
    \
    testFunction:\
        test\
        description:\
        \
        Pass Condition:\
        1. 

Function:\
    \
    testFunction:\
        test\
        description:\
        \
        Pass Condition:\
        1. 

Function:\
    \
    testFunction:\
        test\
        description:\
        \
        Pass Condition:\
        1. 

Function:\
    \
    testFunction:\
        test\
        description:\
        \
        Pass Condition:\
        1. 

Function:\
    \
    testFunction:\
        test\
        description:\
        \
        Pass Condition:\
        1. 

Function:\
    \
    testFunction:\
        test\
        description:\
        \
        Pass Condition:\
        1. 

Function:\
    \
    testFunction:\
        test\
        description:\
        \
        Pass Condition:\
        1. 