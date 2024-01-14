#necessary imports
import pandas as pd
import base64
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

#for each row, return a string of the times in format time1,time2,time3... from PGN data
def extractTimesFromPGN(row):
    timeStr = ""
    for i in range(len(row)):
        #if this is true, we know that we are about to find a time to add
        if row[i-4:i] == "%clk":
            #if the second is a decimal, the time in the PGN is longer so adjust for that
            if row[i+9] == "}":
                timeStr += row[i+1:i+8]+","
            else:
                timeStr += row[i+1:i+10]+","
    #don't return the very last character, which is a ','
    return timeStr[:-1]

#for each game, calculate the difference in clock time for each move, and save it as a string in the following format: dif1,dif2,dif3...
def calculateUserTimeAdvantage(row):

    #if there are not timestamps or the time control is daily (time advantage doesn't apply), then return with a code of -1 to indicate that there was an issue
    if not row["timestamps"] or "/" in row["timeControl"]:
        return "-1"

    #if the time control has increment, remove it
    if "+" in row["timeControl"]:
        startingTime = int(row["timeControl"].split("+")[0])
    else:
        startingTime = int(row["timeControl"])
    blackTimes = [startingTime]
    whiteTimes = [startingTime]
    #splits the string into a list of times
    times = row["timestamps"].split(",")
    #for each time
    for i in range(len(times)):
        
        time = calcTime(times[i])

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

def decodeb64(row):
    return base64.b64decode(row).decode()

#given a time in the format hrs:mins:secs calculates in seconds how long that time is
def calcTime(timeStr):
    #gets the hrs, mins, seconds of the time
    splitTime = timeStr.split(":")
    try:
        #calculates the time in seconds (seconds can sometimes be a float)
        time = int(splitTime[0])*60*60+int(splitTime[1])*60+float(splitTime[2])
    except Exception as e:
        print(splitTime)
        print(timeStr)
        exit()
    return time

#calculates how long a user spent on each move for a game
def timeSpent(row,pov="user"):
    #is the pov person playing as white or black?
    if (pov == "user" and row["userColour"] == "white") or (pov != "user" and row["userColour"] == "black"):
        offset = 0
    else:
        offset = 1
        
    #defines the increment
    if "+" in row["timeControl"]:
        increment = int(row["timeControl"].split("+")[1])
    else:
        increment = 0
    
    #gets just the pov user's times
    times = row["timestamps"].split(",")[offset::2]
    
    #checks if there are any times
    if not times or not times[0]:
        return -1
    
    #calculates the difference in time for each of the user's moves
    prevTime = calcTime(times[0])
    diff = []
    for i in range(1,len(times)):
        intTime = calcTime(times[i])
        diff.append(prevTime-intTime+increment)
        prevTime = intTime
    return diff

#calulates the mean time between moves per game
def avgTimeSpentUser(row):
    #gets the list of time spent per move for the user
    diff = timeSpent(row)

    #if there was an issue
    if diff == -1 or not diff:
        return -1
    
    #returns the mean time spent per move
    return sum(diff)/len(diff)

#divides the avergage time spent per move by the time control
def avgTimeSpentPerTimeControl(row):
    
    #gets the starting time and the increment
    if "+" in row["timeControl"]:
        increment = int(row["timeControl"].split("+")[1])
        startingTime = int(row["timeControl"].split("+")[0])
    else:
        increment = 0
        startingTime = int(row["timeControl"])
    
    #counts how many moves there were
    numberOfMoves = int(row["timestamps"].count(":")/2)

    #returns the average time spent per move divided by the time control
    return row["avgTimeSpentUser"]/(startingTime + increment*numberOfMoves)

#returns an array of colours with cheaters being one colour and non cheaters being another
def distinguishCheatersByColour(df,cheaterColour,otherColour):
    colours = []
    
    #for each user
    for user in sorted(df["user"].unique()):

        #if the user is a cheater add a cheater colour, otherwise add a non cheater colour 
        if df[df["user"]==user]["isCheater"].unique()[0]:
            colours.append(cheaterColour)
        else:
            colours.append(otherColour)
    return colours

#calculates how many wins as a percentage the user has
def winRatio(df):
    
    #get the user wins
    wins = df[df["userResult"]=="win"].groupby("user").count()["period"]
    
    #count how many games they played
    total = df.groupby("user").count()["period"]

    #return the percentage of games won
    return wins/total*100

