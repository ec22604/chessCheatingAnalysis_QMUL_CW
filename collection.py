from telnetlib import GA
import requests
import json
GAME_ARCHIVES_URL = "https://api.chess.com/pub/player/hikaru/games/archives"
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
s = requests.Session()
r = s.get(GAME_ARCHIVES_URL,headers=HEADERS)
archives = json.loads(r.content.decode())["archives"]
for archive in archives:
    games = json.loads(s.get(archive,headers=HEADERS).content.decode())["games"]
    with open("games.csv","a") as f:
        for game in games:
            hColour = "Black"
            oColour = "White"
            if game["white"]["username"] == "Hikaru":
                hColour = "White"
                oColour = "Black"
            
            f.writelines(','.join([archive[-1:-8].replace("/","-"),hColour,game[hColour]["result"],game]))

    exit()