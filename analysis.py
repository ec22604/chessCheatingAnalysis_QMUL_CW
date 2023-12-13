#necessary imports
import pandas as pd

#for each row, return a string of the times in format time1,time2,time3... from PGN data
def extractTimesFromPGN(row):
    timeStr = ""
    for i in range(len(row)):
        #if this is true, we know that we are about to find a time to add
        if row[i-3:i] == "clk":
            #if the second is a decimal, the time in the PGN is longer so adjust for that
            if row[i+9] == "}":
                timeStr += row[i+1:i+8]+","
            else:
                timeStr += row[i+1:i+10]+","
    #don't return the very last character, which is a ','
    return timeStr[:-1]

#for each game, calculate the difference in clock time for each move, and save it as a string in the following format: dif1,dif2,dif3...
def calculateUserTimeAdvantage(row):
    blackTimes = []
    whiteTimes = []

    #splits the string into a list of times
    times = row["timestamps"].split(",")
    #for each time
    for i in range(len(times)):
        #gets the hrs, mins, seconds of the time
        splitTime = times[i].split(":")
        try:
            #calculates the time in seconds (seconds can sometimes be a float)
            time = int(splitTime[0])*60*60+int(splitTime[1])*60+float(splitTime[2])
        except Exception as e:
            print(splitTime)
            print(times[i])
            print(row["timestamps"])
            exit()
        #it alternates white and black with white moving first
        if i % 2 == 0:
            whiteTimes.append(time)
        else:
            blackTimes.append(time)

    #if a timeout occurs, then there is missing data
    if "timeout" in row["opponentResult"]  or "timeout" in row["userResult"]:
        #if there is an equal number of times, white has timedout and should be on 0 seconds, with black on their prevous time
        if len(whiteTimes) == len(blackTimes):
            whiteTimes.append(0)
            blackTimes.append(blackTimes[-1])
        #otherwise black timed out and should be on 0
        else:
            blackTimes.append(0)
    #if the times are still not the same, then white has made an extra move before a resignation/stalemate/etc
    elif len(blackTimes) != len(whiteTimes):
        #if this returns False, black has somehow made an extra move over white, and there is likely some logic going wrong
        if len(blackTimes) < len(whiteTimes):
            blackTimes.append(blackTimes[-1])
        else:
            print("Somehow black made an extra move?")
            print(row)

    calc = []
    #calculates the difference in times from the perspective of the user, if they're white, it's whiteTimes - blackTimes. If they're black, it's blackTimes - whiteTimes
    if row["userColour"] == "white":
        #left minus right
        for i in range(len(whiteTimes)):
            calc.append(str(whiteTimes[i]-blackTimes[i]))
    else:
        #right minus left
        for i in range(len(whiteTimes)):
            calc.append(str(blackTimes[i]-whiteTimes[i]))

    #return the differences as a string in the format dif1,dif2,dif3...
    return ','.join(calc)
gamesDf = pd.read_csv("games.csv")