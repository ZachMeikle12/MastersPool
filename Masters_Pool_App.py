import streamlit as st
import requests
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="The Masters Fantasy Pool",
    page_icon="🌿",
    layout="wide",
)

# ─────────────────────────────────────────────
#  MASTERS-THEMED CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Cormorant+Garamond:wght@300;400;600&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap');

:root {
    --green-deep:  #1a3a2a;
    --green-mid:   #2d5a3d;
    --green-light: #4a7c59;
    --gold:        #c9a84c;
    --gold-light:  #e8c97a;
    --cream:       #f5f0e8;
    --white:       #fdfbf7;
    --charcoal:    #1c1c1c;
    --red-cut:     #8b2020;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--green-deep) !important;
    color: var(--cream) !important;
    font-family: 'EB Garamond', Georgia, serif !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2318 0%, #1a3a2a 100%) !important;
    border-right: 2px solid var(--gold) !important;
}

/* HEADER */
.masters-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    background: linear-gradient(180deg, #0f2318 0%, var(--green-deep) 100%);
    border-bottom: 3px solid var(--gold);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.masters-header::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(201,168,76,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.masters-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 900;
    color: var(--gold);
    letter-spacing: 0.04em;
    text-shadow: 0 2px 20px rgba(201,168,76,0.4);
    margin: 0;
    line-height: 1.1;
}
.masters-subtitle {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.1rem;
    color: var(--gold-light);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 0.4rem;
    opacity: 0.85;
}
.masters-year {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 0.95rem;
    color: rgba(201,168,76,0.6);
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}
.azalea-row {
    text-align: center;
    font-size: 1.5rem;
    letter-spacing: 0.4em;
    color: rgba(201,168,76,0.35);
    margin: 0.5rem 0;
    user-select: none;
}

/* SECTION DIVIDERS */
.section-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0 1.2rem;
}
.section-divider::before,
.section-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.section-label {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.3rem;
    color: var(--gold);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: nowrap;
}

