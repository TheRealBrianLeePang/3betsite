from urllib import request

days = [31,30,31,31,29,31]
months = ['10','11','12','01','02','03']
year = [2019,2019,2019,2020,2020,2020]

def addZero(num):
    if len(str(num)) == 1:
        return '0'+str(num)
    else:
        return str(num)

for i in range(len(months)):
    for j in range(1,days[i]+1):
        string = str(year[i])+months[i]+addZero(j)
        url = 'http://data.nba.net/10s/prod/v1/'+string+'/scoreboard.json'
        print(url)
        request.urlretrieve(url, 'C:\\Users\\david\\Documents\\case\\graduating\\395\\3betsite\\mysite\data\\'+string+'.json')
    
