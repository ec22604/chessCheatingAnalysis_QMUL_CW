import requests
import json
import base64
def addPlayerGames(username):
    GAME_ARCHIVES_URL = "https://api.chess.com/pub/player/%s/games/archives" %(username)
    HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
    s = requests.Session()
    r = s.get(GAME_ARCHIVES_URL,headers=HEADERS)
    archives = json.loads(r.content.decode())["archives"]
    for i,archive in enumerate(archives):
        games = json.loads(s.get(archive,headers=HEADERS).content.decode())["games"]
        with open("C:\\Users\\ec22604\\Documents\\games.csv","a",encoding="UTF-8") as f:
            for game in games:
                uColour = "black"
                oColour = "white"
                if game["white"]["username"].lower() == username.lower():
                    uColour = "white"
                    oColour = "black"
                try:
                    f.writelines(','.join([username,str(archive)[::-1][0:7][::-1].replace("/","-"),uColour,game[uColour]["result"],game[oColour]["result"],str(game["time_control"]),base64.b64encode(repr(game["pgn"]).encode()).decode(),game["rules"],str(game[uColour]["rating"]),str(game[oColour]["rating"]),str(game["end_time"])])+"\n")
                except Exception as e:
                    print("Suspected nonstandard game - ignoring")
                    print(e)
        print("%f%% archives completed (%d/%d) for user %s" %((i+1)/len(archives)*100,i+1,len(archives),username))
    return archives
if __name__ == "__main__":
    with open("users.csv","r") as f:
        count = 1
        for user in f.readlines()[1:]:
            addPlayerGames(user.split(",")[0])
            print("completed user %s (%f%% - %d/%d)" %(user.split(",")[0],count/60*100,count,60))
            count += 1
    