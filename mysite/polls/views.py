from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
from datetime import date
import json
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from copy import copy, deepcopy

def addZero(num):
    if len(str(num)) == 1:
        return '0'+str(num)
    else:
        return str(num)



today = date.today()
year = str(today.year)
month = addZero(today.month)
day = addZero(today.day)
scheduleYear = ''
games = []

url = 'http://data.nba.net/10s/prod/v1/'+year+month+day+'/scoreboard.json'
urllib.request.urlretrieve(url, 'test.json')
url = 'http://data.nba.net/10s/prod/v1/today.json'
urllib.request.urlretrieve(url, 'frontpage.json')

with open('test.json') as json_file:
    data = json.load(json_file)
    for p in data['games']:
        games.append([p['vTeam']['teamId'],p['hTeam']['teamId']])
with open('frontpage.json') as json_file:
    data = json.load(json_file)
    scheduleYear = data['seasonScheduleYear']
url = 'http://data.nba.net/10s//prod/'+str(scheduleYear)+'/teams_config.json'
urllib.request.urlretrieve(url, 'teamconfig.json')
teamNames = deepcopy(games)
for index,i in enumerate(games):
    for jindex,j in enumerate(i):
        name = teams.find_team_name_by_id(j)
        teamNames[index][jindex] = name['full_name']
def getPlayers(teamId):
    teamDict = commonteamroster.CommonTeamRoster(teamId).get_dict()
    players = ""
    for i in teamDict["resultSets"][0]["rowSet"]:
        players+=(i[3])+", "
    return players

result = ""
for index,i in enumerate(teamNames):
    for jindex,j in enumerate(i):
        result+=str(j)
        if(jindex == 0):
            result+= " -- "+getPlayers(games[index][jindex]) + "<br>"
            result+="VS <br>"
        else:
            result+= " -- "+getPlayers(games[index][jindex]) + "<br>"
    result+="<br>"

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return HttpResponse(result)

