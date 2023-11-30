import matplotlib.pyplot as plt
import pandas as pd
def extractTimesFromPGN(row):
    timeStr = ""
    for i in range(len(row)):
        if row[i-3:i] == "clk":
            if row[i+9] == "}":
                timeStr += row[i+1:i+8]+","
            else:
                timeStr += row[i+1:i+10]+","
    return timeStr
def calculateHikaruTimeAdvantage(row):
    blackTimes = []
    whiteTimes = []
    times = row["timestamps"].split(",")
    for i in range(len(times)):
        splitTime = times[i].split(":")
        try:
            time = int(splitTime[0])*60*60+int(splitTime[1])*60+float(splitTime[2])
        except Exception as e:
            print(splitTime)
            print(times[i])
            print(row["timestamps"])
            exit()
        if i % 2 == 0:
            whiteTimes.append(time)
        else:
            blackTimes.append(time)
    if "timeout" in row["opponentResult"]  or "timeout" in row["hikaruResult"]:
        if len(whiteTimes) == len(blackTimes):
            whiteTimes.append(0)
            blackTimes.append(blackTimes[-1])
        else:
            blackTimes.append(0)
    elif len(blackTimes) != len(whiteTimes):
        if len(blackTimes) < len(whiteTimes):
            blackTimes.append(blackTimes[-1])
        else:
            print("Somehow black made an extra move?")
            print(row)
    calc = []
    if row["hikaruColour"] == "white":
        #left minus right
        
        for i in range(len(whiteTimes)):
            calc.append(str(whiteTimes-blackTimes))
        
    else:
        #right minus left
        for i in range(len(whiteTimes)):
            calc.append(str(blackTimes-whiteTimes))
    return ','.join(calc)
gamesDf = pd.read_csv("games.csv")
threePlusZero = gamesDf.where((gamesDf["timeControl"]=="180")&(gamesDf["rules"] == "chess")).dropna()
print("there are %d games of 3+0 standard variant" %(len(threePlusZero)))
threePlusZero["timestamps"] = threePlusZero["pgn"].apply(extractTimesFromPGN)
threePlusZero["timeAdvantage"] = threePlusZero.apply(calculateHikaruTimeAdvantage,axis=1)
print(threePlusZero.head())