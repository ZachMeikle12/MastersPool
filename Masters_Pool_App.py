import streamlit as st
import requests
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────
#  PAGE CONFIG
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Cormorant+Garamond:wght@300;400;600&family=EB+Garamond:wght@400;500&display=swap');

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

[data-testid="stVerticalBlock"] {
    gap: 0.6rem;
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
    margin: 2rem 0 1rem;
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
    font-size: 1.25rem;
    color: var(--gold);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: nowrap;
}

/* INFO BOX */
.info-box {
    background: rgba(201,168,76,0.08);
    border-left: 3px solid var(--gold);
    padding: 0.7rem 1rem;
    border-radius: 2px;
    font-family: 'EB Garamond', Georgia, serif;
    font-size: 0.98rem;
    color: rgba(245,240,232,0.82);
    margin-bottom: 1.2rem;
}

/* CARD SHELLS */
.card-shell {
    background: linear-gradient(145deg, #243d2e 0%, #1a3028 100%);
    border: 1px solid rgba(201,168,76,0.28);
    border-radius: 8px;
    padding: 0.1rem 0.1rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.25);
}

.first-shell {
    border: 2px solid var(--gold);
    box-shadow: 0 4px 24px rgba(201,168,76,0.18);
}

.breakdown-shell {
    background: linear-gradient(145deg, #1e3528 0%, #182c20 100%);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 8px;
    padding: 0.1rem 0.1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.22);
}

/* STREAMLIT OVERRIDES */
h1,h2,h3,h4,h5,h6 { color: var(--gold) !important; }
.stMarkdown p, .stMarkdown div {
    color: var(--cream);
    font-family: 'EB Garamond', Georgia, serif !important;
}
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

div[data-testid="stHorizontalBlock"] > div {
    padding-top: 0.1rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  POOL PARTICIPANTS
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
    if s is None:
        return None
    try:
        s = str(s).strip().replace("−", "-").replace("–", "-").replace("+", "")
        if s in ("E", "Even", ""):
            return 0
        if s.upper() in ("CUT", "--", "WD", "DQ"):
            return None
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

def normalize(name):
    if name is None:
        return ""
    replacements = {
        "å": "a", "Å": "a",
        "ö": "o", "Ö": "o",
        "é": "e", "É": "e",
        "ø": "o", "Ø": "o",
        "ü": "u", "Ü": "u",
        "á": "a", "Á": "a",
        "í": "i", "Í": "i",
        "ó": "o", "Ó": "o",
        "ú": "u", "Ú": "u",
        "ë": "e", "Ë": "e",
        "ï": "i", "Ï": "i",
        "ñ": "n", "Ñ": "n",
    }
    out = str(name).strip().lower()
    for old, new in replacements.items():
        out = out.replace(old, new)
    return " ".join(out.split())

def dedupe_keep_order(items):
    seen = set()
    out = []
    for item in items:
        key = normalize(item)
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out

def parse_score_token(tokens):
    for i, tok in enumerate(tokens):
        t = tok.strip()
        if t in {"E", "CUT", "--"} or t.startswith("+") or t.startswith("-"):
            return i, t
    return None, "--"

def format_position_labels(sorted_entries):
    """
    Returns a dict of owner -> rank label, e.g.
    T1, T1, 3, 4
    """
    labels = {}
    prev_score = None
    prev_rank = None

    for idx, (owner, info) in enumerate(sorted_entries, start=1):
        score = info["total"]

        if score == prev_score:
            labels[owner] = f"T{prev_rank}"
        else:
            # Look ahead to see if this score is tied
            count_same = sum(1 for _, inf in sorted_entries if inf["total"] == score)
            if count_same > 1:
                labels[owner] = f"T{idx}"
            else:
                labels[owner] = str(idx)

            prev_score = score
            prev_rank = idx

    return labels

def score_color(kind):
    if kind == "under":
        return "#6dbf8a"
    if kind == "over":
        return "#e07070"
    if kind == "cut":
        return "#c07070"
    return "#f5f0e8"

# ─────────────────────────────────────────────
#  FETCH ESPN LEADERBOARD
# ─────────────────────────────────────────────
@st.cache_data(ttl=120, show_spinner=False)
def fetch_leaderboard():
    url = "https://www.espn.com/golf/leaderboard?season=2025&tournamentId=401811941"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }

    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    rows = []
    seen = set()

    player_links = soup.find_all("a", href=True)

    for a in player_links:
        name = a.get_text(" ", strip=True)
        href = a.get("href", "")

        if not name or "/golf/player/_/id/" not in href:
            continue

        key = normalize(name)
        if key in seen:
            continue

        container = a
        for _ in range(8):
            container = container.parent
            if container is None:
                break
            block_text = container.get_text(" ", strip=True)
            if name in block_text and len(block_text.split()) >= 4:
                break

        if container is None:
            continue

        block_text = container.get_text(" ", strip=True)
        after = block_text.split(name, 1)[1].strip() if name in block_text else ""
        tokens = after.split()

        idx, score = parse_score_token(tokens)

        thru = "–"
        r1 = None
        r2 = None
        r3 = None
        r4 = None

        if idx is not None:
            if idx + 2 < len(tokens):
                thru = tokens[idx + 2]

            numeric_tokens = [t for t in tokens if t.isdigit()]

            if len(numeric_tokens) >= 4:
                r1, r2, r3, r4 = numeric_tokens[-4], numeric_tokens[-3], numeric_tokens[-2], numeric_tokens[-1]
            elif len(numeric_tokens) == 3:
                r1, r2, r3 = numeric_tokens[-3], numeric_tokens[-2], numeric_tokens[-1]
            elif len(numeric_tokens) == 2:
                r1, r2 = numeric_tokens[-2], numeric_tokens[-1]
            elif len(numeric_tokens) == 1:
                r1 = numeric_tokens[-1]

        rows.append({
            "name": name,
            "score": score,
            "thru": thru,
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "r4": r4,
        })
        seen.add(key)

    if not rows:
        raise ValueError("No leaderboard rows were parsed from the ESPN page.")

    return rows

