import urllib.request
from datetime import date
import json

def addZero(num):
    if len(str(num)) == 1:
        return '0'+str(num)
    else:
        return str(num)

today = date.today()
year = str(today.year)
month = addZero(int(today.month)-2)
day = addZero(today.day+4)
scheduleYear = ''

url = 'http://data.nba.net/10s/prod/v1/today.json'
urllib.request.urlretrieve(url, 'frontpage.json')

with open('frontpage.json') as json_file:
    data = json.load(json_file)
    scheduleYear = data['seasonScheduleYear']

url = 'http://data.nba.net/10s//prod/'+str(scheduleYear)+'/teams_config.json'
urllib.request.urlretrieve(url, 'teamconfig.json')

teamIds = {}

with open('teamconfig.json') as json_file:
    data = json.load(json_file)
    for i in data['teams']['config']:
        if 'ttsName' in i:
            teamIds[i['teamId']] = ""

def getPlayers(teamId):
    players = ""
    url = 'http://data.nba.net/10s/prod/v1/'+str(int(year)-1)+'/teams/'+teamId+'/roster.json'
    urllib.request.urlretrieve(url, teamId+'.json')
    with open(teamId+'.json') as json_file:
        data = json.load(json_file)
        for p in data['league']['standard']['players']:
            players += getPlayerName(p['personId'])+","
    return players


def getPlayerName(playerId):
    url = "http://data.nba.net/10s/prod/v1/"+str(int(year)-1)+"/players.json"
    urllib.request.urlretrieve(url, 'players.json')
    with open('players.json') as json_file:
        data = json.load(json_file)
        for p in data['league']['standard']:
            if p['personId'] == playerId:
                return p['firstName']+" "+p['lastName']

for i in teamIds:
    teamIds[i] = getPlayers(i)

with open('playerDictionary.json', 'w') as file:
     file.write(json.dumps(teamIds))

print(teamIds)

'''
for index,i in enumerate(teamNames):
    result += "<tr>"
    for jindex,j in enumerate(i):
        
        playerids = getPlayers(games[index][jindex])
        playernames = []

        for i in playerids.split(","):
            playernames.append(getPlayerName(i))
            '''