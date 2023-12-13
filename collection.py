#necessary imports
import requests
import json
import base64

#adds all the games for a particular user to the games.csv file
def addPlayerGames(username):
    #constants used for the API
    GAME_ARCHIVES_URL = "https://api.chess.com/pub/player/%s/games/archives" %(username)
    HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
    s = requests.Session()
    #gets all the urls to parse to the API for each month that the user played a game in (called an archive)
    r = s.get(GAME_ARCHIVES_URL,headers=HEADERS)
    #parses the response and stores each url as a list of strings
    archives = json.loads(r.content.decode())["archives"]
    for i,archive in enumerate(archives):
        #gets all the information about all the games for a particular archive
        games = json.loads(s.get(archive,headers=HEADERS).content.decode())["games"]
        with open("games.csv","a",encoding="UTF-8") as f:
            for game in games:
                #assumes a user's colour and opponent's colour
                uColour = "black"
                oColour = "white"
                #changes the colours if wrong
                if game["white"]["username"].lower() == username.lower():
                    uColour = "white"
                    oColour = "black"
                try:
                    #attempts to write all of the necessary information about the game to the file. 
                    f.writelines(','.join([username,str(archive)[::-1][0:7][::-1].replace("/","-"),uColour,game[uColour]["result"],game[oColour]["result"],str(game["time_control"]),base64.b64encode(repr(game["pgn"]).encode()).decode(),game["rules"],str(game[uColour]["rating"]),str(game[oColour]["rating"]),str(game["end_time"])])+"\n")
                except Exception as e:
                    #will through an error if the game doesn't have a pgn, which only happens when the rules of the game are not standard, but prints out the error anyways as a log of games which throw an error
                    print("Suspected nonstandard game - ignoring")
                    print(e)
        print("%f%% archives completed (%d/%d) for user %s" %((i+1)/len(archives)*100,i+1,len(archives),username))
    return archives
#when importing the function for unittesting, we don't want to run all the users, so __name__ check is put in place
if __name__ == "__main__":
    with open("users.csv","r") as f:
        count = 1
        for user in f.readlines()[1:]:
            addPlayerGames(user.split(",")[0])
            print("completed user %s (%f%% - %d/%d)" %(user.split(",")[0],count/60*100,count,60))
            count += 1
    