#associates a time control with a rating class
def applyControlClass(row):

    #the number of moves each game will average
    EXPECTED_NUMBER_OF_MOVES = 40

    #calculates the starting time and the increment
    if "+" in row["timeControl"]:
        starting,increment = row["timeControl"].split("+")
        starting,increment = int(starting),int(increment)
    else:
        starting = int(row["timeControl"])
        increment = 0

    #uses the starting time and the increment to calculate how long each game will be on average. This is then used to classify the game
    calc = starting +increment*EXPECTED_NUMBER_OF_MOVES

    #classify the game based on how long it normally takes in seconds
    if calc < 180:
        controlType = "Bullet"
    elif calc < 600:
        controlType = "Blitz"
    else:
        controlType = "Rapid"
    return controlType

#calculate a user's largest win streak
def largestWinStreak(df,user):

    userWinStreaks = {}

    #filter the dataframe only the user's games
    userGames = df[df["user"]==user]

    #for each rating type
    for ratingType in userGames["Control Classification"].unique():

        #get the dataframe of games for that rating type and sort by the order which the games were played in
        games = userGames[userGames["Control Classification"]==ratingType].sort_values(by="endTime")
        games.reset_index(drop=True)
        wins = 0
        bestWins = 0

        #for each game
        for index in games.index:

            #if it's a win then add 1 to the current win streak
            if games["userResult"][index] == "win":
                wins += 1

            #otherwise if it's a new best winstreak, set it as the new win streak
            elif wins > bestWins:
                bestWins = wins
                wins = 0

            #else, we don't care about it
            else:
                wins = 0
        
        #store the user's best winstreak for the rating type
        userWinStreaks[ratingType] = bestWins

    #return the best winstreak for each rating type
    return userWinStreaks

