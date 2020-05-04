from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
from datetime import date, timedelta, datetime
import json
from copy import copy, deepcopy
import os.path
from os import path
import ast
from django.template import Context, RequestContext
from django.shortcuts import render, get_object_or_404

def getContentForDate(param):
    today = param
    def addZero(num):
        if len(str(num)) == 1:
            return '0'+str(num)
        else:
            return str(num)

    year = str(today.year)
    day = addZero(today.day)
    month = addZero(today.month)
    scheduleYear = ''
    games = []
    arenas = []
    scores = []


    url = 'http://data.nba.net/10s/prod/v1/'+year+month+day+'/scoreboard.json'
    print(url)
    #urllib.request.urlretrieve(url, 'scoreboard.json')
    url = 'http://data.nba.net/10s/prod/v1/today.json'
    #urllib.request.urlretrieve(url, 'frontpage.json')

    with open('data/'+year+month+day+'.json') as json_file:
        data = json.load(json_file)
        for p in data['games']:
            games.append([p['vTeam']['teamId'],p['hTeam']['teamId']])
            arenas.append(p['arena']['name']+ ", " + p['arena']['city'])
            score1 = int(p['vTeam']['score'])
            score2 = int(p['hTeam']['score'])
            if score1 > score2:
                scores.append(p['vTeam']['teamId']+"-"+str(score1-score2))
            else:
                scores.append(p['hTeam']['teamId']+"-"+str(score2-score1))

    with open('frontpage.json') as json_file:
        data = json.load(json_file)
        scheduleYear = data['seasonScheduleYear']
    url = 'http://data.nba.net/10s//prod/'+str(scheduleYear)+'/teams_config.json'
    #urllib.request.urlretrieve(url, 'teamconfig.json')

    with open('polls/teamDictionary.json') as json_file:
        teamDict = json.load(json_file)

    teamNames = deepcopy(games)
    for index,i in enumerate(games):
        for jindex,j in enumerate(i):
            name = teamDict[j]
            teamNames[index][jindex] = name
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
            urllib.request.urlretrieve(url, 'data/'+teamId+'.json')
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
    result += "<style>"
    result += "img{display: block; margin-left: auto; margin-right: auto;}"
    result += ".tooltip {position: relative; display: inline-block; border-bottom: 1px dotted black;}"
    result += ".tooltip .tooltiptext {visibility: hidden; width: 200px; background-color: black; color: white; text-align: center; border-radius: 6px; padding: 5px 0; top: 100%; left: 50%; margin-left: -100px; position: absolute; z-index: 1;}"
    result += ".tooltip:hover .tooltiptext {visibility: visible;}"
    result += ".center {margin: 0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);}"
    result += "body{color: white; font-weight: bold; background-image: url('https://cdn.nba.net/assets/video/logos/nba-placeholder.jpg'); background-attachment: fixed; background-position: center; background-repeat: no-repeat; background-size: cover;}"
    result += "table{white-space: nowrap;}</style>"
    result += "</head><div class='center'><body><h1 align='center'>NBA Games Happening on " + month + "/" + day + "/" + year + ":</h1>"
    result += "<h3 style = 'text-align:center'><i>(If COVID-19 didn't exist!)</i></h3>"
    
    result+='''
        <form action="/polls/callback">
            <label for="date">Select Game Day:</label>
            <input type="date" id="date" name="date" value = "2019-10-22">
            <input type="submit">
        </form>
        <style>
        form {
            text-align: center;
        }
        input[type="date"], textarea {
            background-color : #d1d1d1;
            color : black; 
        }
        input[type="submit"], textarea {
            background-color : #d1d1d1; 
            color : black;
        }
        </style>
        '''

    result += "<br><table align='center' class='pure-table pure-table-bordered'><thead><tr><th>Away Team</th><th>Home Team</th><th>Location</th><th>Winner/Spread</th></thead>"

    with open('polls/playerDictionary.json') as json_file:
        playerDict = json.load(json_file)

    for index,i in enumerate(teamNames):
        result += "<tr>"
        for jindex,j in enumerate(i):
            
            playernames = playerDict[games[index][jindex]]
            playernames = playernames.split(",")
            
            result += "<td>"
            
            if jindex % 2 == 0:
                result += "<div class='tooltip'>" + str(j) + "<span class='tooltiptext'>" 
                for p in playernames[:-1]:
                    result += str(p) + "<br>"
                result += playernames[-1] + "</span></div></td>"
            else:
                result += "<div class='tooltip'>" + str(j) + "<span class='tooltiptext'>" 
                for p in playernames[:-1]:
                    result += str(p) + "<br>"
                result += playernames[-1] + "</span></div></td>"
                winningTeam = scores[index][:scores[index].index("-")]
                spread = scores[index][scores[index].index("-"):]
                result += "<td>" + arenas[index]  + "<td>"+teamDict[winningTeam]+" "+spread+"</td> "

        result += "</tr>"
    result+= "</table><br><a href = 'https://stats.nba.com/scores/03/11/2020'><img src='http://loodibee.com/wp-content/uploads/nba-logo-transparent.png' alt='NBA logo' height='150'></a>"
    result+= "<p style = 'text-align:center; font-size:12px'>Project 3bet, Case Western Reserve Univeristy 2020 Senior Project <br> David Greenberg, Brian Pang, Lucas Invernizzi, Kevin Szmyd, David Kerrigan</p></body></html>"
    return result

def getDateError():
    result = ""
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
    result += "body{color: white; font-weight: bold; background-image: url('https://cdn.nba.net/assets/video/logos/nba-placeholder.jpg'); background-attachment: fixed; background-position: center; background-repeat: no-repeat; background-size: cover;}</style>"
    result += "</head><div class='center'>"
    result += "<img src='https://www.nydailynews.com/resizer/DKedK97eZSd4d2WbitR8EHY31ig=/800x449/top/arc-anglerfish-arc2-prod-tronc.s3.amazonaws.com/public/6QUWZT3XHKLK3HJZADSBFWQQPE.gif' alt='DENIED!'>"
    result += "<h1 align='center'>DENIED!</h1><h2 align='center'>The date selected is not in the 3Bet Project Model. <br> Please enter another date:</h2>"
    result+='''
        <form action="/polls/callback">
            <label for="date">Select Game Day:</label>
            <input type="date" id="date" name="date" value = "2019-10-22" min="2019-10-22" max="2020-03-11">
            <input type="submit">
        </form>
        <style>
        form {
            text-align: center;
        }
        input[type="date"], textarea {
            background-color : #d1d1d1;
            color : black; 
        }
        input[type="submit"], textarea {
            background-color : #d1d1d1; 
            color : black;
        }
        </style>
        '''
    return result

def callback(request):
    today = datetime.strptime(request.GET.get('date'),"%Y-%m-%d")
    start = datetime.strptime("01-10-2019", "%d-%m-%Y")
    end = datetime.strptime("31-03-2020", "%d-%m-%Y")
    if today > start and today < end:
        result=getContentForDate(today)
        return HttpResponse(result)
    else:
        result = getDateError()
        return HttpResponse(result)


def index(request):
    today = date.today() - timedelta(days=90)
    result = getContentForDate(today)
    return HttpResponse(result)
