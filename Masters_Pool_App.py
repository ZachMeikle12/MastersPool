import streamlit as st
import requests
from bs4 import BeautifulSoup

def scorecheck(s):
    try:
        s = s.replace('−', '-').replace('+', '')
        return int(s)
    except:
        return None

url = 'https://www.espn.com/golf/leaderboard/_/tournament/401529524'  
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0)',
    'Accept-Language': 'en-US,en;q=0.9'
}
resp = requests.get(url, headers=headers)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, 'html.parser')

# Extract leaderboard table
table = soup.find('table')
rows = []
if table:
    for tr in table.find_all('tr')[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all('td')]
        if cells:
            rows.append(cells)

# Define your groups (example players, adjust as needed)
groups = {
    'Zach': ['Scottie Scheffler', 'Shane Lowry', 'Tommy Fleetwood', 'Joaquín Niemann', 'Tyrell Hatton', 'Jon Rahm', 'Russell Henley', 'Cameron Young', 'Xander Schauffele', 'Viktor Hovland'],
    'Chris': ['Rory McIlroy', 'Padraig Harrington', 'Justin Thomas', 'Justin Rose', 'Sepp Straka', 'Scottie Scheffler', 'Jon Rahm', 'Matt Fitzpatrick', 'Chris Gotterup', 'Adam Scott'],
    'Bob': ['Rory McIlroy', 'Bryson Dechambeau', 'Shane Lowry', 'Justin Rose', 'Viktor Hovland', 'Scottie Scheffler', 'Jon Rahm', 'Tommy Fleetwood', 'Ludvig Åberg', 'Robert McIntyre'],
    'Bob2': ['Mackenzie Hughes', 'Collin Morikawa', 'Matt Fitzpatrick', 'Brooks Koepka', 'Rory McIlroy', 'Rickie Fowler', 'Scottie Scheffler', 'J.J. Spaun', 'Tony Finau', 'Tom Kim'],
    'Michael' : ['Rory McIlroy', 'Tom McKibbin', 'Shane Lowry', 'Justin Rose', 'Viktor Hovland', 'Scottie Scheffler', 'Jon Rahm', 'Tommy Fleetwood', 'Jordan Spieth', 'Tyrell Hatton'],
   
}

# Determine worst live round score (excluding cuts/E)
worstscore = 0
for row in rows:
    if len(row) > 5:
        r = scorecheck(row[5])
        if row[4] not in ['E', 'CUT'] and r is not None:
            worstscore = max(worstscore, r)

# Build group leaderboard
leaderboard = []
for name, players in groups.items():
    total = 0
    for row in rows:
        if len(row) > 4 and row[3] in players:
            scr = row[4]
            val = scorecheck(scr)
            if scr == 'CUT':
                r1 = scorecheck(row[7]) if len(row) > 7 else None
                r2 = scorecheck(row[8]) if len(row) > 8 else None
                if r1 is not None and r2 is not None:
                    ps = r1 + r2 - 144
                    total += ps + worstscore
            elif val is not None:
                total += val
    leaderboard.append((name, total))

# Display sorted leaderboard
leaderboard.sort(key=lambda x: x[1])
st.title("🏌️‍♂️ Open Championship Pool Leaderboard")
for i, (name, tot) in enumerate(leaderboard, 1):
    st.write(f"#{i} • {name}: **{tot:+}**")

# Detailed player scores
st.header("Group Player Breakdown")
for name, players in groups.items():
    st.subheader(name)
    total = 0
    for p in players:
        for row in rows:
            if len(row) > 6 and row[3] == p:
                scr, thru = row[4], row[6]
                val = scorecheck(scr)
                if scr == 'E':
                    st.write(f"{p}: E (Even) — thru {thru}")
                elif scr == 'CUT':
                    r1 = scorecheck(row[7]) if len(row) > 7 else None
                    r2 = scorecheck(row[8]) if len(row) > 8 else None
                    if r1 is not None and r2 is not None:
                        ps = r1 + r2 - 144
                        player_worse = ps + worstscore
                        total += player_worse
                        st.write(f"{p}: CUT (+{ps}) + worstscore ({worstscore}) = {player_worse}")
                    else:
                        st.write(f"{p}: CUT — score unavailable")
                elif val is not None:
                    total += val
                    st.write(f"{p}: {val:+} thru {thru}")
    st.write(f"**{name} Total: {total:+}**\n")