#when importing for unittesting, we don't want to cause the program to hang by running this
if __name__ == "__main__":
    #constants
    CHEATER_COLOUR = "#ff00ff"
    NON_CHEATER_COLOUR = "#00ff00"
    WINDOW_SIZE = 5 #rolling mean size

    #load in data
    chunks = pd.read_csv("games_new.csv",header=None,names=["user","period","userColour","userResult","opponentResult","timeControl","pgn","rules","userRating","opponentRating","endTime","rated"],dtype={"userRating":int,"opponentRating":int,"endTime":int},chunksize=100000)
    gamesDf = pd.concat(chunks)
    users = pd.read_csv("users.csv")
    users = users.rename(columns={"Usernames":"user","Title":"title","isCheater?":"isCheater"})
    gamesDf = gamesDf.merge(users,on="user")
    #filter for only games we care about
    
    #remove all the daily games
    mask = ~gamesDf['timeControl'].str.contains('/')
    gamesDf = gamesDf[mask]
    
    #only consider games which weren't abandoned
    gamesDf = gamesDf[(gamesDf["userResult"] != "abandoned")&(gamesDf["opponentResult"] != "abandoned")]
    
    #only consider games where the time control has increment or is at least 60 seconds
    gamesDf = gamesDf[(gamesDf["timeControl"].str.len() >= 3) | (gamesDf["timeControl"].str[0] == "6") | (gamesDf["timeControl"].str[0] == "7") | (gamesDf["timeControl"].str[0] == "8") | (gamesDf["timeControl"].str[0] == "9") ]
    
    #add calculated columns
    gamesDf["pgn"] = gamesDf["pgn"].apply(decodeb64)
    gamesDf["timestamps"] = gamesDf["pgn"].apply(extractTimesFromPGN)
    gamesDf["timeAdvantage"] = gamesDf.apply(calculateUserTimeAdvantage,axis=1)
    gamesDf["avgTimeSpentUser"] = gamesDf.apply(avgTimeSpentUser,axis=1)
    gamesDf["avgTimeSpentDivideTimeControl"] = gamesDf.apply(avgTimeSpentPerTimeControl,axis=1)
    gamesDf["Control Classification"] = gamesDf.apply(applyControlClass,axis=1)


    #separate cheater and non-cheater dataframes
    nonCheaterDf = gamesDf[gamesDf["isCheater"] == False]
    cheaterDf = gamesDf[gamesDf["isCheater"] == True]

    #graphs

    #win ratio of all players, with cheaters highlighted in purple and non-cheaters highlighted in green (headline figure)

    #calculate the win ratio of each user
    winRatioAll = winRatio(gamesDf)
    winRatioAllList = list(winRatioAll)

    #sort the win ratios in descending order
    sortedWinRatioAll = sorted(winRatioAll,reverse=True)

    #associate the correct users and colours based off of the newly sorted win ratios
    colours = distinguishCheatersByColour(gamesDf,CHEATER_COLOUR,NON_CHEATER_COLOUR)
    user = []
    colour = []
    for item in sortedWinRatioAll:
        index = winRatioAllList.index(item)
        user.append(winRatioAll.index[index])
        colour.append(colours[index])
    #plot the graph
    print(1)
    plt.figure(figsize=(15,7))
    plt.bar(user,sortedWinRatioAll,color=colour)
    plt.xticks(rotation=90)
    plt.legend(handles=[Patch(facecolor=CHEATER_COLOUR,label="Cheater"),Patch(facecolor=NON_CHEATER_COLOUR,label="Non Cheater")])
    plt.title("Win Percentage for each user")
    plt.ylabel("Win Percentage")
    plt.xlabel("User")
    plt.show()

    #how each game ended for all users

    #check how each game ended from the user's point of view
    gamesEnded = []
    dictionary = {}
    for result in gamesDf["userResult"].unique():
        gamesEnded.append(gamesDf.groupby("userResult").count()["user"][result])
        dictionary[gamesEnded[-1]] = result

    #sort the game results in descending order 
    gamesEnded = sorted(gamesEnded,reverse=True)

    #associate the correct labels based off of the newly sorted games
    results = [dictionary[value] for value in gamesEnded]

    #plot the graph
    print(2)
    plt.bar(results,gamesEnded)
    plt.xticks(rotation=90)
    plt.ylabel("Total Games")
    plt.xlabel("Game Results")
    plt.title("How each game ended")
    plt.show()

    #how each game ended for non-cheating users

    #check how each game ended from the user's point of view
    gamesEnded = []
    dictionary = {}
    for result in nonCheaterDf["userResult"].unique():
        gamesEnded.append(nonCheaterDf.groupby("userResult").count()["user"][result])
        dictionary[gamesEnded[-1]] = result
    
    #sort the game results in descending order 
    gamesEnded = sorted(gamesEnded,reverse=True)

    #associate the correct labels based off of the newly sorted games
    results = [dictionary[value] for value in gamesEnded]

    #plot the graph
    print(3)
    plt.bar(results,gamesEnded)
    plt.xticks(rotation=90)
    plt.ylabel("Total Games")
    plt.xlabel("Game Results")
    plt.title("How each game ended for non cheaters")
    plt.show()

    #how each game ended for cheating users

    #check how each game ended from the user's point of view
    gamesEnded = []
    dictionary = {}
    for result in cheaterDf["userResult"].unique():
        gamesEnded.append(cheaterDf.groupby("userResult").count()["user"][result])
        dictionary[gamesEnded[-1]] = result

    #sort the game results in descending order 
    gamesEnded = sorted(gamesEnded,reverse=True)

    #associate the correct labels based off of the newly sorted games
    results = [dictionary[value] for value in gamesEnded]

    #plot the graph
    print(4)
    plt.bar(results,gamesEnded)
    plt.xticks(rotation=90)
    plt.ylabel("Total Games")
    plt.xlabel("Game Results")
    plt.title("How each game ended for cheaters")
    plt.show()

    #plot how quick a player is moving on average (standardised for all time controls)

    #get the mean time spent per player
    meanTimeSpentAll = gamesDf.groupby("user")["avgTimeSpentDivideTimeControl"].mean()
    meanTimeSpentAllList = list(meanTimeSpentAll)

    #sort the mean time spent in ascending order
    sortedMeanTimeSpentAll = sorted(meanTimeSpentAll)
    colours = distinguishCheatersByColour(gamesDf,CHEATER_COLOUR,NON_CHEATER_COLOUR)

    #now correctly put names and colours in order based on the newly sorted mean time order
    user = []
    colour = []
    for item in sortedMeanTimeSpentAll:
        index = meanTimeSpentAllList.index(item)
        user.append(meanTimeSpentAll.index[index])
        colour.append(colours[index])

    #plot the graph
    print(5)
    plt.figure(figsize=(15,7))
    plt.bar(user,sortedMeanTimeSpentAll,color=colour)
    plt.xticks(rotation=90)
    plt.legend(handles=[Patch(facecolor=CHEATER_COLOUR,label="Cheater"),Patch(facecolor=NON_CHEATER_COLOUR,label="Non Cheater")])
    plt.title("Mean number of seconds spent per game divided by time control")
    plt.ylabel("Mean Time Spent / Time Control (seconds)")
    plt.xlabel("User")
    plt.show()

    #plot the best winstreak per time control type per player

    #get a list of dictionaries which each dictionary having an entry of the user and their bullet,blitz, and rapid best winstreak
    winStreaks = []
    for user in gamesDf["user"].unique():
        dictionary = largestWinStreak(gamesDf[gamesDf["rated"]==True],user)
        dictionary["user"] = user
        winStreaks.append(dictionary)

    #for each ratingType
    for ratingType in list(gamesDf["Control Classification"].unique()):
        streaks = []
        userStreak = {}

        #get the streaks for that rating type and associate each streak number with a username
        for d in winStreaks:
            try:
                streaks.append(d[ratingType])
                if d["user"] is None:
                    print("issue")
                    print(d)
                if d[ratingType] in userStreak:
                    userStreak[d[ratingType]].append(d["user"])
                else:
                    userStreak[d[ratingType]] = [d["user"]]
            except Exception as e:
                pass
        #sort the streaks in descending order
        streaks = sorted(streaks, reverse=True)
        user = []
        colour = []
        usedIndicies = []
        #now correctly put names and colours in order based on the newly sorted streaks order
        for item in streaks:
            if streaks.index(item) in usedIndicies:
                continue
            else:
                usedIndicies.append(streaks.index(item))
            indices = [i for i, x in enumerate(streaks) if x == item]
            for i,index in enumerate(indices):
                username = userStreak[streaks[index]][i]
                user.append(username)
                if gamesDf[gamesDf["user"]==username]["isCheater"].iloc[0]:
                    userColour = "#ff00ff"
                else:
                    userColour = "#00ff00"
                colour.append(userColour)
        
        #plot the graph
        print(6)
        plt.bar(user,streaks,color=colour)
        plt.title("Best User Winstreak (%s rating type)"%(ratingType))
        plt.legend(handles=[Patch(facecolor="#ff00ff",label="Cheater"),Patch(facecolor="#33ff33",label="Non Cheater")])
        plt.xticks(rotation=90)
        plt.ylabel("Longest Winstreak")
        plt.xlabel("Username")
        plt.show()

    #plot the rating change of each cheater per rating classification
    
    #for each rating type
    for ratingType in cheaterDf["Control Classification"].unique():

        #set the starting point of the x-axis
        games = 0

        #for each cheater
        for user in cheaterDf["user"].unique():

            #calculate their n-point rolling average of their rating across all of their games
            mean = cheaterDf[(cheaterDf["user"]==user)&(cheaterDf["Control Classification"]==ratingType)&(cheaterDf["rated"]==True)].sort_values(by="endTime")["userRating"].rolling(window=WINDOW_SIZE).mean()
            
            #plot the mean line with x values from the starting point up to the number of points in the mean line
            plt.plot(range(games,len(mean)+games),mean, label=user)

            #increase the next starting point to the end of the most reccent line + 1
            games += len(mean)+1
        print(7)
        #plot the remaining graph info
        plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1))
        plt.xlabel("Game Number")
        plt.ylabel("%d point moving average of Rating Value" %(WINDOW_SIZE))
        plt.title("Cheater Average Rating Change (%s)" %(ratingType))
        plt.show()
    
    #plot the rating change of each cheater per rating classification

    #for each rating type
    for ratingType in nonCheaterDf["Control Classification"].unique():

        #set the starting point of the x-axis
        games = 0

        #for each non-cheater
        for user in nonCheaterDf["user"].unique():

            #calculate their n-point rolling average of their rating across all of their games
            mean = nonCheaterDf[(nonCheaterDf["user"]==user)&(nonCheaterDf["Control Classification"]==ratingType)&(nonCheaterDf["rated"]==True)].sort_values(by="endTime")["userRating"].rolling(window=WINDOW_SIZE).mean()
            
            #plot the mean line with x values from the starting point up to the number of points in the mean line
            plt.plot(range(games,len(mean)+games),mean, label=user)

            #increase the next starting point to the end of the most reccent line + 1
            games += len(mean)+1

        #plot the remaining graph info
        print(8)
        plt.legend(bbox_to_anchor=(1.15, 1))
        plt.xlabel("Game Number")
        plt.ylabel("%d point moving average of Rating Value" %(WINDOW_SIZE))
        plt.title("Non Cheaters Average Rating Change (%s)" %(ratingType))
        plt.show()