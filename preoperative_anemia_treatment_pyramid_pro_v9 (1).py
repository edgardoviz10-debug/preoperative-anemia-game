
import json, os, time, random
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Preoperative Anemia Treatment Pyramid", page_icon="🩸", layout="wide")

APP_DIR = Path(__file__).resolve().parent
STATE_FILE = APP_DIR / "pbm_competition_shared_state.json"

CASES = [
    {"case":1,"title":"Case 1","type":"mcq","scenario":"60-year-old woman, Hb 10 g/dL, ferritin 8 ng/mL, TSAT 10%. Surgery in 5 weeks.","question":"What is the best treatment strategy?","options":{"A":"Oral iron therapy","B":"Immediate transfusion","C":"ESA alone","D":"No treatment"},"correct":"A","feedback":{"A":"Correct. Oral iron is appropriate when absolute iron deficiency is present and there is enough time before surgery.","B":"Incorrect. Immediate transfusion is not the best first strategy in this stable elective scenario.","C":"Incorrect. ESA alone will not correct iron deficiency adequately.","D":"Incorrect. The patient has treatable preoperative iron deficiency anemia."},"clue":"Hint: Oral iron works when enough time is available before surgery.","piece":"Pyramid piece: Oral Iron layer.","explanation":"This patient has absolute iron deficiency anemia with enough time before elective surgery. Oral iron is an appropriate first-line option because iron stores are clearly depleted and there are several weeks available before surgery."},
    {"case":2,"title":"Case 2","type":"mcq","scenario":"72-year-old man, Hb 9 g/dL, ferritin 15 ng/mL, TSAT 12%. Surgery in 10 days.","question":"What is the best treatment strategy?","options":{"A":"Oral iron","B":"Intravenous iron","C":"Wait until surgery","D":"Folic acid"},"correct":"B","feedback":{"A":"Incorrect. Oral iron is too slow for a patient going to surgery in 10 days.","B":"Correct. IV iron is preferred when time before surgery is short.","C":"Incorrect. Delaying treatment misses the chance to optimize the patient.","D":"Incorrect. There is no evidence here that folate deficiency is the main problem."},"clue":"Hint: Short time before surgery favors IV iron.","piece":"Pyramid piece: Intravenous Iron layer.","explanation":"The patient has iron deficiency anemia, but surgery is very close. Oral iron will not act quickly enough, so intravenous iron is the best option to optimize hemoglobin in the short preoperative window."},
    {"case":3,"title":"Case 3","type":"mcq","scenario":"55-year-old woman, Hb 10.5 g/dL, low vitamin B12. Surgery in 4 weeks.","question":"What is the best treatment strategy?","options":{"A":"Vitamin B12 replacement","B":"ESA alone","C":"Blood transfusion","D":"Oral iron"},"correct":"A","feedback":{"A":"Correct. B12 deficiency should be corrected directly.","B":"Incorrect. ESA alone will not fix a vitamin B12 deficiency.","C":"Incorrect. Transfusion is not the first-line approach in this elective case.","D":"Incorrect. The key abnormality is B12 deficiency, not iron deficiency."},"clue":"Hint: Correct vitamin deficiencies before stimulating erythropoiesis.","piece":"Pyramid piece: Vitamin B12 layer.","explanation":"Low vitamin B12 is the key cause of anemia in this case. The right approach is to replace vitamin B12 directly before considering erythropoiesis-stimulating strategies."},
    {"case":4,"title":"Case 4","type":"mcq","scenario":"68-year-old man, Hb 8.8 g/dL, low ferritin. Surgery in 7 days.","question":"What is the best treatment strategy?","options":{"A":"Intravenous iron","B":"Oral iron","C":"Observation only","D":"Folic acid"},"correct":"A","feedback":{"A":"Correct. IV iron is the fastest appropriate iron replacement option in this scenario.","B":"Incorrect. Oral iron is too slow given the short timeline.","C":"Incorrect. The anemia is significant and should be optimized.","D":"Incorrect. Low ferritin points to iron deficiency rather than folate deficiency."},"clue":"Hint: IV iron works faster than oral iron.","piece":"Pyramid piece: Fast optimization piece.","explanation":"This patient has significant iron deficiency anemia and only one week before surgery. IV iron is preferred because it replenishes iron more rapidly than oral therapy."},
    {"case":5,"title":"Case 5","type":"sequence","scenario":"63-year-old woman, Hb 9.5 g/dL, normal ferritin, low TSAT, functional iron deficiency. Elective surgery in 2 weeks.","question":"Choose the correct management sequence.","cards":["Measure ferritin","Calculate iron deficit","IV iron","Reevaluate Hb","Oral iron","ESA"],"correct_sequence":["Measure ferritin","Calculate iron deficit","IV iron","Reevaluate Hb"],"clue":"Hint: First confirm iron status, then estimate replacement need, then choose the fastest treatment, then reassess response.","piece":"Pyramid piece: Clinical sequencing mastery piece.","explanation":"In functional iron deficiency with limited time before surgery, the logical sequence is to assess iron status, estimate the iron deficit, use IV iron for rapid optimization, and then reevaluate hemoglobin response."},
    {"case":6,"title":"Case 6","type":"matching","scenario":"Matching challenge: link each treatment with its usual dose and frequency of administration.","question":"Match oral iron, intravenous iron, erythropoietin, vitamins B6, B9 and B12 with the correct dose and frequency.","clue":"Hint: Oral therapies are usually daily; IV iron is usually delivered in 1–2 sessions; ESA is usually weekly.","piece":"Pyramid piece: Dosing and frequency mastery piece.","explanation":"Correct treatment matching strengthens practical PBM decisions: oral iron needs time and daily dosing, IV iron is rapid, ESA is typically weekly, folate and B6 are daily, and B12 replacement is often weekly in deficiency correction."},
    {"case":7,"title":"Case 7","type":"board","scenario":"Concept discovery board: uncover and match related concepts until the whole board is solved.","question":"Reveal two related concepts at a time. The case is won only when the full board is discovered.","clue":"Hint: Match deficiency states, timeline concepts and therapeutic choices that belong together.","piece":"Pyramid piece: Integration and concept board mastery piece.","explanation":"The final board integrates diagnosis and treatment logic: anemia mechanism, timing and the most appropriate PBM tool must align to build the full treatment pyramid."},
]

