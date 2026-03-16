
import json
import os
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Preoperative Anemia Treatment Pyramid", page_icon="🩸", layout="wide")

APP_DIR = Path(__file__).resolve().parent
STATE_FILE = APP_DIR / "pbm_competition_shared_state.json"

CASES = [
    {
        "case": 1,
        "title": "Case 1",
        "scenario": "60-year-old woman, Hb 10 g/dL, ferritin 8 ng/mL, TSAT 10%. Surgery in 5 weeks.",
        "question": "What is the best treatment strategy?",
        "options": {
            "A": "Oral iron therapy",
            "B": "Immediate transfusion",
            "C": "ESA alone",
            "D": "No treatment",
        },
        "correct": "A",
        "feedback": {
            "A": "Correct. Oral iron is appropriate when absolute iron deficiency is present and there is enough time before surgery.",
            "B": "Incorrect. Immediate transfusion is not the best first strategy in this stable elective scenario.",
            "C": "Incorrect. ESA alone will not correct iron deficiency adequately.",
            "D": "Incorrect. The patient has treatable preoperative iron deficiency anemia.",
        },
        "clue": "Hint: Oral iron works when enough time is available before surgery.",
        "piece": "Pyramid piece: Oral Iron layer.",
        "explanation": "This patient has absolute iron deficiency anemia with enough time before elective surgery. Oral iron is an appropriate first-line option because iron stores are clearly depleted and there are several weeks available before surgery.",
    },
    {
        "case": 2,
        "title": "Case 2",
        "scenario": "72-year-old man, Hb 9 g/dL, ferritin 15 ng/mL, TSAT 12%. Surgery in 10 days.",
        "question": "What is the best treatment strategy?",
        "options": {
            "A": "Oral iron",
            "B": "Intravenous iron",
            "C": "Wait until surgery",
            "D": "Folic acid",
        },
        "correct": "B",
        "feedback": {
            "A": "Incorrect. Oral iron is too slow for a patient going to surgery in 10 days.",
            "B": "Correct. IV iron is preferred when time before surgery is short.",
            "C": "Incorrect. Delaying treatment misses the chance to optimize the patient.",
            "D": "Incorrect. There is no evidence here that folate deficiency is the main problem.",
        },
        "clue": "Hint: Short time before surgery favors IV iron.",
        "piece": "Pyramid piece: Intravenous Iron layer.",
        "explanation": "The patient has iron deficiency anemia, but surgery is very close. Oral iron will not act quickly enough, so intravenous iron is the best option to optimize hemoglobin in the short preoperative window.",
    },
    {
        "case": 3,
        "title": "Case 3",
        "scenario": "55-year-old woman, Hb 10.5 g/dL, low vitamin B12. Surgery in 4 weeks.",
        "question": "What is the best treatment strategy?",
        "options": {
            "A": "Vitamin B12 replacement",
            "B": "ESA alone",
            "C": "Blood transfusion",
            "D": "Oral iron",
        },
        "correct": "A",
        "feedback": {
            "A": "Correct. B12 deficiency should be corrected directly.",
            "B": "Incorrect. ESA alone will not fix a vitamin B12 deficiency.",
            "C": "Incorrect. Transfusion is not the first-line approach in this elective case.",
            "D": "Incorrect. The key abnormality is B12 deficiency, not iron deficiency.",
        },
        "clue": "Hint: Correct vitamin deficiencies before stimulating erythropoiesis.",
        "piece": "Pyramid piece: Vitamin B12 layer.",
        "explanation": "Low vitamin B12 is the key cause of anemia in this case. The right approach is to replace vitamin B12 directly before considering erythropoiesis-stimulating strategies.",
    },
    {
        "case": 4,
        "title": "Case 4",
        "scenario": "68-year-old man, Hb 8.8 g/dL, low ferritin. Surgery in 7 days.",
        "question": "What is the best treatment strategy?",
        "options": {
            "A": "Intravenous iron",
            "B": "Oral iron",
            "C": "Observation only",
            "D": "Folic acid",
        },
        "correct": "A",
        "feedback": {
            "A": "Correct. IV iron is the fastest appropriate iron replacement option in this scenario.",
            "B": "Incorrect. Oral iron is too slow given the short timeline.",
            "C": "Incorrect. The anemia is significant and should be optimized.",
            "D": "Incorrect. Low ferritin points to iron deficiency rather than folate deficiency.",
        },
        "clue": "Hint: IV iron works faster than oral iron.",
        "piece": "Pyramid piece: Fast optimization piece.",
        "explanation": "This patient has significant iron deficiency anemia and only one week before surgery. IV iron is preferred because it replenishes iron more rapidly than oral therapy.",
    },
    {
        "case": 5,
        "title": "Case 5",
        "scenario": "63-year-old woman, Hb 9.5 g/dL, normal ferritin, low TSAT. Functional iron deficiency. Surgery in 2 weeks.",
        "question": "What is the best treatment strategy?",
        "options": {
            "A": "Oral iron",
            "B": "Intravenous iron",
            "C": "Transfusion",
            "D": "Vitamin B12",
        },
        "correct": "B",
        "feedback": {
            "A": "Incorrect. Functional iron deficiency often responds poorly and too slowly to oral iron.",
            "B": "Correct. Functional iron deficiency usually requires IV iron.",
            "C": "Incorrect. Transfusion is not the best optimization strategy here.",
            "D": "Incorrect. There is no indication that B12 deficiency is the issue.",
        },
        "clue": "Hint: Functional iron deficiency usually requires IV iron.",
        "piece": "Pyramid piece: Functional iron deficiency piece.",
        "explanation": "Normal ferritin with low transferrin saturation suggests functional iron deficiency, where iron is not adequately available for erythropoiesis. IV iron is usually preferred in this setting.",
    },
    {
        "case": 6,
        "title": "Case 6",
        "scenario": "70-year-old patient, Hb 9 g/dL, ferritin adequate, major orthopedic surgery in 3 weeks.",
        "question": "Which option is most appropriate?",
        "options": {
            "A": "ESA plus iron support",
            "B": "Oral iron only",
            "C": "Immediate transfusion",
            "D": "No treatment",
        },
        "correct": "A",
        "feedback": {
            "A": "Correct. ESA can be useful in selected patients when iron availability is ensured.",
            "B": "Incorrect. Oral iron alone may be insufficient here.",
            "C": "Incorrect. Transfusion is not automatically indicated in this elective optimization setting.",
            "D": "Incorrect. Preoperative anemia should be addressed.",
        },
        "clue": "Hint: ESA requires adequate iron availability to work.",
        "piece": "Pyramid piece: ESA layer.",
        "explanation": "In selected patients with preoperative anemia and limited time before surgery, erythropoiesis-stimulating agents may be useful, but only if iron support is adequate.",
    },
    {
        "case": 7,
        "title": "Case 7",
        "scenario": "65-year-old patient, Hb 11 g/dL, low folate level, elective surgery in 6 weeks.",
        "question": "What is the best treatment strategy?",
        "options": {
            "A": "Folic acid replacement",
            "B": "ESA",
            "C": "Transfusion",
            "D": "IV iron",
        },
        "correct": "A",
        "feedback": {
            "A": "Correct. Folate deficiency should be corrected directly before surgery.",
            "B": "Incorrect. ESA is not the first step when folate deficiency is the main issue.",
            "C": "Incorrect. Transfusion is not indicated here.",
            "D": "Incorrect. There is no evidence that iron deficiency is the main problem.",
        },
        "clue": "Hint: Correct folate deficiency before stimulating red cell production.",
        "piece": "Pyramid piece: Folic Acid layer.",
        "explanation": "The anemia is linked to folate deficiency, so folic acid replacement is the most appropriate treatment. Treating the underlying deficiency comes first.",
    },
]

