import requests
import json

def addPlayerGames(username):
    GAME_ARCHIVES_URL = "https://api.chess.com/pub/player/%s/games/archives" %(username)
    HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
    s = requests.Session()
    r = s.get(GAME_ARCHIVES_URL,headers=HEADERS)
    archives = json.loads(r.content.decode())["archives"]
    for i,archive in enumerate(archives):
        games = json.loads(s.get(archive,headers=HEADERS).content.decode())["games"]
        with open("games.csv","a") as f:
            for game in games:
                uColour = "black"
                oColour = "white"
                if game["white"]["username"].lower() == username.lower():
                    uColour = "white"
                    oColour = "black"
                try:
                    f.writelines(','.join([username,str(archive)[::-1][0:7][::-1].replace("/","-"),uColour,game[uColour]["result"],game[oColour]["result"],str(game["time_control"]),repr(game["pgn"]).replace(",","___"),game["rules"],str(game[uColour]["rating"]),str(game[oColour]["rating"]),str(game["end_time"])])+"\n")
                except Exception as e:
                    print("Suspected nonstandard game - ignoring")
                    print(e)
                    print(game)
        print("%f%% archives completed (%d/%d) for user %s" %((i+1)/len(archives)*100,i+1,len(archives),username))
with open("users.csv","r") as f:
    for user in f.readlines()[1:]:
        addPlayerGames(user)