TEAM_COLORS = {
    "team_red":{"primary":"#c81e1e","soft":"#fff1f2","accent":"#ef4444","glow":"rgba(239,68,68,.24)"},
    "team_blue":{"primary":"#1d4ed8","soft":"#eff6ff","accent":"#60a5fa","glow":"rgba(59,130,246,.24)"},
}

MATCHING_TREATMENTS = ["Oral Iron","Intravenous Iron","Erythropoietin (ESA)","Vitamin B6","Vitamin B9 (Folic Acid)","Vitamin B12"]
MATCHING_DOSES = ["100–200 mg elemental iron/day","1000 mg","300–600 IU/kg","25–50 mg/day","1–5 mg/day","1000 mcg"]
MATCHING_FREQS = ["Daily for 4–8 weeks","1–2 sessions","Weekly / 3–4 preoperative doses","Daily","Daily","Weekly"]
MATCHING_CORRECT = {
    "Oral Iron":("100–200 mg elemental iron/day","Daily for 4–8 weeks"),
    "Intravenous Iron":("1000 mg","1–2 sessions"),
    "Erythropoietin (ESA)":("300–600 IU/kg","Weekly / 3–4 preoperative doses"),
    "Vitamin B6":("25–50 mg/day","Daily"),
    "Vitamin B9 (Folic Acid)":("1–5 mg/day","Daily"),
    "Vitamin B12":("1000 mcg","Weekly"),
}
BOARD_PAIRS = [
    ("Iron","Iron deficiency anemia"),
    ("Intravenous iron","Functional iron deficiency"),
    ("Vitamin B12","Low vitamin B12"),
    ("Vitamin B9","Low folate"),
    ("ESA","Adequate iron availability"),
    ("Short time before surgery","Rapid optimization"),
]

def default_board_cards():
    cards=[]
    for i,(a,b) in enumerate(BOARD_PAIRS):
        cards.append({"id":f"{i}_a","pair":i,"label":a})
        cards.append({"id":f"{i}_b","pair":i,"label":b})
    random.shuffle(cards)
    return cards

def shuffled_matching_lists():
    doses = MATCHING_DOSES[:]
    freqs = MATCHING_FREQS[:]
    random.shuffle(doses)
    random.shuffle(freqs)
    return doses, freqs

def shuffled_sequence_cards():
    cards = CASES[4]["cards"][:]
    random.shuffle(cards)
    return cards

def default_team_state(name, theme):
    dose_order, freq_order = shuffled_matching_lists()
    return {
        "name":name,"theme":theme,"current_case":0,"correct_cases":0,"answered_correctly":False,"selected_answer":None,
        "show_case_hint":False,"attempts_in_case":0,"case_hint_available":False,"score":0,"pieces_claimed":0,"finished":False,
        "last_result":None,"finish_ts":None,"case5_sequence":[],"case5_card_pool":shuffled_sequence_cards(),
        "case6_matches":{},"case6_freqs":{},"case6_dose_order":dose_order,"case6_freq_order":freq_order,
        "case7_cards":default_board_cards(),"case7_selected":[],"case7_matched":[],"case7_message":"","case7_anim":""
    }

def default_shared_state():
    return {"facilitator_code":"FAC2026","team_codes":{"team_red":"RED2026","team_blue":"BLUE2026"},"timer_minutes":12,
            "competition_end_ts":None,"timer_running":False,"paused_remaining_seconds":12*60,
            "teams":{"team_red":default_team_state("Team Red","team_red"),"team_blue":default_team_state("Team Blue","team_blue")}}

def load_state():
    if not STATE_FILE.exists():
        state=default_shared_state(); save_state(state); return state
    try:
        with open(STATE_FILE,"r",encoding="utf-8") as f: data=json.load(f)
        data.setdefault("paused_remaining_seconds", int(data.get("timer_minutes", 12) * 60))
        for tk in ("team_red","team_blue"):
            t=data["teams"][tk]
            t.setdefault("finish_ts",None); t.setdefault("case5_sequence",[]); t.setdefault("case5_card_pool", shuffled_sequence_cards())
            t.setdefault("case6_matches",{}); t.setdefault("case6_freqs",{})
            if "case6_dose_order" not in t or sorted(t["case6_dose_order"]) != sorted(MATCHING_DOSES):
                t["case6_dose_order"], t["case6_freq_order"] = shuffled_matching_lists()
            if "case6_freq_order" not in t or sorted(t["case6_freq_order"]) != sorted(MATCHING_FREQS):
                t["case6_dose_order"], t["case6_freq_order"] = shuffled_matching_lists()
            t.setdefault("case7_cards",default_board_cards()); t.setdefault("case7_selected",[]); t.setdefault("case7_matched",[])
            t.setdefault("case7_message",""); t.setdefault("case7_anim","")
        return data
    except Exception:
        state=default_shared_state(); save_state(state); return state

def save_state(state):
    tmp=str(STATE_FILE)+".tmp"
    with open(tmp,"w",encoding="utf-8") as f: json.dump(state,f,ensure_ascii=False,indent=2)
    os.replace(tmp, STATE_FILE)

def reset_case_state(team):
    team["answered_correctly"]=False; team["selected_answer"]=None; team["show_case_hint"]=False; team["attempts_in_case"]=0; team["case_hint_available"]=False; team["last_result"]=None
    if team["current_case"]==4:
        team["case5_sequence"]=[]; team["case5_card_pool"]=shuffled_sequence_cards()
    if team["current_case"]==5:
        team["case6_matches"]={}; team["case6_freqs"]={}; team["case6_dose_order"], team["case6_freq_order"] = shuffled_matching_lists()
    if team["current_case"]==6:
        team["case7_cards"]=default_board_cards(); team["case7_selected"]=[]; team["case7_matched"]=[]; team["case7_message"]=""; team["case7_anim"]=""