TEAM_COLORS = {
    "team_red": {"primary": "#c81e1e", "soft": "#fff1f2", "accent": "#ef4444", "glow": "rgba(239,68,68,.24)"},
    "team_blue": {"primary": "#1d4ed8", "soft": "#eff6ff", "accent": "#60a5fa", "glow": "rgba(59,130,246,.24)"},
}


def default_team_state(name: str, theme: str):
    return {
        "name": name,
        "theme": theme,
        "current_case": 0,
        "correct_cases": 0,
        "answered_correctly": False,
        "selected_answer": None,
        "show_case_hint": False,
        "attempts_in_case": 0,
        "case_hint_available": False,
        "score": 0,
        "pieces_claimed": 0,
        "finished": False,
        "last_result": None,
        "finish_ts": None,
    }


def default_shared_state():
    return {
        "facilitator_code": "FAC2026",
        "team_codes": {"team_red": "RED2026", "team_blue": "BLUE2026"},
        "timer_minutes": 12,
        "competition_end_ts": None,
        "timer_running": False,
        "projection_mode": False,
        "teams": {
            "team_red": default_team_state("Team Red", "team_red"),
            "team_blue": default_team_state("Team Blue", "team_blue"),
        },
    }


def load_state():
    if not STATE_FILE.exists():
        state = default_shared_state()
        save_state(state)
        return state
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("projection_mode", False)
        for team_key in ("team_red", "team_blue"):
            data["teams"][team_key].setdefault("finish_ts", None)
        return data
    except Exception:
        state = default_shared_state()
        save_state(state)
        return state


