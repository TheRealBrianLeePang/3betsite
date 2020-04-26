import json
import urllib.request

teamIds = {}

url = 'http://data.nba.net/10s//prod/'+str(2019)+'/teams_config.json'
urllib.request.urlretrieve(url, 'teamconfig.json')

with open('teamconfig.json') as json_file:
    data = json.load(json_file)
    for i in data['teams']['config']:
        if 'ttsName' in i:
            teamIds[i['teamId']] = i['ttsName']

with open('teamDictionary.json', 'w') as file:
    file.write(json.dumps(teamIds))