def restart_competition(state):
    state["competition_end_ts"]=None; state["timer_running"]=False; state["paused_remaining_seconds"]=int(state["timer_minutes"]*60)
    for tk in ("team_red","team_blue"):
        name=state["teams"][tk]["name"]; state["teams"][tk]=default_team_state(name, tk)
    save_state(state)

def remaining_seconds(state):
    if state["timer_running"] and state["competition_end_ts"] is not None:
        remaining = max(0, int(state["competition_end_ts"]-time.time()))
        state["paused_remaining_seconds"] = remaining
        return remaining
    return int(state.get("paused_remaining_seconds", state["timer_minutes"]*60))

def format_clock(seconds): return f"{seconds//60:02d}:{seconds%60:02d}"

def winner_key(state):
    red,blue=state["teams"]["team_red"],state["teams"]["team_blue"]
    if red["score"]>blue["score"]: return "team_red"
    if blue["score"]>red["score"]: return "team_blue"
    if red["pieces_claimed"]>blue["pieces_claimed"]: return "team_red"
    if blue["pieces_claimed"]>red["pieces_claimed"]: return "team_blue"
    rt,bt=red.get("finish_ts"),blue.get("finish_ts")
    if rt and bt: return "team_red" if rt<bt else "team_blue"
    return "tie"

def winner_name(state):
    wk=winner_key(state)
    return "Tie" if wk=="tie" else state["teams"][wk]["name"]

def sound_html(kind="correct"):
    if kind=="correct":
        notes=[660,784,988]; osc="triangle"; border="#16a34a"; bg="#f0fdf4"; icon="✅"; label="Correct answer"; height=58
    elif kind=="incorrect":
        notes=[220,174]; osc="sawtooth"; border="#dc2626"; bg="#fef2f2"; icon="❌"; label="Incorrect answer"; height=58
    else:
        notes=[523,659,784,1047,1318]; osc="sine"; border="#f59e0b"; bg="#fffbeb"; icon="🏆"; label="Winner"; height=70
    notes_js=",".join(str(n) for n in notes)
    html=f"""
    <div style='padding:10px;border-radius:14px;border:2px solid {border};background:{bg};font-weight:700;text-align:center;'>{icon} {label}</div>
    <script>
    try {{
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const notes = [{notes_js}];
      notes.forEach((freq, idx) => {{
        const start = ctx.currentTime + idx * 0.12;
        const o = ctx.createOscillator(); const g = ctx.createGain();
        o.type = "{osc}"; o.frequency.value = freq; o.connect(g); g.connect(ctx.destination);
        g.gain.setValueAtTime(0.0001, start); g.gain.exponentialRampToValueAtTime(0.12, start + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, start + 0.18);
        o.start(start); o.stop(start + 0.18);
      }});
    }} catch (e) {{}}
    </script>"""
    return html,height

def play_tone(kind="correct"):
    html,height=sound_html(kind); components.html(html, height=height)

st.markdown("""
<style>
.main {
    background:
      radial-gradient(circle at 10% 5%, rgba(239,68,68,.12), transparent 18%),
      radial-gradient(circle at 90% 5%, rgba(59,130,246,.12), transparent 18%),
      linear-gradient(180deg, #f8fafc 0%, #eef2ff 50%, #f8fafc 100%);
}
.block-container {max-width:1220px;padding-top:1rem;padding-bottom:2rem;}
.glass-card {background:rgba(255,255,255,.90);border:1px solid rgba(148,163,184,.24);border-radius:24px;box-shadow:0 16px 34px rgba(15,23,42,.08);padding:1.1rem 1.2rem;}
.minor-card {background:white;border-radius:20px;border:1px solid #e2e8f0;box-shadow:0 12px 24px rgba(15,23,42,.06);padding:1rem 1.1rem;}
.metric-pill-red,.metric-pill-blue,.metric-pill-neutral {display:inline-block;padding:.38rem .7rem;border-radius:999px;font-weight:700;margin-right:.35rem;margin-bottom:.35rem;}
.metric-pill-red {background:#fff1f2;color:#c81e1e;} .metric-pill-blue {background:#eff6ff;color:#1d4ed8;} .metric-pill-neutral {background:#f8fafc;color:#334155;}
.section-title {font-size:1.3rem;font-weight:800;margin-bottom:.35rem;}
.sequence-slot {background:#f8fafc;border:1px dashed #94a3b8;border-radius:16px;padding:14px; min-height:78px;}
.card-pick {background:linear-gradient(180deg,#ffffff,#f8fafc); border:1px solid #cbd5e1; border-radius:18px; box-shadow:0 10px 22px rgba(15,23,42,.06); padding:8px;}
div.stButton > button {border-radius:14px;border:1px solid #cbd5e1;padding:.78rem 1rem;font-weight:700;min-height:3rem;}
[data-testid="stMetricValue"] {font-size:2rem;}
</style>
""", unsafe_allow_html=True)