def save_state(state):
    tmp = str(STATE_FILE) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_FILE)


def reset_case_state(team):
    team["answered_correctly"] = False
    team["selected_answer"] = None
    team["show_case_hint"] = False
    team["attempts_in_case"] = 0
    team["case_hint_available"] = False
    team["last_result"] = None


def reset_team(team):
    theme = team["theme"]
    name = team["name"]
    fresh = default_team_state(name, theme)
    team.clear()
    team.update(fresh)


def restart_competition(state):
    state["competition_end_ts"] = None
    state["timer_running"] = False
    for team_key in ("team_red", "team_blue"):
        name = state["teams"][team_key]["name"]
        state["teams"][team_key] = default_team_state(name, team_key)
    save_state(state)


def remaining_seconds(state):
    if not state["timer_running"] or state["competition_end_ts"] is None:
        return int(state["timer_minutes"] * 60)
    return max(0, int(state["competition_end_ts"] - time.time()))


def format_clock(seconds):
    return f"{seconds//60:02d}:{seconds%60:02d}"


def winner_key(state):
    red = state["teams"]["team_red"]
    blue = state["teams"]["team_blue"]
    if red["score"] > blue["score"]:
        return "team_red"
    if blue["score"] > red["score"]:
        return "team_blue"
    if red["pieces_claimed"] > blue["pieces_claimed"]:
        return "team_red"
    if blue["pieces_claimed"] > red["pieces_claimed"]:
        return "team_blue"
    red_ts = red.get("finish_ts")
    blue_ts = blue.get("finish_ts")
    if red_ts and blue_ts:
        return "team_red" if red_ts < blue_ts else "team_blue"
    return "tie"


def winner_name(state):
    wk = winner_key(state)
    return "Tie" if wk == "tie" else state["teams"][wk]["name"]


def sound_html(kind="correct"):
    if kind == "correct":
        notes = [660, 784, 988]
        osc = "triangle"
        border = "#16a34a"
        bg = "#f0fdf4"
        icon = "✅"
        label = "Correct answer"
    elif kind == "incorrect":
        notes = [220, 174]
        osc = "sawtooth"
        border = "#dc2626"
        bg = "#fef2f2"
        icon = "❌"
        label = "Incorrect answer"
    else:
        notes = [523, 659, 784, 1047, 1318]
        osc = "sine"
        border = "#f59e0b"
        bg = "#fffbeb"
        icon = "🏆"
        label = "Winner"
    notes_js = ",".join(str(n) for n in notes)
    return f"""
    <div style='padding:10px;border-radius:14px;border:2px solid {border};background:{bg};font-weight:700;text-align:center;'>
        {icon} {label}
    </div>
    <script>
    try {{
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const notes = [{notes_js}];
      notes.forEach((freq, idx) => {{
        const start = ctx.currentTime + idx * 0.12;
        const o = ctx.createOscillator();
        const g = ctx.createGain();
        o.type = "{osc}";
        o.frequency.value = freq;
        o.connect(g); g.connect(ctx.destination);
        g.gain.setValueAtTime(0.0001, start);
        g.gain.exponentialRampToValueAtTime(0.12, start + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, start + 0.18);
        o.start(start);
        o.stop(start + 0.18);
      }});
    }} catch (e) {{}}
    </script>
    """


def play_tone(kind="correct"):
    components.html(sound_html(kind), height=58)


