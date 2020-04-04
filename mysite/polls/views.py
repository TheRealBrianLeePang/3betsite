from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
from datetime import date
import json
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from copy import copy, deepcopy
import os.path
from os import path
import ast

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
savedDict = {}
def getPlayers(teamId):
    print("SKIPPING APIS")
    if path.exists("players"+year+month+day+".txt"):
        with open("players"+year+month+day+".txt", 'r') as f:
            s = f.read()
            tempDict = ast.literal_eval(s)
        return tempDict[teamId]
    else:
        print("ACCESSING APIS")
        teamDict = commonteamroster.CommonTeamRoster(teamId).get_dict()
        players = ""
        for i in teamDict["resultSets"][0]["rowSet"]:
            players+=(i[3])+", "
        savedDict[teamId] = players
        if len(savedDict) == len(teamNames) * 2:
            print(teamNames)
            with open("players"+year+month+day+".txt", 'w') as f:
                print(savedDict, file=f)
        return players


result = "<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>NBA Games</title><link rel='stylesheet' href='https://unpkg.com/purecss@1.0.1/build/pure-min.css'><style>img{width: 5%;display: block; margin-left: auto; margin-right: auto;}</style></head><body><h1 align='center'>NBA Games Happening Today:</h1><table align='center' class='pure-table pure-table-bordered'><thead><tr><th>Home Team</th><th>Away Team</th></thead>"

for index,i in enumerate(teamNames):
    result += "<tr>"
    for jindex,j in enumerate(i):
        result+="<td>" + str(j) +"</td>"
    result += "</tr>"
result+= "</table><br><img src='http://loodibee.com/wp-content/uploads/nba-logo-transparent.png' alt='NBA logo'></body></html>"


def index(request):
    return HttpResponse(result)