components.html("""
<svg width="100%" height="260" viewBox="0 0 1440 260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#b91c1c"/><stop offset="48%" stop-color="#dc2626"/><stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <linearGradient id="pyr" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#e2e8f0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="1440" height="260" rx="30" fill="url(#bg)"/>
  <circle cx="122" cy="74" r="18" fill="rgba(255,255,255,.2)"/><circle cx="168" cy="52" r="8" fill="rgba(255,255,255,.18)"/>
  <path d="M92 165 C92 130, 131 112, 131 78 C131 112, 170 130, 170 165 C170 190, 152 208, 131 208 C110 208, 92 190, 92 165Z" fill="#fff"/>
  <g transform="translate(1035,56)">
    <rect x="0" y="20" width="165" height="28" rx="10" fill="#fff" opacity=".98"/><rect x="136" y="25" width="18" height="18" rx="2" fill="#c81e1e"/>
    <line x1="145" y1="54" x2="188" y2="95" stroke="#fff" stroke-width="6"/><circle cx="216" cy="110" r="28" fill="none" stroke="#fff" stroke-width="7"/>
    <path d="M203 110 L212 119 L230 99" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="228" y="88" fill="#fff" font-size="39" font-weight="800" font-family="Arial, sans-serif">Preoperative Anemia Treatment Pyramid</text>
  <text x="229" y="122" fill="#eef2ff" font-size="18" font-family="Arial, sans-serif">competition mode • anesthesia • bleeding control • PBM</text>
  <g transform="translate(820,136)">
    <rect x="110" y="0" width="100" height="34" rx="10" fill="url(#pyr)" stroke="#fff" stroke-width="2"/>
    <text x="160" y="22" text-anchor="middle" fill="#1e293b" font-size="16" font-weight="800" font-family="Arial, sans-serif">ESA</text>
    <rect x="30" y="48" width="260" height="38" rx="10" fill="url(#pyr)" stroke="#fff" stroke-width="2"/>
    <text x="160" y="72" text-anchor="middle" fill="#1e293b" font-size="15" font-weight="800" font-family="Arial, sans-serif">VITAMINS B12 - B9 - B6</text>
    <rect x="0" y="100" width="150" height="42" rx="10" fill="url(#pyr)" stroke="#fff" stroke-width="2"/><rect x="170" y="100" width="150" height="42" rx="10" fill="url(#pyr)" stroke="#fff" stroke-width="2"/>
    <text x="75" y="126" text-anchor="middle" fill="#1e293b" font-size="13.5" font-weight="800" font-family="Arial, sans-serif">INTRAVENOUS IRON</text><text x="245" y="126" text-anchor="middle" fill="#1e293b" font-size="13.5" font-weight="800" font-family="Arial, sans-serif">ORAL IRON</text>
  </g>
</svg>
""", height=260)

