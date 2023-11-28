from telnetlib import GA
import requests
import json
GAME_ARCHIVES_URL = "https://api.chess.com/pub/player/hikaru/games/archives"
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
s = requests.Session()
r = s.get(GAME_ARCHIVES_URL,headers=HEADERS)
archives = json.loads(r.content.decode())["archives"]
for i,archive in enumerate(archives):
    games = json.loads(s.get(archive,headers=HEADERS).content.decode())["games"]
    with open("games.csv","a") as f:
        for game in games:
            hColour = "black"
            oColour = "white"
            if game["white"]["username"] == "Hikaru":
                hColour = "white"
                oColour = "black"
            try:
                f.writelines(','.join([str(archive)[::-1][0:7][::-1].replace("/","-"),hColour,game[hColour]["result"],game[oColour]["result"],str(game["time_control"]),repr(game["pgn"]),game["rules"],str(game[hColour]["rating"]),str(game[oColour]["rating"]),str(game["end_time"])])+"\n")
            except Exception as e:
                print(e)
                print(game)
    print("%f%% archives completed (%d/%d)" %((i+1)/len(archives)*100,i+1,len(archives)))