# ─────────────────────────────────────────────
#  COMPUTE POOL SCORES
# ─────────────────────────────────────────────
def compute(rows):
    leaderboard_lookup = {}
    saturday_worst = 0
    sunday_worst = 0

    for row in rows:
        leaderboard_lookup[normalize(row["name"])] = row

        try:
            r3 = int(row["r3"]) if row.get("r3") not in (None, "") else None
        except Exception:
            r3 = None

        try:
            r4 = int(row["r4"]) if row.get("r4") not in (None, "") else None
        except Exception:
            r4 = None

        if r3 is not None:
            saturday_worst = max(saturday_worst, r3 - 72)

        if r4 is not None:
            sunday_worst = max(sunday_worst, r4 - 72)

    results = {}

    for owner, players in groups.items():
        unique_players = dedupe_keep_order(players)
        player_details = []
        total = 0

        for player in unique_players:
            row = leaderboard_lookup.get(normalize(player))

            if row is None:
                player_details.append({
                    "name": player,
                    "display": "Not found on leaderboard",
                    "kind": "even",
                    "value": 0,
                })
                continue

            scr = str(row.get("score", "")).strip()
            thru = row.get("thru", "–")
            val = scorecheck(scr)

            if scr.upper() == "CUT":
                r1_raw = row.get("r1")
                r2_raw = row.get("r2")

                try:
                    r1 = int(r1_raw) if r1_raw not in (None, "") else None
                    r2 = int(r2_raw) if r2_raw not in (None, "") else None
                except Exception:
                    r1, r2 = None, None

                if r1 is not None and r2 is not None:
                    cut_score = (r1 + r2) - 144
                    combined = cut_score + saturday_worst + sunday_worst
                    total += combined

                    cut_str = f"+{cut_score}" if cut_score > 0 else ("E" if cut_score == 0 else str(cut_score))
                    sat_str = f"+{saturday_worst}" if saturday_worst > 0 else ("E" if saturday_worst == 0 else str(saturday_worst))
                    sun_str = f"+{sunday_worst}" if sunday_worst > 0 else ("E" if sunday_worst == 0 else str(sunday_worst))

                    player_details.append({
                        "name": player,
                        "display": f"CUT ({cut_str}) + Sat ({sat_str}) + Sun ({sun_str}) = {combined:+}",
                        "kind": "cut",
                        "value": combined,
                    })
                else:
                    combined = saturday_worst + sunday_worst
                    total += combined

                    sat_str = f"+{saturday_worst}" if saturday_worst > 0 else ("E" if saturday_worst == 0 else str(saturday_worst))
                    sun_str = f"+{sunday_worst}" if sunday_worst > 0 else ("E" if sunday_worst == 0 else str(sunday_worst))

                    player_details.append({
                        "name": player,
                        "display": f"CUT — using Sat ({sat_str}) + Sun ({sun_str}) = {combined:+}",
                        "kind": "cut",
                        "value": combined,
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

            else:
                player_details.append({
                    "name": player,
                    "display": f"{scr}  —  thru {thru}",
                    "kind": "even",
                    "value": 0,
                })

        results[owner] = {
            "players": player_details,
            "total": total,
        }

    return results, saturday_worst, sunday_worst

# ─────────────────────────────────────────────
#  RENDER HELPERS
# ─────────────────────────────────────────────
def render_standings_card(rank_label, owner, total, is_first=False):
    score_text, kind = fmt_score(total)
    card_class = "card-shell first-shell" if is_first else "card-shell"

    with st.container(border=False):
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)

        top_left, top_mid, top_right = st.columns([1.2, 2.2, 0.8])

        with top_left:
            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-family:'Playfair Display',serif;
                    color:rgba(201,168,76,0.85);
                    padding-top:0.55rem;
                ">
                    <div style="font-size:1.5rem;font-weight:700;color:#c9a84c;line-height:1.05;">
                        {rank_label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with top_mid:
            st.markdown(
                f"""
                <div style="
                    font-family:'Cormorant Garamond',serif;
                    color:#f5f0e8;
                    font-size:1.45rem;
                    font-weight:600;
                    padding-top:0.65rem;
                ">
                    {owner}
                </div>
                """,
                unsafe_allow_html=True
            )

        with top_right:
            badge = "🏅" if is_first else ""
            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    padding-top:0.7rem;
                    padding-right:0.4rem;
                    font-size:1rem;
                ">
                    {badge}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-family:'Playfair Display',serif;
                font-size:1.8rem;
                font-weight:700;
                color:{score_color(kind)};
                padding:0.15rem 0 1rem 0;
            ">
                {score_text}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

def render_breakdown_card(rank_label, owner, info):
    total = info["total"]
    total_text, total_kind = fmt_score(total)

    with st.container(border=False):
        st.markdown('<div class="breakdown-shell">', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="
                font-family:'Playfair Display',serif;
                font-size:1.3rem;
                color:#c9a84c;
                letter-spacing:0.05em;
                border-bottom:1px solid rgba(201,168,76,0.22);
                padding:0.9rem 1rem 0.7rem 1rem;
                margin-bottom:0.1rem;
            ">
                {rank_label} · {owner}
            </div>
            """,
            unsafe_allow_html=True
        )

        header_cols = st.columns([3.2, 2.2])
        with header_cols[0]:
            st.markdown(
                "<div style='color:rgba(245,240,232,0.68);font-size:0.95rem;padding:0.2rem 0 0.35rem 0.15rem;'>Player</div>",
                unsafe_allow_html=True
            )
        with header_cols[1]:
            st.markdown(
                "<div style='color:rgba(245,240,232,0.68);font-size:0.95rem;padding:0.2rem 0.15rem 0.35rem 0;text-align:right;'>Score</div>",
                unsafe_allow_html=True
            )

        for p in info["players"]:
            row_cols = st.columns([3.2, 2.2])

            with row_cols[0]:
                st.markdown(
                    f"""
                    <div style="
                        color:#f5f0e8;
                        font-size:1.05rem;
                        padding:0.28rem 0.15rem;
                        border-top:1px solid rgba(255,255,255,0.045);
                    ">
                        {p['name']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with row_cols[1]:
                st.markdown(
                    f"""
                    <div style="
                        color:{score_color(p['kind'])};
                        font-size:1.05rem;
                        font-weight:600;
                        text-align:right;
                        padding:0.28rem 0.15rem;
                        border-top:1px solid rgba(255,255,255,0.045);
                    ">
                        {p['display']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown(
            f"""
            <div style="
                font-family:'Cormorant Garamond',serif;
                font-size:1.18rem;
                font-weight:600;
                color:{score_color(total_kind) if total_kind != 'even' else '#e8c97a'};
                border-top:1px solid rgba(201,168,76,0.22);
                margin-top:0.5rem;
                padding:0.8rem 1rem 0.9rem 1rem;
                text-align:right;
                letter-spacing:0.04em;
            ">
                Pool Total: {total_text}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="masters-header">
    <div class="azalea-row">✦ ✦ ✦</div>
    <p class="masters-year">Augusta National · 2026</p>
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
        data, saturday_worst, sunday_worst = compute(raw_rows)
        load_ok = True
    except Exception as e:
        load_ok = False
        err_msg = str(e)

if not load_ok:
    st.error(f"⛳ Could not fetch leaderboard data: {err_msg}")
    st.stop()

sorted_entries = sorted(data.items(), key=lambda x: x[1]["total"])
rank_labels = format_position_labels(sorted_entries)

# ─────────────────────────────────────────────
#  STANDINGS OVERVIEW
# ─────────────────────────────────────────────
st.markdown(
    '<div class="section-divider"><span class="section-label">🏆 Standings</span></div>',
    unsafe_allow_html=True
)

stand_cols = st.columns(len(sorted_entries))
top_score = sorted_entries[0][1]["total"] if sorted_entries else None

for i, (owner, info) in enumerate(sorted_entries):
    with stand_cols[i]:
        is_first = info["total"] == top_score
        render_standings_card(rank_labels[owner], owner, info["total"], is_first=is_first)

# ─────────────────────────────────────────────
#  INFO BOX
# ─────────────────────────────────────────────
sat_disp = f"+{saturday_worst}" if saturday_worst > 0 else ("E" if saturday_worst == 0 else str(saturday_worst))
sun_disp = f"+{sunday_worst}" if sunday_worst > 0 else ("E" if sunday_worst == 0 else str(sunday_worst))

st.markdown(f"""
<div class="info-box">
    ⛳ <strong>Scoring:</strong> Pool score = sum of each player's score to par.
    If a player misses the cut, their cut score plus the field's worst Saturday score ({sat_disp}) and worst Sunday score ({sun_disp}) is applied.
    Scores refresh every 2 minutes.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PLAYER BREAKDOWNS
# ─────────────────────────────────────────────
st.markdown(
    '<div class="section-divider"><span class="section-label">🌿 Player Breakdown</span></div>',
    unsafe_allow_html=True
)

break_cols = st.columns(2)
for i, (owner, info) in enumerate(sorted_entries):
    with break_cols[i % 2]:
        render_breakdown_card(rank_labels[owner], owner, info)
        st.write("")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;opacity:0.4;font-family:'Cormorant Garamond',serif;
letter-spacing:0.15em;font-size:0.85rem;text-transform:uppercase;color:#c9a84c;">
    A tradition unlike any other &nbsp;·&nbsp; Data via ESPN
</div>
""", unsafe_allow_html=True)