def render_clock(seconds, running=False):
    clock_id = f"clock_{'run' if running else 'stop'}_{int(time.time()*1000)%1000000}"
    script = f"""
    <script>
    let total = {seconds};
    const el = document.getElementById("{clock_id}");
    function tick(){{
      if(!el || total < 0) return;
      const m = String(Math.floor(total/60)).padStart(2,'0');
      const s = String(total%60).padStart(2,'0');
      el.textContent = `${{m}}:${{s}}`;
      total -= 1;
    }}
    tick();
    window.__pyramidClockInterval = window.__pyramidClockInterval || null;
    if(window.__pyramidClockInterval) clearInterval(window.__pyramidClockInterval);
    window.__pyramidClockInterval = setInterval(tick, 1000);
    </script>
    """ if running else ""
    components.html(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b); color:white; border-radius:24px; padding:14px 18px; text-align:center; box-shadow:0 16px 32px rgba(15,23,42,.18);">
      <div style="font-size:13px; letter-spacing:1px; opacity:.84;">COMPETITION TIMER</div>
      <div id="{clock_id}" style="font-size:40px; font-weight:800; margin-top:6px;">{format_clock(seconds)}</div>
    </div>
    {script}
    """, height=118)

def render_winner_announcement():
    wk=winner_key(state); title="Tie"; accent="#64748b"
    if wk!="tie": title=state["teams"][wk]["name"]; accent=TEAM_COLORS[wk]["primary"]
    components.html(f"""
    <div style="position:relative;overflow:hidden;background:linear-gradient(135deg,{accent},#0f172a);border-radius:28px;padding:26px 24px;color:white;box-shadow:0 18px 40px rgba(15,23,42,.22);">
      <div style="position:absolute;inset:0;background:radial-gradient(circle at 10% 20%, rgba(255,255,255,.22), transparent 18%),radial-gradient(circle at 88% 18%, rgba(255,255,255,.12), transparent 16%),radial-gradient(circle at 50% 100%, rgba(255,255,255,.12), transparent 22%);"></div>
      <div style="position:relative;z-index:2;text-align:center;">
        <div style="font-size:18px;letter-spacing:2px;font-weight:700;opacity:.9;">WINNER ANNOUNCEMENT</div>
        <div style="font-size:44px;font-weight:900;margin-top:10px;">{title}</div>
        <div style="font-size:18px;opacity:.9;margin-top:8px;">Preoperative Anemia Treatment Pyramid Champion</div>
        <div style="margin-top:18px;font-size:48px;">🏆 🎉 🩸</div>
      </div>
    </div>
    """, height=220)

state = load_state()

def render_leaderboard_table():
    red, blue = state["teams"]["team_red"], state["teams"]["team_blue"]
    rows=[{"Team":red["name"],"Score":red["score"],"Cases":f"{red['correct_cases']}/{len(CASES)}","Pieces":red["pieces_claimed"],"Status":"Finished" if red["finished"] else f"Case {red['current_case']+1}"},
          {"Team":blue["name"],"Score":blue["score"],"Cases":f"{blue['correct_cases']}/{len(CASES)}","Pieces":blue["pieces_claimed"],"Status":"Finished" if blue["finished"] else f"Case {blue['current_case']+1}"}]
    st.dataframe(rows, use_container_width=True, hide_index=True)

def finish_current_case(team):
    team["correct_cases"] += 1; team["pieces_claimed"] += 1; team["current_case"] += 1
    if team["current_case"] >= len(CASES):
        team["finished"] = True; team["score"] += 5; team["finish_ts"] = time.time()
    reset_case_state(team); save_state(state)

def render_case_header(case, colors):
    st.markdown(f"""<div class="glass-card" style="border-left:8px solid {colors['primary']};"><div style="font-size:26px;font-weight:800;">{case['title']}</div><div style="margin-top:10px;"><b>Clinical scenario:</b> {case['scenario']}</div><div style="margin-top:10px;"><b>Question:</b> {case['question']}</div></div>""", unsafe_allow_html=True)

def render_mcq_case(case, team, team_key, colors):
    if team["last_result"]=="correct":
        play_tone("correct"); st.success(case["feedback"][case["correct"]]); st.success("Correct answer. You may now claim a pyramid piece from the instructor.")
    elif team["last_result"]=="incorrect" and team["selected_answer"]:
        play_tone("incorrect"); st.error(case["feedback"][team["selected_answer"]]); st.warning("Incorrect answer. Try again and analyze the clinical scenario.")
    cols=st.columns(2)
    for idx,(key,value) in enumerate(case["options"].items()):
        with cols[idx%2]:
            if st.button(f"{key}. {value}", key=f"{team_key}_{case['case']}_{key}", use_container_width=True):
                team["selected_answer"]=key
                if key==case["correct"]:
                    team["answered_correctly"]=True; team["last_result"]="correct"; team["score"] += 10
                else:
                    team["attempts_in_case"] += 1; team["case_hint_available"]=True; team["last_result"]="incorrect"; team["score"]=max(0, team["score"]-1)
                save_state(state); st.rerun()
    l,r=st.columns([1,1])
    with l:
        if team["case_hint_available"] and not team["answered_correctly"] and st.button("Use hint", key=f"hint_{team_key}_{case['case']}", use_container_width=True):
            team["show_case_hint"]=True; save_state(state); st.rerun()
        if team["show_case_hint"] and not team["answered_correctly"]:
            st.markdown(f"""<div style="background:#fff7ed;border:1px solid #fdba74;color:#7c2d12;border-radius:16px;padding:14px;margin-top:8px;"><b>{case['clue']}</b></div>""", unsafe_allow_html=True)
    with r:
        st.markdown(f"""<div style="background:{colors['soft']};border:1px solid {colors['accent']};color:#334155;border-radius:16px;padding:14px;"><b>Clinical focus:</b> Match the type of anemia to the available time before surgery.</div>""", unsafe_allow_html=True)
    if team["answered_correctly"]:
        st.markdown(f"""<div style="background:{colors['soft']};border:1px solid {colors['accent']};color:{colors['primary']};border-radius:16px;padding:14px;margin-top:10px;"><b>Claim from instructor:</b> {case['piece']}</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="background:#f0fdf4;border:1px solid #86efac;color:#166534;border-radius:16px;padding:14px;margin-top:10px;"><b>Why this is correct:</b> {case['explanation']}</div>""", unsafe_allow_html=True)
        if st.button("Go to next case", key=f"next_{team_key}_{case['case']}", use_container_width=True):
            finish_current_case(team); st.rerun()
    else:
        st.caption("The hint becomes available after the first wrong answer.")

def render_sequence_case(case, team, team_key, colors):
    if team["last_result"]=="correct":
        play_tone("correct"); st.success("Correct sequence. You may now claim a pyramid piece from the instructor.")
    elif team["last_result"]=="incorrect":
        play_tone("incorrect"); st.error("Incorrect sequence. Review the order of management."); st.warning("Try again. The hint is available after the first incorrect attempt.")
    st.markdown('<div class="minor-card">', unsafe_allow_html=True)
    st.markdown("### Drag-style sequence cards")
    st.caption("Tap a card to place it into the next available slot. Cards appear in random order each time.")
    available = [c for c in team["case5_card_pool"] if c not in team["case5_sequence"]]
    cols = st.columns(3)
    for idx, card in enumerate(available):
        with cols[idx % 3]:
            st.markdown('<div class="card-pick">', unsafe_allow_html=True)
            if st.button(f"⬇️ {card}", key=f"{team_key}_seq_card_{idx}_{card}", use_container_width=True):
                if len(team["case5_sequence"]) < 4:
                    team["case5_sequence"].append(card); save_state(state); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("### Drop zone")
    slots = st.columns(4)
    for i in range(4):
        with slots[i]:
            if i < len(team["case5_sequence"]):
                st.markdown(f"""<div class="sequence-slot"><div style="font-size:13px;color:#64748b;font-weight:700;">STEP {i+1}</div><div style="margin-top:8px;font-weight:800;">{team["case5_sequence"][i]}</div></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="sequence-slot"><div style="font-size:13px;color:#94a3b8;font-weight:700;">STEP {i+1}</div><div style="margin-top:8px;color:#94a3b8;">Drop card here</div></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    a,b,c=st.columns([1,1,1])
    with a:
        if st.button("Check sequence", key=f"check_seq_{team_key}", use_container_width=True):
            if team["case5_sequence"] == case["correct_sequence"]:
                team["answered_correctly"]=True; team["last_result"]="correct"; team["score"] += 10
            else:
                team["attempts_in_case"] += 1; team["case_hint_available"]=True; team["last_result"]="incorrect"; team["score"]=max(0, team["score"]-1)
            save_state(state); st.rerun()
    with b:
        if st.button("Reset sequence", key=f"reset_seq_{team_key}", use_container_width=True):
            team["case5_sequence"]=[]; team["case5_card_pool"]=shuffled_sequence_cards(); save_state(state); st.rerun()
    with c:
        st.markdown(f"""<div style="background:{colors['soft']};border:1px solid {colors['accent']};color:#334155;border-radius:16px;padding:14px;"><b>Clinical focus:</b> This station tests stepwise clinical reasoning, not just a single answer.</div>""", unsafe_allow_html=True)
    if team["case_hint_available"] and not team["answered_correctly"] and st.button("Use hint", key=f"hint_seq_{team_key}", use_container_width=True):
        team["show_case_hint"]=True; save_state(state); st.rerun()
    if team["show_case_hint"] and not team["answered_correctly"]:
        st.markdown(f"""<div style="background:#fff7ed;border:1px solid #fdba74;color:#7c2d12;border-radius:16px;padding:14px;margin-top:8px;"><b>{case['clue']}</b></div>""", unsafe_allow_html=True)
    if team["answered_correctly"]:
        st.markdown(f"""<div style="background:{colors['soft']};border:1px solid {colors['accent']};color:{colors['primary']};border-radius:16px;padding:14px;margin-top:10px;"><b>Claim from instructor:</b> {case['piece']}</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="background:#f0fdf4;border:1px solid #86efac;color:#166534;border-radius:16px;padding:14px;margin-top:10px;"><b>Why this is correct:</b> {case['explanation']}</div>""", unsafe_allow_html=True)
        if st.button("Go to next case", key=f"next_seq_{team_key}", use_container_width=True):
            finish_current_case(team); st.rerun()

