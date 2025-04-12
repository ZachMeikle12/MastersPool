import streamlit as st
import requests
from bs4 import BeautifulSoup

def safe_parse_score(s):
    try:
        s = s.replace('−', '-').replace('+', '')  
        return int(s)
    except:
        return None

url = 'https://www.espn.com/golf/leaderboard/_/tournament/401529410'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}
response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table')
rows = []
if table:
    headers = [th.text for th in table.find_all('th')]
    for tr in table.find_all('tr')[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all('td')]
        if cells:
            rows.append(cells)

Zach_Players = ['Joaquín Niemann', 'Scottie Scheffler', 'Rory McIlroy', 'Xander Schauffele', 'Collin Morikawa', 'Jon Rahm', 'Patrick Cantlay', 'Min Woo Lee', 'Sepp Straka', 'Corey Conners']
Chris_Players = ['Jordan Spieth', 'Scottie Scheffler', 'Rory McIlroy', 'Hideki Matsuyama', 'Justin Thomas', 'Jon Rahm', 'Phil Mickelson', 'Robert MacIntyre', 'Dustin Johnson', 'Corey Conners']
Bob_Players = ['Scottie Scheffler', 'Will Zalatoris', 'Corey Conners', 'Collin Morikawa', 'Ludvig Åberg', 'Robert MacIntyre', 'Jon Rahm', 'Tony Finau', 'Rory McIlroy', 'Tom Hoge']
Matthew_Players = ['Bryson DeChambeau','Tony Finau','Tom Kim', 'Scottie Scheffler', 'Jordan Spieth', 'Justin Thomas', 'Keegan Bradley', 'Collin Morikawa', 'Xander Schauffele', 'Rory McIlroy']
Michael_Players = ['Rory McIlroy', 'Scottie Scheffler', 'Xander Schauffele', 'Bryson DeChambeau', 'Brooks Koepka', 'Shane Lowry', 'Tommy Fleetwood', 'Collin Morikawa', 'Jordan Spieth', 'Justin Thomas']
groups = [('Zach', Zach_Players), ('Chris', Chris_Players), ('Bob', Bob_Players), ('Matthew', Matthew_Players), ('Michael', Michael_Players)]

worstscore = 0
for row in rows:
    if len(row) > 5:
        r1 = safe_parse_score(row[5])
        if row[4] not in ['E', 'CUT'] and r1 is not None:
            worstscore = max(worstscore, r1)

leaderboard = []
for group in groups:
    name = group[0]
    players = group[1]
    totalscore = 0
    for row in rows:
        if len(row) > 4 and row[3] in players:
            score_str = row[4]
            score_val = safe_parse_score(score_str)

            if score_str == 'CUT':
                r1 = safe_parse_score(row[7]) if len(row) > 7 else None
                r2 = safe_parse_score(row[8]) if len(row) > 8 else None
                if r1 is not None and r2 is not None:
                    playerscore = r1 + r2 - 144
                    totalscore += playerscore + worstscore
            elif score_val is not None:
                totalscore += score_val
    leaderboard.append([name, players, totalscore])


scaled_leaderboard = sorted(leaderboard, key=lambda x: x[2])

leaderboard_print = ''
for i in range(len(scaled_leaderboard)):
    leaderboard_print += f"#{i+1}: {scaled_leaderboard[i][0]} with a score of: {scaled_leaderboard[i][2]}  \n"

st.title('Pool Leaderboard:')
st.write(leaderboard_print)

worstscore = 0
for row in rows:
    if len(row) > 5:
        r1 = safe_parse_score(row[5])
        if row[4] not in ['E', 'CUT'] and r1 is not None:
            worstscore = max(worstscore, r1)

for group in scaled_leaderboard:
    name = group[0]
    players = group[1]
    output = f"{name}'s Individual Scores:  \n"
    totalscore = 0
    for row in rows:
        if len(row) > 6 and row[3] in players:
            player = row[3]
            score_str = row[4]
            thru = row[6] if len(row) > 6 else ''
            score_val = safe_parse_score(score_str)

            if score_str == 'E':
                output += f"{player}: Even thru {thru}  \n"
            elif score_str == 'CUT':
                r1 = safe_parse_score(row[7]) if len(row) > 7 else None
                r2 = safe_parse_score(row[8]) if len(row) > 8 else None
                if r1 is not None and r2 is not None:
                    playerscore = r1 + r2 - 144
                    player_worse = playerscore + worstscore
                    output += f"{player}: CUT (+{playerscore}) + worst score ({worstscore}) = {player_worse}  \n"
                    totalscore += player_worse
                else:
                    output += f"{player}: CUT (score unavailable)  \n"
            elif score_val is not None:
                output += f"{player}: {score_val} thru {thru}  \n"
                totalscore += score_val

    output += f"Total Score = {totalscore}  \n  \n"
    st.write(output)