/* LEADERBOARD CARDS */
.lb-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
    gap: 1rem;
    margin-bottom: 2.5rem;
}
.lb-card {
    background: linear-gradient(145deg, #243d2e 0%, #1a3028 100%);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 4px;
    padding: 1.2rem 1rem;
    text-align: center;
    position: relative;
    transition: transform 0.2s, border-color 0.2s;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.lb-card:hover { transform: translateY(-3px); border-color: var(--gold); }
.lb-card.first-place {
    background: linear-gradient(145deg, #2e4a1e 0%, #1e3818 100%);
    border: 2px solid var(--gold);
    box-shadow: 0 4px 25px rgba(201,168,76,0.25);
}
.lb-rank { font-family: 'Playfair Display', serif; font-size: 0.8rem; color: rgba(201,168,76,0.6); letter-spacing: 0.2em; text-transform: uppercase; }
.lb-rank-num { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: var(--gold); line-height: 1; }
.lb-rank-num.first { color: var(--gold-light); text-shadow: 0 0 15px rgba(201,168,76,0.5); }
.lb-name { font-family: 'Cormorant Garamond', serif; font-size: 1.25rem; font-weight: 600; color: var(--cream); margin: 0.3rem 0; letter-spacing: 0.05em; }
.lb-score { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 700; }
.lb-score.under { color: #6dbf8a; }
.lb-score.over  { color: #e07070; }
.lb-score.even  { color: var(--cream); }

.jacket-ribbon { position: absolute; top: 0; right: 0; width: 0; height: 0; border-style: solid; border-width: 0 42px 42px 0; border-color: transparent var(--gold) transparent transparent; }
.jacket-ribbon span { position: absolute; top: 5px; right: -38px; font-size: 0.65rem; color: var(--green-deep); font-weight: 700; letter-spacing: 0.05em; transform: rotate(45deg); pointer-events: none; }

/* PLAYER BREAKDOWN */
.breakdown-section {
    background: linear-gradient(145deg, #1e3528 0%, #182c20 100%);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.25);
}
.breakdown-title { font-family: 'Playfair Display', serif; font-size: 1.35rem; color: var(--gold); margin-bottom: 0.8rem; border-bottom: 1px solid rgba(201,168,76,0.25); padding-bottom: 0.5rem; letter-spacing: 0.06em; }
.player-row { display: flex; justify-content: space-between; align-items: center; padding: 0.35rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-family: 'EB Garamond', Georgia, serif; font-size: 1.05rem; }
.player-row:last-of-type { border-bottom: none; }
.player-name { color: var(--cream); }
.player-score.under { color: #6dbf8a; font-weight: 600; }
.player-score.over  { color: #e07070; font-weight: 600; }
.player-score.cut   { color: #c07070; font-style: italic; }
.player-score.even  { color: var(--cream); }
.breakdown-total { font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; font-weight: 600; color: var(--gold-light); margin-top: 0.7rem; text-align: right; letter-spacing: 0.05em; }

/* INFO BOX */
.info-box {
    background: rgba(201,168,76,0.08);
    border-left: 3px solid var(--gold);
    padding: 0.7rem 1rem;
    border-radius: 2px;
    font-family: 'EB Garamond', Georgia, serif;
    font-size: 0.95rem;
    color: rgba(245,240,232,0.75);
    margin-bottom: 1.5rem;
}

/* STREAMLIT OVERRIDES */
h1,h2,h3,h4,h5,h6 { color: var(--gold) !important; }
.stMarkdown p { color: var(--cream) !important; font-family: 'EB Garamond', Georgia, serif !important; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ✏️  EDIT YOUR POOL PARTICIPANTS HERE
#  Each person gets 10 player names.
#  Names must match ESPN leaderboard spelling.
# ─────────────────────────────────────────────
groups = {
    "Zach": [
        "Scottie Scheffler",
        "Rory McIlroy",
        "Jon Rahm",
        "Xander Schauffele",
        "Bryson Dechambeau",
        "Ludvig Åberg",
        "Tommy Fleetwood",
        "Akshay Bhatia",
        "Cameron Young",
        "Jordan Spieth",
    ],
    "Chris": [
        "Scottie Scheffler",
        "Rory McIlroy",
        "Bryson DeChambeau",
        "Xander Schauffele",
        "Nicolai Højgaard",
        "Hideki Matsuyama",
        "Matt Fitzpatrick",
        "Hideki Matsuyama",
        "Patrick Reed",
        "Ludvig Åberg",
    ],
    "Bob": [
        "Corey Conners",
        "Rory McIlroy",
        "Jon Rahm",
        "Collin Morikawa",
        "Tommy Fleetwood",
        "Jordan Spieth",
        "Ludvig Åberg",
        "Chris Gotterup",
        "Bryson DeChambeau",
        "Justin Rose",
    ],
    "Matthew": [
        "Scottie Scheffler",
        "Rory McIlroy",
        "Jon Rahm",
        "Tommy Fleetwood",
        "Matt Fitzpatrick",
        "Ludvig Åberg",
        "Cameron Young",
        "Justin Rose",
        "Xander Schauffele",
        "Bryson Dechambeau",
    ],
    "Michael": [
        "Scottie Scheffler",
        "Rory McIlroy",
        "Bryson Dechambeau",
        "Tommy Fleetwood",
        "Hideki Matsuyama",
        "Jon Rahm",
        "Sepp Straka",
        "Akshay Bhatia",
        "Shane Lowry",
        "Ludvig Åberg",
    ],
    "Rives": [
        "Scottie Scheffler",
        "Rory McIlroy",
        "Bryson Dechambeau",
        "Cameron Young",
        "Tommy Fleetwood",
        "Chris Gotterup",
        "Jon Rahm",
        "Justin Rose",
        "Hideki Matsuyama",
        "Ludvig Åberg",
    ],
    "Sawyer": [
        "Scottie Scheffler",
        "Rory McIlroy",
        "Bryson Dechambeau",
        "Jon Rahm",
        "Xander Schauffele",
        "Ludvig Åberg",
        "Tommy Fleetwood",
        "Min Woo Lee",
        "Hideki Matsuyama",
        "Justin Rose",
    ],
}

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def scorecheck(s):
    try:
        s = s.strip().replace('−', '-').replace('–', '-').replace('+', '')
        if s in ('E', 'Even', ''):
            return 0
        return int(s)
    except Exception:
        return None

def fmt_score(val):
    if val is None:
        return "–", "even"
    if val == 0:
        return "E", "even"
    if val > 0:
        return f"+{val}", "over"
    return str(val), "under"

# ─────────────────────────────────────────────
#  FETCH ESPN LEADERBOARD
#  Update the tournament ID below each year!
#  Find it in the ESPN leaderboard URL.
# ─────────────────────────────────────────────
@st.cache_data(ttl=120, show_spinner=False)
def fetch_leaderboard():
    url = "https://www.espn.com/golf/leaderboard/_/tournamentId/401811998"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0)",
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")
    rows = []
    if table:
        for tr in table.find_all("tr")[1:]:
            cells = [td.get_text(strip=True) for td in tr.find_all("td")]
            if cells:
                rows.append(cells)
    return rows

# ─────────────────────────────────────────────
#  COMPUTE POOL SCORES
# ─────────────────────────────────────────────
def compute(rows):
    # Worst single-round score among active players (used for missed-cut penalty)
    worst = 0
    for row in rows:
        if len(row) > 5:
            r = scorecheck(row[5])
            if row[4] not in ["E", "CUT"] and r is not None:
                worst = max(worst, r)

    results = {}
    for owner, players in groups.items():
        player_details = []
        total = 0
        for player in players:
            found = False
            for row in rows:
                if len(row) > 6 and row[3].strip() == player:
                    found = True
                    scr  = row[4].strip()
                    thru = row[6].strip() if len(row) > 6 else "–"
                    val  = scorecheck(scr)

                    if scr == "CUT":
                        r1 = scorecheck(row[7]) if len(row) > 7 else None
                        r2 = scorecheck(row[8]) if len(row) > 8 else None
                        if r1 is not None and r2 is not None:
                            ps = r1 + r2 - 144
                            combined = ps + worst
                            total += combined
                            ws_str = f"+{worst}" if worst >= 0 else str(worst)
                            ps_str = f"+{ps}" if ps >= 0 else str(ps)
                            player_details.append({
                                "name": player,
                                "display": f"CUT ({ps_str}) + worst ({ws_str}) = {combined:+}",
                                "kind": "cut",
                                "value": combined,
                            })
                        else:
                            player_details.append({
                                "name": player,
                                "display": "CUT — score unavailable",
                                "kind": "cut",
                                "value": None,
                            })
                    elif val == 0:
                        player_details.append({
                            "name": player,
                            "display": f"E  —  thru {thru}",
                            "kind": "even",
                            "value": 0,
                        })
                    elif val is not None:
                        total += val
                        s, cls = fmt_score(val)
                        player_details.append({
                            "name": player,
                            "display": f"{s}  —  thru {thru}",
                            "kind": cls,
                            "value": val,
                        })
                    break

            if not found:
                player_details.append({
                    "name": player,
                    "display": "Not yet started",
                    "kind": "even",
                    "value": 0,
                })

        results[owner] = {"players": player_details, "total": total}

    return results, worst

# ─────────────────────────────────────────────
#  RENDER HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="masters-header">
    <div class="azalea-row">✦ ✦ ✦</div>
    <p class="masters-year">Augusta National · 2025</p>
    <h1 class="masters-title">The Masters</h1>
    <p class="masters-subtitle">Fantasy Pool Leaderboard</p>
    <div class="azalea-row">✦ ✦ ✦</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
with st.spinner("Fetching live scores from Augusta..."):
    try:
        raw_rows = fetch_leaderboard()
        data, worst_score = compute(raw_rows)
        load_ok = True
    except Exception as e:
        load_ok = False
        err_msg = str(e)

if not load_ok:
    st.error(f"⛳ Could not fetch leaderboard data: {err_msg}")
    st.stop()

# ─────────────────────────────────────────────
#  STANDINGS OVERVIEW
# ─────────────────────────────────────────────
sorted_entries = sorted(data.items(), key=lambda x: x[1]["total"])

st.markdown('<div class="section-divider"><span class="section-label">🏆 Standings</span></div>', unsafe_allow_html=True)

ordinals = {1: "st", 2: "nd", 3: "rd"}
cards_html = '<div class="lb-grid">'
for rank, (owner, info) in enumerate(sorted_entries, 1):
    tot = info["total"]
    s, cls = fmt_score(tot)
    is_first = "first-place" if rank == 1 else ""
    num_cls  = "first" if rank == 1 else ""
    ribbon   = '<div class="jacket-ribbon"><span>🏅</span></div>' if rank == 1 else ""
    suf = ordinals.get(rank, "th")
    cards_html += f"""
    <div class="lb-card {is_first}">
        {ribbon}
        <div class="lb-rank"><span class="lb-rank-num {num_cls}">{rank}</span><sup>{suf}</sup></div>
        <div class="lb-name">{owner}</div>
        <div class="lb-score {cls}">{s}</div>
    </div>"""
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INFO BOX
# ─────────────────────────────────────────────
ws_disp = f"+{worst_score}" if worst_score >= 0 else str(worst_score)
st.markdown(f"""
<div class="info-box">
    ⛳ <strong>Scoring:</strong> Pool score = sum of each player's score to par.
    Players who miss the cut: their cut score + the field's worst round ({ws_disp}) is applied.
    Scores refresh every 2 minutes.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PLAYER BREAKDOWNS (2-column layout)
# ─────────────────────────────────────────────
st.markdown('<div class="section-divider"><span class="section-label">🌿 Player Breakdown</span></div>', unsafe_allow_html=True)

cols = st.columns(2)
for i, (owner, info) in enumerate(sorted_entries):
    col = cols[i % 2]
    with col:
        rows_html = ""
        for p in info["players"]:
            rows_html += f"""
            <div class="player-row">
                <span class="player-name">{p['name']}</span>
                <span class="player-score {p['kind']}">{p['display']}</span>
            </div>"""
        tot = info["total"]
        ts, _ = fmt_score(tot)
        rank_label = next(r + 1 for r, (o, _) in enumerate(sorted_entries) if o == owner)
        st.markdown(f"""
        <div class="breakdown-section">
            <div class="breakdown-title">#{rank_label} &nbsp;·&nbsp; {owner}</div>
            {rows_html}
            <div class="breakdown-total">Pool Total: {ts}</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;opacity:0.4;font-family:'Cormorant Garamond',serif;
letter-spacing:0.15em;font-size:0.85rem;text-transform:uppercase;color:#c9a84c;">
    A tradition unlike any other &nbsp;·&nbsp; Data via ESPN
</div>
""", unsafe_allow_html=True)
