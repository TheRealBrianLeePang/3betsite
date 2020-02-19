import urllib.request
from datetime import date

def addZero(num):
    if len(str(num)) == 1:
        return '0'+str(num)
    else:
        return str(num)

print('Beginning file download with urllib2...')


today = date.today()
year = str(today.year)
month = addZero(today.month)
day = addZero(today.day)



url = 'http://data.nba.net/10s/prod/v1/'+year+month+day+'/scoreboard.json'
print(url)
urllib.request.urlretrieve(url, 'test.json')