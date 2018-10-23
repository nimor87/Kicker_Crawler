import requests
from bs4 import BeautifulSoup

base_url = 'http://www.kicker.de'
clubs_url = base_url + '/news/fussball/bundesliga/vereine/1-bundesliga/2018-19/vereine-liste.html'

html = requests.get(clubs_url).content
soup = BeautifulSoup(html, 'html.parser')

# get table with all clubs
table = soup.find_all('table', 'tStat')[0]
rows = table.find_all('tr', 'fest')

clubs = []

# row = club
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 0:
        club_name = cells[0].find('a', 'verinsLinkBild').get_text()
        club_squad_url = cells[2].find('a').get('href')
        clubs.append((club_name, club_squad_url))

bundesliga = dict()
club_id = 0

for name, url in clubs:
    club = dict()
    club_id += 1
    club['id'] = club_id
    club['name'] = name
    squad_url = base_url + url
    players = dict()
    soup = BeautifulSoup(requests.get(squad_url).content, 'html.parser')
    table = soup.find_all('table', 'tStat')[0]
    player_id = 0
    for link in table.find_all('a', 'link'):
        player_info = dict()
        player_id += 1
        player_url = base_url + link.get('href')
        player = BeautifulSoup(requests.get(player_url).content, 'html.parser')
        table = player.find_all('table', 'infoBox')[0]
        rows = table.find_all('tr')
        player_info['id'] = player_id
        player_info['first_name'] = rows[0].find_all('td')[1].get_text()
        player_info['last_name'] = rows[1].find_all('td')[1].get_text()
        player_info['position'] = rows[2].find_all('td')[1].get_text()
        player_info['number'] = rows[3].find_all('td')[1].get_text()
        player_info['birthday'] = rows[6].find_all('td')[1].get_text()
        player_info['height'] = rows[7].find_all('td')[1].get_text()
        player_info['weight'] = rows[8].find_all('td')[1].get_text()
        players[player_id] = player_info
    club['squad'] = squad
    bundesliga[club_id] = club



    