def render_matching_case(case, team, team_key, colors):
    if team["last_result"]=="correct":
        play_tone("correct"); st.success("Correct matching activity. You may now claim a pyramid piece from the instructor.")
    elif team["last_result"]=="incorrect":
        play_tone("incorrect"); st.error("Incorrect matching. Review dose and frequency."); st.warning("Try again. The hint is available after the first incorrect attempt.")
    st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown("**Match each treatment with the correct dose and frequency**")
    for idx, treatment in enumerate(MATCHING_TREATMENTS):
        c1,c2,c3=st.columns([1.25,1.2,1.1])
        with c1: st.markdown(f"**{treatment}**")
        with c2:
            dose_options = team["case6_dose_order"]
            current_dose = team["case6_matches"].get(treatment, dose_options[0])
            dose = st.selectbox(f"Dose for {treatment}", dose_options, index=dose_options.index(current_dose) if current_dose in dose_options else 0, key=f"{team_key}_dose_{idx}", label_visibility="collapsed")
            team["case6_matches"][treatment]=dose
        with c3:
            freq_options = team["case6_freq_order"]
            current_freq = team["case6_freqs"].get(treatment, freq_options[0])
            freq = st.selectbox(f"Frequency for {treatment}", freq_options, index=freq_options.index(current_freq) if current_freq in freq_options else 0, key=f"{team_key}_freq_{idx}", label_visibility="collapsed")
            team["case6_freqs"][treatment]=freq
    st.markdown('</div>', unsafe_allow_html=True)
    a,b=st.columns([1,1])
    with a:
        if st.button("Check matching activity", key=f"check_match_{team_key}", use_container_width=True):
            ok = all(team["case6_matches"].get(t)==d and team["case6_freqs"].get(t)==f for t,(d,f) in MATCHING_CORRECT.items())
            if ok:
                team["answered_correctly"]=True; team["last_result"]="correct"; team["score"] += 10
            else:
                team["attempts_in_case"] += 1; team["case_hint_available"]=True; team["last_result"]="incorrect"; team["score"]=max(0, team["score"]-1)
            save_state(state); st.rerun()
    with b:
        st.markdown(f"""<div style="background:{colors['soft']};border:1px solid {colors['accent']};color:#334155;border-radius:16px;padding:14px;"><b>Clinical focus:</b> This station tests practical dosing and frequency knowledge for PBM therapies.</div>""", unsafe_allow_html=True)
    if team["case_hint_available"] and not team["answered_correctly"] and st.button("Use hint", key=f"hint_matching_{team_key}", use_container_width=True):
        team["show_case_hint"]=True; save_state(state); st.rerun()
    if team["show_case_hint"] and not team["answered_correctly"]:
        st.markdown(f"""<div style="background:#fff7ed;border:1px solid #fdba74;color:#7c2d12;border-radius:16px;padding:14px;margin-top:8px;"><b>{case['clue']}</b></div>""", unsafe_allow_html=True)
    if team["answered_correctly"]:
        st.markdown(f"""<div style="background:{colors['soft']};border:1px solid {colors['accent']};color:{colors['primary']};border-radius:16px;padding:14px;margin-top:10px;"><b>Claim from instructor:</b> {case['piece']}</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="background:#f0fdf4;border:1px solid #86efac;color:#166534;border-radius:16px;padding:14px;margin-top:10px;"><b>Why this is correct:</b> {case['explanation']}</div>""", unsafe_allow_html=True)
        if st.button("Go to next case", key=f"next_matching_{team_key}", use_container_width=True):
            finish_current_case(team); st.rerun()

def board_is_revealed(team, card_id): return card_id in team["case7_matched"] or card_id in team["case7_selected"]

def handle_board_click(team, card_id):
    if card_id in team["case7_matched"] or card_id in team["case7_selected"]: return
    if len(team["case7_selected"])==2: team["case7_selected"]=[]
    team["case7_selected"].append(card_id)
    if len(team["case7_selected"])==2:
        cards={c["id"]:c for c in team["case7_cards"]}
        c1,c2=cards[team["case7_selected"][0]], cards[team["case7_selected"][1]]
        if c1["pair"]==c2["pair"]:
            team["case7_matched"].extend(team["case7_selected"]); team["case7_selected"]=[]; team["case7_message"]="Correct relation uncovered."; team["last_result"]="correct"; team["case7_anim"]=f"{c1['label']} ↔ {c2['label']}"
            if len(team["case7_matched"])==len(team["case7_cards"]): team["answered_correctly"]=True; team["score"] += 10
        else:
            team["attempts_in_case"] += 1; team["case_hint_available"]=True; team["case7_message"]="Not a correct relation. Try again."; team["last_result"]="incorrect"; team["score"]=max(0, team["score"]-1); team["case7_selected"]=[]; team["case7_anim"]=""
    save_state(state)

def render_match_animation(team):
    if team["case7_anim"]:
        components.html(f"""
        <div style="margin:8px 0;padding:14px;border-radius:18px;background:linear-gradient(135deg,#dcfce7,#dbeafe);border:1px solid #93c5fd;text-align:center;animation:pulse .7s ease-in-out 1;">
          <div style="font-size:15px;color:#334155;font-weight:700;">MATCH DISCOVERED</div>
          <div style="font-size:28px;font-weight:900;color:#0f172a;margin-top:6px;">{team["case7_anim"]}</div>
        </div>
        <style>@keyframes pulse {{0% {{transform:scale(.96); opacity:.3;}}60% {{transform:scale(1.02); opacity:1;}}100% {{transform:scale(1); opacity:1;}}}}</style>
        """, height=100)