def global_styles():
    st.markdown(
        """
        <style>
        .main {
            background:
                radial-gradient(circle at 10% 5%, rgba(239,68,68,.12), transparent 18%),
                radial-gradient(circle at 90% 5%, rgba(59,130,246,.12), transparent 18%),
                linear-gradient(180deg, #f8fafc 0%, #eef2ff 50%, #f8fafc 100%);
        }
        .block-container {
            max-width: 1220px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
        .glass-card {
            background: rgba(255,255,255,.90);
            border: 1px solid rgba(148,163,184,.24);
            border-radius: 24px;
            box-shadow: 0 16px 34px rgba(15,23,42,.08);
            padding: 1.1rem 1.2rem;
        }
        .minor-card {
            background: white;
            border-radius: 20px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 12px 24px rgba(15,23,42,.06);
            padding: 1rem 1.1rem;
        }
        .metric-pill-red, .metric-pill-blue, .metric-pill-neutral {
            display:inline-block; padding:.38rem .7rem; border-radius:999px; font-weight:700; margin-right:.35rem; margin-bottom:.35rem;
        }
        .metric-pill-red { background:#fff1f2; color:#c81e1e; }
        .metric-pill-blue { background:#eff6ff; color:#1d4ed8; }
        .metric-pill-neutral { background:#f8fafc; color:#334155; }
        .section-title { font-size: 1.3rem; font-weight: 800; margin-bottom:.35rem; }
        div.stButton > button {
            border-radius: 14px;
            border: 1px solid #cbd5e1;
            padding: 0.78rem 1rem;
            font-weight: 700;
        }
        [data-testid="stMetricValue"] { font-size: 2rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_banner():
    svg = """
    <svg width="100%" height="250" viewBox="0 0 1440 250" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="#b91c1c"/>
          <stop offset="48%" stop-color="#dc2626"/>
          <stop offset="100%" stop-color="#1d4ed8"/>
        </linearGradient>
        <linearGradient id="pyr" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="100%" stop-color="#e2e8f0"/>
        </linearGradient>
      </defs>
      <rect x="0" y="0" width="1440" height="250" rx="30" fill="url(#bg)"/>
      <circle cx="122" cy="74" r="18" fill="rgba(255,255,255,.2)"/>
      <circle cx="168" cy="52" r="8" fill="rgba(255,255,255,.18)"/>
      <path d="M92 155 C92 120, 131 102, 131 68 C131 102, 170 120, 170 155 C170 180, 152 198, 131 198 C110 198, 92 180, 92 155Z" fill="#fff"/>
      <g transform="translate(1045,46)">
        <rect x="0" y="20" width="165" height="28" rx="10" fill="#fff" opacity=".98"/>
        <rect x="136" y="25" width="18" height="18" rx="2" fill="#c81e1e"/>
        <line x1="145" y1="54" x2="188" y2="95" stroke="#fff" stroke-width="6"/>
        <circle cx="216" cy="110" r="28" fill="none" stroke="#fff" stroke-width="7"/>
        <path d="M203 110 L212 119 L230 99" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
      </g>

      <g transform="translate(700,55)">
        <rect x="110" y="0" width="100" height="34" rx="10" fill="url(#pyr)" stroke="#fff" stroke-width="2"/>
        <text x="160" y="22" text-anchor="middle" fill="#1e293b" font-size="16" font-weight="800" font-family="Arial, sans-serif">ESA</text>

        <rect x="30" y="48" width="260" height="38" rx="10" fill="url(#pyr)" stroke="#fff" stroke-width="2"/>
        <text x="160" y="72" text-anchor="middle" fill="#1e293b" font-size="15" font-weight="800" font-family="Arial, sans-serif">VITAMINS B12 - B9 - B6</text>

        <rect x="0" y="100" width="150" height="42" rx="10" fill="url(#pyr)" stroke="#fff" stroke-width="2"/>
        <rect x="170" y="100" width="150" height="42" rx="10" fill="url(#pyr)" stroke="#fff" stroke-width="2"/>
        <text x="75" y="126" text-anchor="middle" fill="#1e293b" font-size="13.5" font-weight="800" font-family="Arial, sans-serif">INTRAVENOUS IRON</text>
        <text x="245" y="126" text-anchor="middle" fill="#1e293b" font-size="13.5" font-weight="800" font-family="Arial, sans-serif">ORAL IRON</text>
      </g>

      <text x="228" y="95" fill="#fff" font-size="39" font-weight="800" font-family="Arial, sans-serif">Preoperative Anemia Treatment Pyramid</text>
      <text x="229" y="130" fill="#eef2ff" font-size="18" font-family="Arial, sans-serif">competition mode • anesthesia • bleeding control • PBM</text>
    </svg>
    """
    components.html(svg, height=250)


def render_clock(seconds):
    components.html(
        f"""
        <div style="background:linear-gradient(135deg,#0f172a,#1e293b); color:white; border-radius:24px; padding:14px 18px; text-align:center; box-shadow:0 16px 32px rgba(15,23,42,.18);">
            <div style="font-size:13px; letter-spacing:1px; opacity:.84;">COMPETITION TIMER</div>
            <div id="clock" style="font-size:40px; font-weight:800; margin-top:6px;">{format_clock(seconds)}</div>
        </div>
        <script>
        let total = {seconds};
        const el = document.getElementById("clock");
        function tick(){{
            if(total < 0) return;
            const m = String(Math.floor(total/60)).padStart(2,'0');
            const s = String(total%60).padStart(2,'0');
            el.textContent = `${{m}}:${{s}}`;
            total -= 1;
        }}
        tick();
        setInterval(tick, 1000);
        </script>
        """,
        height=118,
    )


def render_winner_announcement(state):
    wk = winner_key(state)
    title = "Tie"
    accent = "#64748b"
    if wk != "tie":
        title = state["teams"][wk]["name"]
        accent = TEAM_COLORS[wk]["primary"]
    components.html(
        f"""
        <div style="position:relative;overflow:hidden;background:linear-gradient(135deg,{accent},#0f172a);border-radius:28px;padding:26px 24px;color:white;box-shadow:0 18px 40px rgba(15,23,42,.22);">
          <div style="position:absolute;inset:0;background:
              radial-gradient(circle at 10% 20%, rgba(255,255,255,.22), transparent 18%),
              radial-gradient(circle at 88% 18%, rgba(255,255,255,.12), transparent 16%),
              radial-gradient(circle at 50% 100%, rgba(255,255,255,.12), transparent 22%);
          "></div>
          <div style="position:relative;z-index:2;text-align:center;">
            <div style="font-size:18px;letter-spacing:2px;font-weight:700;opacity:.9;">WINNER ANNOUNCEMENT</div>
            <div style="font-size:44px;font-weight:900;margin-top:10px;">{title}</div>
            <div style="font-size:18px;opacity:.9;margin-top:8px;">Preoperative Anemia Treatment Pyramid Champion</div>
            <div style="margin-top:18px;font-size:48px;">🏆 🎉 🩸</div>
          </div>
          <script>
            try {{
              const ctx = new (window.AudioContext || window.webkitAudioContext)();
              const notes = [523,659,784,1047,1318];
              notes.forEach((freq, idx) => {{
                const start = ctx.currentTime + idx * 0.14;
                const o = ctx.createOscillator();
                const g = ctx.createGain();
                o.type = "triangle";
                o.frequency.value = freq;
                o.connect(g); g.connect(ctx.destination);
                g.gain.setValueAtTime(0.0001, start);
                g.gain.exponentialRampToValueAtTime(0.13, start + 0.02);
                g.gain.exponentialRampToValueAtTime(0.0001, start + 0.22);
                o.start(start); o.stop(start + 0.22);
              }});
            }} catch (e) {{}}
          </script>
        </div>
        """,
        height=245,
    )


def render_login(state):
    col1, col2 = st.columns([1.15, .85])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Access portal</div>', unsafe_allow_html=True)
        st.write("Choose your role. Each team sees only its own competition screen after login.")
        role = st.radio("Role", ["Team", "Facilitator", "Auditorium Projection"], horizontal=True)

        if role == "Team":
            team_label = st.selectbox("Team", ["Team Red", "Team Blue"])
            team_key = "team_red" if team_label == "Team Red" else "team_blue"
            code = st.text_input("Team access code", type="password")
            if st.button("Login as team", use_container_width=True):
                if code == state["team_codes"][team_key]:
                    st.session_state["logged_role"] = "team"
                    st.session_state["logged_team"] = team_key
                    st.rerun()
                else:
                    st.error("Incorrect team access code.")
        elif role == "Facilitator":
            code = st.text_input("Facilitator access code", type="password")
            if st.button("Login as facilitator", use_container_width=True):
                if code == state["facilitator_code"]:
                    st.session_state["logged_role"] = "facilitator"
                    st.rerun()
                else:
                    st.error("Incorrect facilitator code.")
        else:
            st.caption("Projection mode is view-only and ideal for the auditorium screen.")
            if st.button("Open auditorium projection", use_container_width=True):
                st.session_state["logged_role"] = "projection"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Game Instructions</div>', unsafe_allow_html=True)
        st.markdown(
            """
            - Each team logs in separately and sees only its own panel.  
            - After the first wrong answer, the **Use hint** button becomes available.  
            - Teams keep retrying the same case until they choose the correct answer.  
            - After a correct answer, they must **claim the pyramid piece from the instructor**.  
            - The explanation remains visible before moving to the next case.  
            - Facilitator mode controls timer, names, codes, leaderboard, and reset.  
            - Auditorium mode shows the live scoreboard and final winner announcement.  
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)


