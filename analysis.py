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

gamesDf = pd.read_csv("games.csv")
threePlusZero = gamesDf.where((gamesDf["timeControl"]=="180")&(gamesDf["rules"] == "chess")).dropna()
print("there are %d games of 3+0 standard variant" %(len(threePlusZero)))
threePlusZero["timestamps"] = threePlusZero["pgn"].apply(extractTimesFromPGN)
print(threePlusZero.head())