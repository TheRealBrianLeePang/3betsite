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
arenas = []

url = 'http://data.nba.net/10s/prod/v1/'+year+month+day+'/scoreboard.json'
print(url)
urllib.request.urlretrieve(url, 'test.json')
url = 'http://data.nba.net/10s/prod/v1/today.json'
urllib.request.urlretrieve(url, 'frontpage.json')

with open('test.json') as json_file:
    data = json.load(json_file)
    for p in data['games']:
        games.append([p['vTeam']['teamId'],p['hTeam']['teamId']])
        arenas.append(p['arena']['name']+ ", " + p['arena']['city'])

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
    if path.exists("players"+year+month+day+".txt"):
        
        with open("players"+year+month+day+".txt", 'r') as f:
            s = f.read()
            tempDict = ast.literal_eval(s)
        return tempDict[teamId]
    else:

        players = ""
        url = 'http://data.nba.net/10s/prod/v1/'+str(int(year)-1)+'/teams/'+teamId+'/roster.json'
        urllib.request.urlretrieve(url, teamId+'.json')
        with open(teamId+'.json') as json_file:
            data = json.load(json_file)
            for p in data['league']['standard']['players']:
                players += p['personId']+","
        savedDict[teamId] = players
        if len(savedDict) == len(teamNames) * 2:
            print(teamNames)
            with open("players"+year+month+day+".txt", 'w') as f:
                print(savedDict, file=f)
        return players
        '''
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
        '''

def getPlayerName(playerId):
    url = "http://data.nba.net/10s/prod/v1/"+str(int(year)-1)+"/players.json"
    urllib.request.urlretrieve(url, 'players.json')
    with open('players.json') as json_file:
        data = json.load(json_file)
        for p in data['league']['standard']:
            if p['personId'] == playerId:
                return p['firstName']+" "+p['lastName']


result = "<!DOCTYPE html>"
result += "<html>"
result += "<head>"
result += "<meta charset='utf-8'>"
result += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
result += "<title>NBA Games</title>"
result += "<link rel='stylesheet' href='https://unpkg.com/purecss@1.0.1/build/pure-min.css'>"
result += "<style>img{display: block; margin-left: auto; margin-right: auto;}"
result += ".tooltip {position: relative; display: inline-block; border-bottom: 1px dotted black;}"
result += ".tooltip .tooltiptext {visibility: hidden; width: 200px; background-color: black; color: white; text-align: center; border-radius: 6px; padding: 5px 0; top: 100%; left: 50%; margin-left: -100px; position: absolute; z-index: 1;}"
result += ".tooltip:hover .tooltiptext {visibility: visible;}"
result += ".center {margin: 0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);}"
result += "body{color: white; font-weight: bold; background-image: url('https://burlingtonvt.citymomsblog.com/wp-content/uploads/2020/01/lit-basketball-stadium-with-fans-empty-court-scaled.jpg'); background-attachment: fixed; background-position: center; background-repeat: no-repeat; background-size: cover;}</style>"
result += "</head><div class='center'><body><h1 align='center'>NBA Games Happening Today:</h1>"
result += "<h3 style = 'text-align:center'><i>(If COVID-19 didn't exist!)</i></h3>"
result += "<table align='center' class='pure-table pure-table-bordered'><thead><tr><th>Away Team</th><th>Home Team</th><th>Location</th><th>Winner/Spread</th></thead>"

for index,i in enumerate(teamNames):
    result += "<tr>"
    for jindex,j in enumerate(i):
        
        playerids = getPlayers(games[index][jindex])
        playernames = []

        for i in playerids.split(","):
            playernames.append(getPlayerName(i))
        
        result += "<td>"
        
        if jindex % 2 == 0:
            result += "<div class='tooltip'>" + str(j) + "<span class='tooltiptext'>" 
            for p in playernames:
                if str(p) != "None":
                    result += str(p) + "<br>"
            result += "</span></div></td>"
        else:
            result += "<div class='tooltip'>" + str(j) + "<span class='tooltiptext'>" 
            for p in playernames:
                if str(p) != "None":
                    result += str(p) + "<br>"
            result += "</span></div></td>"
            result += "<td>" + arenas[index]  + "<td></td> "

    result += "</tr>"
result+= "</table><br><a href = 'https://stats.nba.com/scores/03/11/2020'><img src='http://loodibee.com/wp-content/uploads/nba-logo-transparent.png' alt='NBA logo' height='150'></a>"
result+= "<p style = 'text-align:center; font-size:12px'>Project 3bet, Case Western Reserve Univeristy 2020 Senior Project <br> David Greenberg, Brian Pang, Lucas Invernizzi, Kevin Szmyd, David Kerrigan</p></body></html>"


def index(request):
    return HttpResponse(result)