def render_leaderboard_table(state):
    red = state["teams"]["team_red"]
    blue = state["teams"]["team_blue"]
    rows = [
        {"Team": red["name"], "Score": red["score"], "Cases": f"{red['correct_cases']}/{len(CASES)}", "Pieces": red["pieces_claimed"], "Status": "Finished" if red["finished"] else f"Case {red['current_case'] + 1}"},
        {"Team": blue["name"], "Score": blue["score"], "Cases": f"{blue['correct_cases']}/{len(CASES)}", "Pieces": blue["pieces_claimed"], "Status": "Finished" if blue["finished"] else f"Case {blue['current_case'] + 1}"},
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)


def render_facilitator(state):
    top_left, top_mid = st.columns([1.5, .8])
    with top_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Facilitator control room</div>', unsafe_allow_html=True)
        st.markdown(
            f'<span class="metric-pill-red">{state["teams"]["team_red"]["name"]}: {state["teams"]["team_red"]["score"]} pts</span>'
            f'<span class="metric-pill-blue">{state["teams"]["team_blue"]["name"]}: {state["teams"]["team_blue"]["score"]} pts</span>'
            f'<span class="metric-pill-neutral">Leader: {winner_name(state)}</span>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with top_mid:
        render_clock(remaining_seconds(state))

    m1, m2, m3, m4 = st.columns(4)
    red = state["teams"]["team_red"]
    blue = state["teams"]["team_blue"]
    m1.metric(red["name"], red["score"], f"{red['correct_cases']} cases")
    m2.metric(blue["name"], blue["score"], f"{blue['correct_cases']} cases")
    m3.metric("Pieces", f"{red['pieces_claimed']} - {blue['pieces_claimed']}")
    m4.metric("Winner so far", winner_name(state))

    left, right = st.columns([1, 1])
    with left:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Competition setup</div>', unsafe_allow_html=True)
        state["teams"]["team_red"]["name"] = st.text_input("Red team name", value=red["name"])
        state["teams"]["team_blue"]["name"] = st.text_input("Blue team name", value=blue["name"])
        state["timer_minutes"] = st.number_input("Timer (minutes)", min_value=1, max_value=60, value=int(state["timer_minutes"]), step=1)
        if st.button("Save names and timer", use_container_width=True):
            save_state(state)
            st.success("Setup saved.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="minor-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Access codes</div>', unsafe_allow_html=True)
        state["team_codes"]["team_red"] = st.text_input("Red team code", value=state["team_codes"]["team_red"])
        state["team_codes"]["team_blue"] = st.text_input("Blue team code", value=state["team_codes"]["team_blue"])
        state["facilitator_code"] = st.text_input("Facilitator code", value=state["facilitator_code"])
        if st.button("Save access codes", use_container_width=True):
            save_state(state)
            st.success("Codes saved.")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Timer and control</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Start / restart timer", use_container_width=True):
                state["competition_end_ts"] = time.time() + int(state["timer_minutes"] * 60)
                state["timer_running"] = True
                save_state(state)
                st.rerun()
        with c2:
            if st.button("Stop timer", use_container_width=True):
                state["timer_running"] = False
                save_state(state)
                st.rerun()
        if st.button("Open / enable projection mode", use_container_width=True):
            state["projection_mode"] = True
            save_state(state)
            st.success("Projection mode enabled.")
        if st.button("Disable projection mode", use_container_width=True):
            state["projection_mode"] = False
            save_state(state)
            st.success("Projection mode disabled.")
        if st.button("Reset whole competition", use_container_width=True):
            restart_competition(state)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="minor-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Leaderboard</div>', unsafe_allow_html=True)
        render_leaderboard_table(state)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Game Instructions", expanded=False):
        st.markdown(
            """
            - Teams use their own codes to log in.  
            - Teams do not see the other team's answer screen.  
            - The hint appears only after the first wrong answer.  
            - Correct answers unlock a pyramid piece to claim from the instructor.  
            - Wrong answers subtract 1 point. Correct answers add 10 points. Completing all cases adds 5 bonus points.  
            - Projection mode is for the auditorium leaderboard and final winner screen.  
            """
        )

    if red["finished"] or blue["finished"]:
        render_winner_announcement(state)

    if st.button("Logout facilitator"):
        st.session_state.pop("logged_role", None)
        st.rerun()


def render_team_screen(state, team_key):
    team = state["teams"][team_key]
    other_key = "team_blue" if team_key == "team_red" else "team_red"
    other_team = state["teams"][other_key]
    colors = TEAM_COLORS[team_key]

    top1, top2, top3 = st.columns([1.7, .8, .8])
    with top1:
        st.markdown(
            f"""
            <div class="glass-card" style="border-top:6px solid {colors['primary']}; box-shadow: 0 16px 34px {colors['glow']};">
                <div style="font-size:34px;font-weight:900;color:{colors['primary']};">{team['name']}</div>
                <div style="font-size:16px;color:#475569;margin-top:4px;">Preoperative Anemia Treatment Pyramid</div>
                <div style="margin-top:10px;">
                    <span class="metric-pill-neutral">Score: {team['score']}</span>
                    <span class="metric-pill-neutral">Cases solved: {team['correct_cases']}/{len(CASES)}</span>
                    <span class="metric-pill-neutral">Pieces: {team['pieces_claimed']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top2:
        render_clock(remaining_seconds(state))
    with top3:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Competition status</div>', unsafe_allow_html=True)
        st.write(f"Opponent: **{other_team['name']}**")
        st.write(f"Leader: **{winner_name(state)}**")
        if st.button("Refresh status", use_container_width=True):
            st.rerun()
        if st.button("Logout", use_container_width=True):
            st.session_state.pop("logged_role", None)
            st.session_state.pop("logged_team", None)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Game Instructions", expanded=False):
        st.markdown(
            """
            - Answer the case using the buttons.  
            - After the first wrong answer, **Use hint** becomes available.  
            - Keep trying until the correct answer is selected.  
            - After a correct answer, claim the pyramid piece from the instructor.  
            - Wrong answers subtract 1 point. Correct answers add 10 points.  
            """
        )

    if team["finished"]:
        render_winner_announcement(state)
        st.success(f"{team['name']} completed all cases.")
        return

    case = CASES[team["current_case"]]
    st.progress(team["current_case"] / len(CASES))

    st.markdown(
        f"""
        <div class="glass-card" style="border-left:8px solid {colors['primary']};">
            <div style="font-size:26px;font-weight:800;">{case['title']}</div>
            <div style="margin-top:10px;"><b>Clinical scenario:</b> {case['scenario']}</div>
            <div style="margin-top:10px;"><b>Question:</b> {case['question']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if team["last_result"] == "correct":
        play_tone("correct")
        st.success(case["feedback"][case["correct"]])
        st.success("Correct answer. You may now claim a pyramid piece from the instructor.")
    elif team["last_result"] == "incorrect" and team["selected_answer"]:
        play_tone("incorrect")
        st.error(case["feedback"][team["selected_answer"]])
        st.warning("Incorrect answer. Try again and analyze the clinical scenario.")

    option_items = list(case["options"].items())
    cols = st.columns(2)
    for idx, (key, value) in enumerate(option_items):
        with cols[idx % 2]:
            if st.button(f"{key}. {value}", key=f"{team_key}_{case['case']}_{key}", use_container_width=True):
                team["selected_answer"] = key
                if key == case["correct"]:
                    team["answered_correctly"] = True
                    team["last_result"] = "correct"
                    team["score"] += 10
                else:
                    team["attempts_in_case"] += 1
                    team["case_hint_available"] = team["attempts_in_case"] >= 1
                    team["last_result"] = "incorrect"
                    team["score"] = max(0, team["score"] - 1)
                save_state(state)
                st.rerun()

    l, r = st.columns([1, 1])
    with l:
        if team["case_hint_available"] and not team["answered_correctly"]:
            if st.button("Use hint", use_container_width=True):
                team["show_case_hint"] = True
                save_state(state)
                st.rerun()
        if team["show_case_hint"] and not team["answered_correctly"]:
            st.markdown(
                f"""
                <div style="background:#fff7ed;border:1px solid #fdba74;color:#7c2d12;border-radius:16px;padding:14px;margin-top:8px;">
                    <b>{case['clue']}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with r:
        st.markdown(
            f"""
            <div style="background:{colors['soft']};border:1px solid {colors['accent']};color:#334155;border-radius:16px;padding:14px;">
                <b>Clinical focus:</b> Match the type of anemia to the available time before surgery.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if team["answered_correctly"]:
        st.markdown(
            f"""
            <div style="background:{colors['soft']};border:1px solid {colors['accent']};color:{colors['primary']};border-radius:16px;padding:14px;margin-top:10px;">
                <b>Claim from instructor:</b> {case['piece']}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style="background:#f0fdf4;border:1px solid #86efac;color:#166534;border-radius:16px;padding:14px;margin-top:10px;">
                <b>Why this is correct:</b> {case['explanation']}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to next case", use_container_width=True):
            team["correct_cases"] += 1
            team["pieces_claimed"] += 1
            team["current_case"] += 1
            if team["current_case"] >= len(CASES):
                team["finished"] = True
                team["score"] += 5
                team["finish_ts"] = time.time()
            reset_case_state(team)
            save_state(state)
            st.rerun()
    else:
        st.caption("The hint becomes available after the first wrong answer.")


def render_projection(state):
    red = state["teams"]["team_red"]
    blue = state["teams"]["team_blue"]
    wk = winner_key(state)

    st.markdown(
        """
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:42px;font-weight:900;">AUDITORIUM MODE</div>
            <div style="font-size:18px;color:#475569;margin-top:8px;">Preoperative Anemia Treatment Pyramid</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top1, top2 = st.columns([1.2, .8])
    with top1:
        render_winner_announcement(state)
    with top2:
        render_clock(remaining_seconds(state))

    cols = st.columns(2)
    for idx, team_key in enumerate(["team_red", "team_blue"]):
        team = state["teams"][team_key]
        colors = TEAM_COLORS[team_key]
        with cols[idx]:
            border = f"8px solid {colors['primary']}"
            shadow = f"0 20px 40px {colors['glow']}"
            leader_badge = "🏆 LEADING" if wk == team_key else "COMPETING"
            st.markdown(
                f"""
                <div style="background:white;border-radius:26px;padding:24px;border-top:{border};box-shadow:{shadow};">
                    <div style="font-size:34px;font-weight:900;color:{colors['primary']};">{team['name']}</div>
                    <div style="margin-top:8px;font-size:18px;color:#475569;">{leader_badge}</div>
                    <div style="margin-top:18px;font-size:64px;font-weight:900;color:#0f172a;">{team['score']}</div>
                    <div style="margin-top:10px;font-size:19px;color:#334155;">Cases solved: <b>{team['correct_cases']}/{len(CASES)}</b></div>
                    <div style="margin-top:8px;font-size:19px;color:#334155;">Pieces claimed: <b>{team['pieces_claimed']}</b></div>
                    <div style="margin-top:8px;font-size:19px;color:#334155;">Status: <b>{"Finished" if team['finished'] else "In progress"}</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="minor-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Professional leaderboard</div>', unsafe_allow_html=True)
    render_leaderboard_table(state)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Refresh projection", use_container_width=True):
            st.rerun()
    with c2:
        if st.button("Exit projection mode", use_container_width=True):
            st.session_state.pop("logged_role", None)
            st.rerun()


global_styles()
render_banner()
state = load_state()

role = st.session_state.get("logged_role")
if role is None:
    render_login(state)
elif role == "facilitator":
    render_facilitator(state)
elif role == "projection":
    render_projection(state)
else:
    team_key = st.session_state.get("logged_team", "team_red")
    render_team_screen(state, team_key)