def render_board_case(case, team, team_key, colors):
    if team["last_result"]=="correct" and not team["answered_correctly"]:
        play_tone("correct"); st.success(team["case7_message"] or "Correct relation uncovered."); render_match_animation(team)
    elif team["last_result"]=="incorrect":
        play_tone("incorrect"); st.error(team["case7_message"] or "Incorrect relation."); st.warning("Try again. The hint is available after the first incorrect attempt.")
    elif team["answered_correctly"]:
        play_tone("winner"); st.success("Board completed. Every concept pair is now uncovered."); st.success("You may now claim a pyramid piece from the instructor.")
    st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown("**Hidden concept board**"); st.caption("Reveal related concepts. The case is won only when all pairs remain discovered.")
    cards=team["case7_cards"]; ncols=4
    for row_start in range(0,len(cards),ncols):
        cols=st.columns(ncols)
        for i,card in enumerate(cards[row_start:row_start+ncols]):
            label=card["label"] if board_is_revealed(team, card["id"]) else "?"
            with cols[i]:
                if st.button(label, key=f"{team_key}_card_{card['id']}", use_container_width=True):
                    handle_board_click(team, card["id"]); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    if team["case_hint_available"] and not team["answered_correctly"] and st.button("Use hint", key=f"hint_board_{team_key}", use_container_width=True):
        team["show_case_hint"]=True; save_state(state); st.rerun()
    if team["show_case_hint"] and not team["answered_correctly"]:
        st.markdown(f"""<div style="background:#fff7ed;border:1px solid #fdba74;color:#7c2d12;border-radius:16px;padding:14px;margin-top:8px;"><b>{case['clue']}</b></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="background:{colors['soft']};border:1px solid {colors['accent']};color:#334155;border-radius:16px;padding:14px;margin-top:10px;"><b>Clinical focus:</b> Integrate pathology, timing and treatment choice into one PBM reasoning map.</div>""", unsafe_allow_html=True)
    if team["answered_correctly"]:
        st.markdown(f"""<div style="background:{colors['soft']};border:1px solid {colors['accent']};color:{colors['primary']};border-radius:16px;padding:14px;margin-top:10px;"><b>Claim from instructor:</b> {case['piece']}</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="background:#f0fdf4;border:1px solid #86efac;color:#166534;border-radius:16px;padding:14px;margin-top:10px;"><b>Why this is correct:</b> {case['explanation']}</div>""", unsafe_allow_html=True)
        if st.button("Finish game", key=f"finish_board_{team_key}", use_container_width=True):
            finish_current_case(team); st.rerun()

def render_team_screen(team_key):
    team=state["teams"][team_key]; other_key="team_blue" if team_key=="team_red" else "team_red"; other_team=state["teams"][other_key]; colors=TEAM_COLORS[team_key]
    top1,top2,top3=st.columns([1.7,.8,.8])
    with top1:
        st.markdown(f"""<div class="glass-card" style="border-top:6px solid {colors['primary']}; box-shadow: 0 16px 34px {colors['glow']};"><div style="font-size:34px;font-weight:900;color:{colors['primary']};">{team['name']}</div><div style="font-size:16px;color:#475569;margin-top:4px;">Preoperative Anemia Treatment Pyramid</div><div style="margin-top:10px;"><span class="metric-pill-neutral">Score: {team['score']}</span><span class="metric-pill-neutral">Cases solved: {team['correct_cases']}/{len(CASES)}</span><span class="metric-pill-neutral">Pieces: {team['pieces_claimed']}</span></div></div>""", unsafe_allow_html=True)
    with top2: render_clock(remaining_seconds(state), state.get("timer_running", False))
    with top3:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">Competition status</div>', unsafe_allow_html=True)
        st.write(f"Opponent: **{other_team['name']}**"); st.write(f"Leader: **{winner_name(state)}**")
        if st.button("Refresh status", use_container_width=True): st.rerun()
        if st.button("Logout", use_container_width=True): st.session_state.pop("logged_role",None); st.session_state.pop("logged_team",None); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("Game Instructions", expanded=False):
        st.markdown("- Cases 1–4 are clinical multiple-choice stations.  \n- Case 5 is a management sequence challenge with randomized drag-style cards.  \n- Case 6 is a treatment-dose-frequency matching challenge with randomized options.  \n- Case 7 is a hidden concept board that is won only when the full board is discovered.  \n- After the first wrong answer, **Use hint** becomes available.  \n- Wrong answers subtract 1 point. Correct cases add 10 points.")
    if team["finished"]:
        render_winner_announcement(); st.success(f"{team['name']} completed all cases."); return
    case=CASES[team["current_case"]]; st.progress(team["current_case"]/len(CASES)); render_case_header(case, colors)
    if case["type"]=="mcq": render_mcq_case(case, team, team_key, colors)
    elif case["type"]=="sequence": render_sequence_case(case, team, team_key, colors)
    elif case["type"]=="matching": render_matching_case(case, team, team_key, colors)
    else: render_board_case(case, team, team_key, colors)

