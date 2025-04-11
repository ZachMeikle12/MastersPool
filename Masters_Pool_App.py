import streamlit as st
import requests
from bs4 import BeautifulSoup

url = 'https://www.espn.com/golf/leaderboard/_/tournament/401529410' 

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table')
if table:
    headers = [th.text for th in table.find_all('th')]
    rows = []
    for tr in table.find_all('tr')[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all('td')]
        if cells:
            rows.append(cells)
# Scores
Zach_Players = ['Joaquín Niemann', 'Scottie Scheffler', 'Rory McIlroy', 'Xander Schauffele', 'Collin Morikawa', 'Jon Rahm', 'Patrick Cantlay', 'Min Woo Lee', 'Sepp Straka', 'Corey Conners']
Chris_Players = ['Jordan Spieth', 'Scottie Scheffler', 'Rory McIlroy', 'Hideki Matsuyama', 'Justin Thomas', 'Jon Rahm', 'Phil Mickelson', 'Robert MacIntyre', 'Dustin Johnson', 'Corey Conners']
Bob_Players = ['Scottie Scheffler', 'Will Zalatoris', 'Corey Conners', 'Collin Morikawa', 'Ludvig Åberg', 'Robert MacIntyre', 'Jon Rahm', 'Tony Finau', 'Rory McIlroy', 'Tom Hoge']
Matthew_Players = ['Bryson DeChambeau','Tony Finau','Tom Kim', 'Scottie Scheffler', 'Jordan Spieth', 'Justin Thomas', 'Keegan Bradley', 'Collin Morikawa', 'Xander Schauffele', 'Rory McIlroy']
Michael_Players = ['Rory McIlroy', 'Scottie Scheffler', 'Xander Schauffele', 'Bryson DeChambeau', 'Brooks Koepka', 'Shane Lowry', 'Tommy Fleetwood', 'Collin Morikawa', 'Jordan Spieth', 'Justin Thomas']
groups = [('Zach',Zach_Players), ('Chris',Chris_Players), ('Bob', Bob_Players), ('Matthew', Matthew_Players), ('Michael', Michael_Players)]
leaderboard = []

for group in groups:
    score = group[0] + "'s Total Score:  \n"
    totalscore = 0
    for row in rows:
        if len(row) > 2 and row[3] in group[1] and row[4] != 'E':
            totalscore += int(row[4])
    leaderboard.append([group[0], totalscore])     
    
scaled_leaderboard =[]
for x in range (-30, 50):
    for leader in leaderboard:
        if leader[1] == x:
            scaled_leaderboard.append(leader)

leaderboard_print = ''
for i in (1,2,3,4,5):
    index = i-1
    leaderboard_print += ('#' + str(i) + ': ' + scaled_leaderboard[index][0] + ' with a score of: ' + str(scaled_leaderboard[index][1]) + '  \n')

st.title('Pool Leaderboard:')
st.write(leaderboard_print)

for group in groups:
    score = group[0] + "'s Total Score:  \n"
    totalscore = 0
    for row in rows:
        if len(row) > 2 and row[3] in group[1]:
            if row[4] == 'E':
                score += str(row[3] + ': Even' + '  \n')
            else:
                totalscore += int(row[4])
                score += str(row[3] + ' : ' + row[4] +'  \n')
    score += 'Total Score = ' + str(totalscore) + '  \n  \n  \n'   
    leaderboard.append([group[0], totalscore])     
    st.write (score)