def render_facilitator():
    red,blue=state["teams"]["team_red"],state["teams"]["team_blue"]
    top_left,top_mid=st.columns([1.5,.8])
    with top_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">Facilitator control room</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="metric-pill-red">{red["name"]}: {red["score"]} pts</span><span class="metric-pill-blue">{blue["name"]}: {blue["score"]} pts</span><span class="metric-pill-neutral">Leader: {winner_name(state)}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with top_mid: render_clock(remaining_seconds(state), state.get("timer_running", False))
    m1,m2,m3,m4=st.columns(4)
    m1.metric(red["name"], red["score"], f"{red['correct_cases']} cases"); m2.metric(blue["name"], blue["score"], f"{blue['correct_cases']} cases"); m3.metric("Pieces", f"{red['pieces_claimed']} - {blue['pieces_claimed']}"); m4.metric("Winner so far", winner_name(state))
    left,right=st.columns([1,1])
    with left:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">Competition setup</div>', unsafe_allow_html=True)
        state["teams"]["team_red"]["name"]=st.text_input("Red team name", value=red["name"]); state["teams"]["team_blue"]["name"]=st.text_input("Blue team name", value=blue["name"]); previous_minutes = int(state["timer_minutes"]); state["timer_minutes"]=st.number_input("Timer (minutes)", min_value=1, max_value=60, value=previous_minutes, step=1)
        if int(state["timer_minutes"]) != previous_minutes and not state["timer_running"]:
            state["paused_remaining_seconds"] = int(state["timer_minutes"] * 60)
        if st.button("Save names and timer", key="save_names_timer", use_container_width=True): save_state(state); st.success("Setup saved.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">Access codes</div>', unsafe_allow_html=True)
        state["team_codes"]["team_red"]=st.text_input("Red team code", value=state["team_codes"]["team_red"]); state["team_codes"]["team_blue"]=st.text_input("Blue team code", value=state["team_codes"]["team_blue"]); state["facilitator_code"]=st.text_input("Facilitator code", value=state["facilitator_code"])
        if st.button("Save access codes", key="save_access_codes", use_container_width=True): save_state(state); st.success("Codes saved.")
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">Timer and control</div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            if st.button("Start / restart timer", key="facilitator_start_restart_timer", use_container_width=True):
                state["paused_remaining_seconds"] = int(state["timer_minutes"]*60)
                state["competition_end_ts"]=time.time()+state["paused_remaining_seconds"]
                state["timer_running"]=True
                save_state(state)
                st.rerun()
        with c2:
            if st.button("Stop timer", key="facilitator_stop_timer", use_container_width=True):
                state["paused_remaining_seconds"] = remaining_seconds(state)
                state["competition_end_ts"] = None
                state["timer_running"]=False
                save_state(state)
                st.rerun()
        if st.button("Reset whole competition", key="facilitator_reset_competition", use_container_width=True): restart_competition(state); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">Leaderboard</div>', unsafe_allow_html=True); render_leaderboard_table(); st.markdown('</div>', unsafe_allow_html=True)
    if red["finished"] or blue["finished"]: render_winner_announcement()
    if st.button("Logout facilitator"): st.session_state.pop("logged_role",None); st.rerun()

def render_projection():
    red,blue=state["teams"]["team_red"],state["teams"]["team_blue"]; wk=winner_key(state)
    st.markdown("""<div class="glass-card" style="text-align:center;"><div style="font-size:42px;font-weight:900;">AUDITORIUM MODE</div><div style="font-size:18px;color:#475569;margin-top:8px;">Preoperative Anemia Treatment Pyramid</div></div>""", unsafe_allow_html=True)
    action_left, action_right = st.columns(2)
    with action_left:
        if st.button("Refresh status", key="projection_refresh", use_container_width=True):
            st.rerun()
    with action_right:
        if st.button("Logout", key="projection_logout", use_container_width=True):
            st.session_state.pop("logged_role",None)
            st.session_state.pop("logged_team",None)
            st.rerun()
    t1,t2=st.columns([1.2,.8])
    with t1: render_winner_announcement()
    with t2: render_clock(remaining_seconds(state), state.get("timer_running", False))
    cols=st.columns(2)
    for idx,team_key in enumerate(["team_red","team_blue"]):
        team=state["teams"][team_key]; colors=TEAM_COLORS[team_key]; badge="🏆 LEADING" if wk==team_key else "COMPETING"
        with cols[idx]:
            st.markdown(f"""<div style="background:white;border-radius:26px;padding:24px;border-top:8px solid {colors['primary']};box-shadow:0 20px 40px {colors['glow']};"><div style="font-size:34px;font-weight:900;color:{colors['primary']};">{team['name']}</div><div style="margin-top:8px;font-size:18px;color:#475569;">{badge}</div><div style="margin-top:18px;font-size:64px;font-weight:900;color:#0f172a;">{team['score']}</div><div style="margin-top:10px;font-size:19px;color:#334155;">Cases solved: <b>{team['correct_cases']}/{len(CASES)}</b></div><div style="margin-top:8px;font-size:19px;color:#334155;">Pieces claimed: <b>{team['pieces_claimed']}</b></div><div style="margin-top:8px;font-size:19px;color:#334155;">Status: <b>{"Finished" if team['finished'] else "In progress"}</b></div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">Professional leaderboard</div>', unsafe_allow_html=True); render_leaderboard_table(); st.markdown('</div>', unsafe_allow_html=True)

role=st.session_state.get("logged_role")
if role is None:
    col1,col2=st.columns([1.15,.85])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">Access portal</div>', unsafe_allow_html=True)
        st.write("Choose your role. Each team sees only its own competition screen after login.")
        role_choice=st.radio("Role", ["Team","Facilitator","Auditorium Projection"], horizontal=True)
        if role_choice=="Team":
            team_label=st.selectbox("Team", ["Team Red","Team Blue"]); team_key="team_red" if team_label=="Team Red" else "team_blue"; code=st.text_input("Team access code", type="password")
            if st.button("Login as team", use_container_width=True):
                if code==state["team_codes"][team_key]: st.session_state["logged_role"]="team"; st.session_state["logged_team"]=team_key; st.rerun()
                else: st.error("Incorrect team access code.")
        elif role_choice=="Facilitator":
            code=st.text_input("Facilitator access code", type="password")
            if st.button("Login as facilitator", use_container_width=True):
                if code==state["facilitator_code"]: st.session_state["logged_role"]="facilitator"; st.rerun()
                else: st.error("Incorrect facilitator code.")
        else:
            st.caption("Projection mode is view-only and ideal for the auditorium screen.")
            if st.button("Open auditorium projection", use_container_width=True): st.session_state["logged_role"]="projection"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">Game Instructions</div>', unsafe_allow_html=True)
        st.markdown("- Each team logs in separately and sees only its own panel.  \n- Case 5 is a management sequence challenge with randomized drag-style cards.  \n- Case 6 is a matching challenge with randomized options.  \n- Case 7 is a hidden concept board; it is won only when the full board is uncovered.  \n- After a correct answer, teams must claim the pyramid piece from the instructor.")
        st.markdown('</div>', unsafe_allow_html=True)
elif role=="facilitator":
    render_facilitator()
elif role=="projection":
    render_projection()
else:
    render_team_screen(st.session_state.get("logged_team","team_red"))
