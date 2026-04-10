import json, os, time, random
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PBM Pyramid – WCA 2026", page_icon="🩸", layout="wide")

APP_DIR = Path(__file__).resolve().parent
STATE_FILE = APP_DIR / "pbm_competition_shared_state.json"

# ─── VIDEO PATHS ───────────────────────────────────────────────────────────────
VIDEOS_DIR   = APP_DIR / "videos"
VIDEO_INICIO = VIDEOS_DIR / "video_inicio.mp4"
VIDEO_FINAL  = VIDEOS_DIR / "video_final.mp4"
VIDEOS_JUEGOS = [
    VIDEOS_DIR / "video_juego_1.mp4",
    VIDEOS_DIR / "video_juego_2.mp4",
    VIDEOS_DIR / "video_juego_3.mp4",
]

# ─── DATA ──────────────────────────────────────────────────────────────────────
CASES = [
    {"case":1,"title":"Challenge 1","type":"mcq","icon":"🩺","scenario":"A 60-year-old patient is scheduled for a right total knee replacement in 6 weeks.\n\nPre-operative blood tests reveal:\n• Haemoglobin: 11.5 g/dL\n• Ferritin: 8 ng/mL\n• Transferrin saturation (TSAT): 10%\n\nTime is running… Your mission is to select the most appropriate strategy to optimise this patient before surgery.","question":"What is the most appropriate strategy to optimise this patient before surgery?","options":{"A":"Using oral iron would be a reasonable approach","B":"I would not waste time — blood transfusion is a quick solution","C":"I am not concerned — proceeding with a haemoglobin of 11.5 g/dL is acceptable","D":"Erythropoietin could be a convenient option, as we still have time"},"correct":"A","feedback":{"A":"Correct. Ferritin of 8 ng/mL and TSAT of 10% confirm absolute iron deficiency. With 6 weeks before surgery, oral iron is a reasonable and effective first-line approach to replenish iron stores and improve haemoglobin.","B":"Incorrect. Transfusion carries risks including immunomodulation and infection. It should be reserved for patients with symptomatic or severe anaemia and is not first-line in an elective setting with time to optimise.","C":"Incorrect. Although Hb 11.5 g/dL may appear borderline, the severely depleted iron stores (ferritin 8 ng/mL) indicate true iron deficiency anaemia that will worsen with surgical blood loss. This is a treatable condition.","D":"Incorrect. Erythropoietin requires adequate iron stores to be effective. With a ferritin of 8 ng/mL, ESA therapy would be futile without first correcting the underlying iron deficiency."},"clue":"A clue awaits beneath one of the chairs… be quick — your patient is counting on you.","piece":"Pyramid piece: Oral Iron layer.","explanation":"This patient has absolute iron deficiency anaemia (ferritin 8 ng/mL, TSAT 10%) with sufficient time before elective surgery (6 weeks). Oral iron is the appropriate first-line strategy because iron stores are clearly depleted and there is an adequate window for oral supplementation to take effect. The key principle: identify the deficiency, match the treatment to the available time."},
    {"case":2,"title":"Challenge 2","type":"mcq","icon":"💉","scenario":"A 72-year-old patient is scheduled for a hip replacement in 10 days.\n\nPre-operative blood tests reveal:\n• Haemoglobin: 9 g/dL\n• Ferritin: 15 ng/mL\n• Transferrin saturation (TSAT): 12%\n\nShe is increasingly concerned about the risk of bleeding.\n\nTime is limited… Your mission is to rapidly optimise her condition and reduce perioperative risk.","question":"What is the most appropriate strategy to rapidly optimise this patient?","options":{"A":"Vitamin supplementation combined with oral iron should resolve the problem","B":"One or two sessions of intravenous ferric carboxymaltose may be sufficient","C":"We can proceed to surgery — if bleeding occurs, we can manage it with transfusion","D":"The issue can be resolved by supplementing the appropriate vitamins, such as folate (vitamin B9)"},"correct":"B","feedback":{"A":"Incorrect. Oral iron requires 4–8 weeks to meaningfully raise haemoglobin. With only 10 days before surgery, oral supplementation is too slow to make a clinical difference.","B":"Correct. With ferritin 15 ng/mL and TSAT 12%, this patient has clear iron deficiency anaemia. Intravenous ferric carboxymaltose can rapidly replenish iron stores in 1–2 sessions, making it the ideal choice when the preoperative window is short.","C":"Incorrect. Proceeding without optimisation exposes the patient to avoidable transfusion risk. Reactive transfusion management is inferior to proactive preoperative optimisation — a core principle of Patient Blood Management.","D":"Incorrect. The laboratory profile points to iron deficiency, not folate deficiency. Folate supplementation alone would not address the underlying cause of this patient's anaemia."},"clue":"Hint: When time is short, think about the fastest route to replenish iron stores.","piece":"Pyramid piece: Intravenous Iron layer.","explanation":"This patient has iron deficiency anaemia (ferritin 15 ng/mL, TSAT 12%) with only 10 days before surgery. Oral iron is far too slow. Intravenous ferric carboxymaltose can deliver 1000 mg of iron in a single session, rapidly restoring iron availability. The key principle: match the urgency of the clinical timeline to the speed of the intervention."},
    {"case":3,"title":"Challenge 3","type":"mcq","icon":"💊","scenario":"A 55-year-old patient is scheduled for a right colectomy in 7 weeks.\n\nPre-operative blood tests reveal:\n• Haemoglobin: 10.5 g/dL\n• Mean corpuscular volume (MCV): 108 fL\n• Vitamin B12: 120 pg/mL (low)\n• Folate: 8 ng/mL (within normal range)\n\nHe reports following a vegetarian diet and states that he regularly takes vitamin supplements.\n\nSomething does not add up…","question":"What is the most appropriate treatment strategy?","options":{"A":"Low vitamin B12 levels are common and can be adequately corrected with oral supplementation","B":"There is nothing that cannot be managed with erythropoietin therapy","C":"In the hands of an experienced surgeon, this procedure is unlikely to result in significant bleeding","D":"Initiating oral iron, particularly in combination with folate, would be a suitable approach"},"correct":"A","feedback":{"A":"Correct. The macrocytic anaemia (MCV 108 fL) with low vitamin B12 and normal folate clearly points to B12 deficiency — consistent with a vegetarian diet. Oral B12 supplementation (or intramuscular if absorption is impaired) is the targeted and appropriate correction.","B":"Incorrect. Erythropoietin stimulates red cell production but requires adequate substrate — including B12 — to be effective. Without correcting the underlying B12 deficiency, ESA therapy would be ineffective and inappropriate.","C":"Incorrect. A haemoglobin of 10.5 g/dL with macrocytic anaemia before a colectomy (a procedure with potential for significant blood loss) must not be dismissed. Preoperative optimisation is essential.","D":"Incorrect. The key abnormality is low vitamin B12, not iron deficiency. Ferritin and TSAT are not mentioned as abnormal. Starting iron and folate would miss the true diagnosis entirely."},"clue":"Hint: Look carefully at the MCV and the dietary history — the diagnosis is hiding in plain sight.","piece":"Pyramid piece: Vitamin B12 layer.","explanation":"This patient has macrocytic anaemia (MCV 108 fL) caused by vitamin B12 deficiency, consistent with a vegetarian diet. Despite taking general supplements, his B12 remains low — suggesting inadequate dosing or a formulation that does not contain B12. The correct approach is targeted B12 replacement. The key principle: always identify the specific deficiency before treating."},
    {"case":4,"title":"Challenge 4","type":"mcq","icon":"⚡","scenario":"We are planning a myocardial revascularisation in three weeks. The patient is 68 years old with chronic kidney disease.\n\nPre-operative blood tests show:\n• Haemoglobin: 10.2 g/dL\n• Mean corpuscular volume (MCV): 72 fL\n• Mean corpuscular haemoglobin (MCH): 22 pg\n• Ferritin: 40 ng/mL\n• Transferrin saturation (TSAT): 15%\n• C-reactive protein (CRP): 18 mg/L\n\nAvoiding transfusion may reduce postoperative risks.","question":"What would be the most appropriate strategy to optimise haemoglobin prior to surgery?","options":{"A":"More than one strategy should be used in this case; a combination of intravenous iron and erythropoietin appears promising","B":"Oral iron alone is sufficient in this case","C":"This is cardiovascular surgery; transfusion will be necessary","D":"Folic acid is required to provide substrate for the bone marrow"},"correct":"A","feedback":{"A":"Correct. This patient has a microcytic anaemia with functional iron deficiency (low TSAT despite borderline ferritin) in the context of chronic kidney disease and inflammation (CRP 18 mg/L). Oral iron will be poorly absorbed. IV iron addresses the functional deficiency, whilst ESA compensates for the blunted erythropoietin response typical of CKD. A combined approach is the most effective strategy.","B":"Incorrect. The elevated CRP indicates an inflammatory state that impairs oral iron absorption via hepcidin upregulation. Additionally, in CKD, the erythropoietin response is blunted — iron alone will not suffice.","C":"Incorrect. Accepting transfusion as inevitable contradicts the principles of Patient Blood Management. With 3 weeks available, there is a meaningful opportunity to optimise this patient and reduce transfusion risk.","D":"Incorrect. Folic acid addresses folate deficiency, which is not the primary abnormality here. The microcytic indices (MCV 72 fL, MCH 22 pg) and low TSAT point clearly to iron-restricted erythropoiesis, not folate deficiency."},"clue":"Hint: Consider what chronic kidney disease does to erythropoietin production, and what inflammation does to iron absorption.","piece":"Pyramid piece: Combined optimisation — IV iron + ESA layer.","explanation":"This is a complex case combining iron-restricted erythropoiesis (functional iron deficiency with TSAT 15%, ferritin 40 ng/mL in an inflammatory state) and chronic kidney disease (blunted EPO response). The microcytic indices confirm iron-restricted red cell production. A combined strategy of IV iron (bypassing hepcidin-mediated absorption block) and ESA (compensating for reduced endogenous erythropoietin) is the most appropriate approach. The key principle: in complex anaemia, a multimodal strategy may be necessary."},
    {"case":5,"title":"Challenge 5","type":"sequence","icon":"🔢","scenario":"A 63-year-old woman is scheduled for elective hip surgery in 2 weeks. However, she reports increasing fatigue over the past months.\n\nHer blood tests show:\n• Haemoglobin: 9.5 g/dL\n• Ferritin: 120 ng/mL\n• Transferrin saturation (TSAT): 15%\n• C-reactive protein (CRP): 32.","question":"Choose the correct management sequence.","cards":["Iron assessment","Calculate iron deficit","IV iron","Re-evaluate Hb","Oral iron","EPO"],"correct_sequence":["Iron assessment","Calculate iron deficit","IV iron","Re-evaluate Hb"],"clue":"Hint: First confirm iron status, then estimate replacement need, then choose the fastest treatment, then reassess response.","piece":"Pyramid piece: Clinical sequencing mastery piece.","explanation":"In functional iron deficiency with limited time before surgery, the logical sequence is to assess iron status, estimate the iron deficit, use IV iron for rapid optimisation, and then re-evaluate haemoglobin response."},
    {"case":6,"title":"Challenge 6","type":"matching","icon":"🔗","scenario":"Matching challenge: link each treatment with its usual dose and frequency of administration.","question":"Match oral iron, intravenous iron, erythropoietin, vitamins B6, B9 and B12 with the correct dose and frequency.","clue":"Hint: Oral therapies are usually daily; IV iron is delivered in sessions; ESA is usually weekly.","piece":"Pyramid piece: Dosing and frequency mastery piece.","explanation":"Correct treatment matching strengthens practical PBM decisions: oral iron needs time and daily dosing, IV iron is rapid, ESA is typically weekly, folate and B6 are daily, and B12 replacement is often weekly in deficiency correction."},
    {"case":7,"title":"Challenge 7","type":"board","icon":"🧩","scenario":"Concept discovery board: uncover and match related concepts until the whole board is solved.","question":"Reveal two related concepts at a time. The challenge is won only when the full board is discovered.","clue":"Hint: Match deficiency states, timeline concepts and therapeutic choices that belong together.","piece":"Pyramid piece: Integration and concept board mastery piece.","explanation":"The final board integrates diagnosis and treatment logic: anaemia mechanism, timing and the most appropriate PBM tool must align to build the full treatment pyramid."},
]

TEAM_COLORS = {
    "team_red":{"primary":"#dc2626","secondary":"#b91c1c","soft":"rgba(239,68,68,.08)","accent":"#dc2626","glow":"rgba(239,68,68,.18)","gradient":"linear-gradient(135deg,#dc2626,#b91c1c,#991b1b)","neon":"#ff4444"},
    "team_blue":{"primary":"#2563eb","secondary":"#1d4ed8","soft":"rgba(59,130,246,.08)","accent":"#2563eb","glow":"rgba(59,130,246,.18)","gradient":"linear-gradient(135deg,#2563eb,#1d4ed8,#1e40af)","neon":"#4488ff"},
}

MATCHING_TREATMENTS = ["Oral Iron","Intravenous Iron","Erythropoietin (ESA)","Vitamin B6","Vitamin B9 (Folic Acid)","Vitamin B12"]
MATCHING_DOSES = ["100–200 mg oral elemental iron","1000 mg IV carboxymaltose","300–600 IU/kg subcutaneous","25–50 mg oral","1–5 mg oral","1000 mcg IM"]
MATCHING_FREQS = ["Daily for 4–8 weeks","Sessions","Weekly / 3–4 preoperative doses","Daily","Daily","Weekly"]
MATCHING_CORRECT = {
    "Oral Iron":("100–200 mg oral elemental iron","Daily for 4–8 weeks"),
    "Intravenous Iron":("1000 mg IV carboxymaltose","Sessions"),
    "Erythropoietin (ESA)":("300–600 IU/kg subcutaneous","Weekly / 3–4 preoperative doses"),
    "Vitamin B6":("25–50 mg oral","Daily"),
    "Vitamin B9 (Folic Acid)":("1–5 mg oral","Daily"),
    "Vitamin B12":("1000 mcg IM","Weekly"),
}
BOARD_PAIRS = [
    ("Iron","Iron deficiency anaemia"),
    ("Intravenous iron","Functional iron deficiency"),
    ("Vitamin B12","Low vitamin B12"),
    ("Vitamin B9","Low folate"),
    ("ESA","Adequate iron availability"),
    ("Short time before surgery","Rapid optimisation"),
]

CASE_TYPE_LABELS = {"mcq":"","sequence":"SEQUENCE BUILDER","matching":"MATCHING CHALLENGE","board":"DISCOVERY BOARD"}
CASE_TYPE_COLORS = {"mcq":"#6366f1","sequence":"#f59e0b","matching":"#10b981","board":"#ec4899"}

# ─── STATE HELPERS ─────────────────────────────────────────────────────────────
def default_board_cards():
    cards=[]
    for i,(a,b) in enumerate(BOARD_PAIRS):
        cards.append({"id":f"{i}_a","pair":i,"label":a})
        cards.append({"id":f"{i}_b","pair":i,"label":b})
    random.shuffle(cards)
    return cards

def shuffled_matching_lists():
    doses = MATCHING_DOSES[:]; freqs = MATCHING_FREQS[:]
    random.shuffle(doses); random.shuffle(freqs)
    return doses, freqs

def shuffled_sequence_cards():
    cards = CASES[4]["cards"][:]; random.shuffle(cards); return cards

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

def nl2br(text):
    """Convert newlines to <br> for safe HTML embedding."""
    return text.replace("\n", "<br>")

# ─── AUDIO ─────────────────────────────────────────────────────────────────────
def sound_html(kind="correct"):
    if kind=="correct":
        notes=[523,659,784,1047]; osc="triangle"; border="#22c55e"; bg="rgba(34,197,94,.08)"; icon="✅"; label="CORRECT"; height=54
    elif kind=="incorrect":
        notes=[294,220]; osc="sawtooth"; border="#ef4444"; bg="rgba(239,68,68,.08)"; icon="❌"; label="INCORRECT"; height=54
    else:
        notes=[523,659,784,988,1047,1318,1568]; osc="sine"; border="#eab308"; bg="rgba(234,179,8,.08)"; icon="🏆"; label="CHAMPION"; height=64
    notes_js=",".join(str(n) for n in notes)
    dur = "0.15" if kind!="winner" else "0.22"
    gap = "0.10" if kind!="winner" else "0.13"
    html=f"""
    <div style='padding:10px 14px;border-radius:16px;border:2px solid {border};background:{bg};
    backdrop-filter:blur(12px);font-weight:800;text-align:center;font-size:15px;letter-spacing:2px;
    box-shadow:0 0 20px {border}44;'>{icon} {label}</div>
    <script>
    try {{
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      [{notes_js}].forEach((freq, idx) => {{
        const t = ctx.currentTime + idx * {gap};
        const o = ctx.createOscillator(), g = ctx.createGain();
        o.type="{osc}"; o.frequency.value=freq; o.connect(g); g.connect(ctx.destination);
        g.gain.setValueAtTime(.0001,t); g.gain.exponentialRampToValueAtTime(.13,t+.02);
        g.gain.exponentialRampToValueAtTime(.0001,t+{dur}); o.start(t); o.stop(t+{dur});
      }});
    }} catch(e){{}}
    </script>"""
    return html,height

def play_tone(kind="correct"):
    html,height=sound_html(kind); components.html(html, height=height)

# ─── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@700&display=swap');

:root {
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #64748b;
  --accent-red: #dc2626;
  --accent-blue: #2563eb;
  --accent-gold: #d97706;
  --accent-green: #16a34a;
  --accent-purple: #7c3aed;
}

.main {
  background: linear-gradient(160deg, #f8fafc 0%, #eef2ff 30%, #faf5ff 60%, #fff1f2 80%, #f8fafc 100%) !important;
}
.block-container {max-width:1280px; padding-top:.6rem; padding-bottom:2rem;}
header[data-testid="stHeader"] {background:transparent !important;}

/* ── Glass card ── */
.glass-card {
  background: rgba(255,255,255,.85);
  backdrop-filter: blur(20px) saturate(1.3);
  -webkit-backdrop-filter: blur(20px) saturate(1.3);
  border: 1px solid rgba(148,163,184,.18);
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(15,23,42,.08), 0 0 0 1px rgba(255,255,255,.6) inset;
  padding: 1.3rem 1.4rem;
  color: var(--text-primary);
  position: relative;
  overflow: hidden;
}
.glass-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.9), transparent);
}

/* ── Minor card ── */
.minor-card {
  background: rgba(255,255,255,.80);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148,163,184,.15);
  border-radius: 20px;
  box-shadow: 0 12px 32px rgba(15,23,42,.07);
  padding: 1.1rem 1.2rem;
  color: var(--text-primary);
  transition: transform .25s ease, box-shadow .25s ease;
}
.minor-card:hover { transform: translateY(-2px); box-shadow: 0 16px 40px rgba(15,23,42,.12); }

/* ── Metric pills ── */
.metric-pill-red, .metric-pill-blue, .metric-pill-neutral {
  display:inline-block; padding:.42rem .85rem; border-radius:999px; font-weight:700;
  margin-right:.4rem; margin-bottom:.4rem; font-size:.85rem; letter-spacing:.3px;
}
.metric-pill-red { background:#fef2f2; color:#dc2626; border:1px solid #fecaca; }
.metric-pill-blue { background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe; }
.metric-pill-neutral { background:#f1f5f9; color:#334155; border:1px solid #e2e8f0; }

/* ── Section title ── */
.section-title {font-size:1.25rem; font-weight:800; margin-bottom:.4rem; color:#0f172a; letter-spacing:.5px; }

/* ── Case type badge ── */
.case-badge {
  display:inline-block; padding:4px 14px; border-radius:999px; font-size:11px;
  font-weight:800; letter-spacing:2px; text-transform:uppercase;
}

/* ── Sequence slots ── */
.sequence-slot {
  background: #f8fafc;
  border: 2px dashed #cbd5e1;
  border-radius: 18px; padding: 16px; min-height: 84px;
  transition: border-color .3s, background .3s;
}
.sequence-slot-filled {
  background: #eef2ff;
  border: 2px solid #818cf8;
  border-radius: 18px; padding: 16px; min-height: 84px;
}

/* ── Card pick ── */
.card-pick {
  background: linear-gradient(145deg, #ffffff, #f1f5f9);
  border: 2px solid #c7d2fe;
  border-radius: 22px;
  box-shadow: 0 8px 24px rgba(99,102,241,.10), 0 2px 6px rgba(15,23,42,.04);
  padding: 28px 14px 22px;
  min-height: 160px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.card-pick::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 5px;
  background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
  border-radius: 22px 22px 0 0;
}
.card-pick:hover {
  transform: translateY(-5px);
  box-shadow: 0 16px 40px rgba(99,102,241,.20), 0 6px 16px rgba(15,23,42,.08);
  border-color: #818cf8;
}
.card-pick-label {
  font-size: 15px; font-weight: 800; color: #312e81;
  letter-spacing: .5px; margin-bottom: 8px; margin-top: 8px;
}
.card-pick-icon {
  font-size: 40px; line-height: 1;
}
.card-pick-hint {
  font-size: 10px; color: #94a3b8; font-weight: 600;
  letter-spacing: 1.5px; text-transform: uppercase; margin-top: 6px;
}

/* ── Streamlit overrides ── */
div.stButton > button {
  border-radius: 16px !important;
  border: 1px solid #e2e8f0 !important;
  background: linear-gradient(135deg, #ffffff, #f8fafc) !important;
  color: #1e293b !important;
  padding: .85rem 1.1rem !important;
  font-weight: 700 !important;
  min-height: 3.2rem !important;
  transition: all .25s ease !important;
  box-shadow: 0 4px 16px rgba(15,23,42,.06) !important;
}
div.stButton > button:hover {
  background: linear-gradient(135deg, #eef2ff, #ede9fe) !important;
  border-color: #a5b4fc !important;
  box-shadow: 0 8px 28px rgba(99,102,241,.15), 0 0 0 2px rgba(99,102,241,.08) !important;
  transform: translateY(-1px) !important;
}
div.stButton > button:active {
  transform: translateY(1px) !important;
  box-shadow: 0 2px 8px rgba(15,23,42,.08) !important;
}

[data-testid="stMetricValue"] { font-size:2rem; color:#0f172a !important; }
[data-testid="stMetricLabel"] { color:#475569 !important; }
[data-testid="stMetricDelta"] { color:#2563eb !important; }

.stProgress > div > div > div { background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899) !important; border-radius:99px !important; }
.stProgress > div > div { background: #e2e8f0 !important; border-radius:99px !important; }

[data-testid="stExpander"] {
  background: rgba(255,255,255,.7) !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 16px !important;
}
[data-testid="stExpander"] summary span { color: #0f172a !important; font-weight:700 !important; }
[data-testid="stExpander"] div { color: #334155 !important; }

.stSelectbox > div > div { background: #ffffff !important; color:#1e293b !important; border:1px solid #e2e8f0 !important; border-radius:12px !important; }
input[type="text"], input[type="password"], input[type="number"] { background: #ffffff !important; color:#1e293b !important; border:1px solid #e2e8f0 !important; border-radius:12px !important; }
.stRadio label, .stSelectbox label, .stTextInput label, .stNumberInput label { color: #475569 !important; }

[data-testid="stDataFrame"] { border-radius:16px; overflow:hidden; }

.stAlert { border-radius:16px !important; }

/* ── Animated glow keyframes ── */
@keyframes breathe { 0%,100%{opacity:.7;transform:scale(1)} 50%{opacity:1;transform:scale(1.03)} }
@keyframes shimmer { 0%{background-position:200% center} 100%{background-position:-200% center} }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
@keyframes pulse-glow { 0%,100%{box-shadow:0 0 20px rgba(99,102,241,.15)} 50%{box-shadow:0 0 40px rgba(99,102,241,.30)} }
@keyframes gradient-shift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
@keyframes fade-in { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }

/* ── Hint box ── */
.hint-box {
  background: #fffbeb;
  border: 1px solid #f59e0b;
  color: #92400e;
  border-radius: 16px; padding: 16px; margin-top: 10px;
  animation: fade-in .4s ease;
}

/* ── Feedback boxes ── */
.feedback-correct {
  background: #f0fdf4; border:1px solid #86efac;
  color:#166534; border-radius:16px; padding:16px; margin-top:10px;
  animation: fade-in .4s ease;
}
.feedback-explain {
  background: #eef2ff; border:1px solid #a5b4fc;
  color:#3730a3; border-radius:16px; padding:16px; margin-top:10px;
  animation: fade-in .4s ease;
}
.feedback-piece {
  background: #fffbeb; border:1px solid #fbbf24;
  color:#92400e; border-radius:16px; padding:16px; margin-top:10px;
  animation: fade-in .4s ease;
}
</style>
""", unsafe_allow_html=True)

# ─── ANIMATED HEADER ───────────────────────────────────────────────────────────
components.html("""
<div id="header-wrap" style="position:relative;border-radius:28px;overflow:hidden;margin-bottom:4px;">
<canvas id="hdr-canvas" style="position:absolute;inset:0;z-index:0;"></canvas>
<svg width="100%" height="290" viewBox="0 0 1440 290" xmlns="http://www.w3.org/2000/svg" style="position:relative;z-index:1;">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7f1d1d"/><stop offset="30%" stop-color="#991b1b"/>
      <stop offset="50%" stop-color="#312e81"/><stop offset="70%" stop-color="#1e3a8a"/>
      <stop offset="100%" stop-color="#0c4a6e"/>
    </linearGradient>
    <linearGradient id="pyr" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="rgba(255,255,255,.95)"/><stop offset="100%" stop-color="rgba(203,213,225,.75)"/>
    </linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="softglow"><feGaussianBlur stdDeviation="6" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect x="0" y="0" width="1440" height="290" rx="28" fill="url(#bg)"/>

  <!-- Subtle grid -->
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,.03)" stroke-width=".5"/>
  </pattern>
  <rect width="1440" height="290" fill="url(#grid)"/>

  <!-- Animated blood drop -->
  <g transform="translate(72,44)" filter="url(#glow)">
    <animateTransform attributeName="transform" type="translate" values="72,44;72,38;72,44" dur="3s" repeatCount="indefinite"/>
    <path d="M28 96 C28 68, 56 54, 56 28 C56 54, 84 68, 84 96 C84 116, 70 130, 56 130 C42 130, 28 116, 28 96Z" fill="#dc2626" opacity=".9"/>
    <path d="M40 96 C40 78, 56 68, 56 48 C56 68, 72 78, 72 96 C72 108, 65 116, 56 116 C47 116, 40 108, 40 96Z" fill="#ef4444" opacity=".5"/>
    <circle cx="48" cy="86" r="4" fill="rgba(255,255,255,.35)"/>
  </g>

  <!-- Title -->
  <text x="164" y="80" fill="rgba(255,255,255,.95)" font-size="42" font-weight="900" font-family="Inter,sans-serif" filter="url(#softglow)">Preoperative Anaemia</text>
  <text x="164" y="120" fill="rgba(255,255,255,.95)" font-size="42" font-weight="900" font-family="Inter,sans-serif" filter="url(#softglow)">Treatment Pyramid</text>

  <!-- Subtitle badges -->
  <rect x="164" y="138" width="400" height="30" rx="15" fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.12)" stroke-width="1"/>
  <text x="174" y="158" fill="rgba(255,255,255,.7)" font-size="11" font-weight="700" font-family="Inter,sans-serif" letter-spacing="1.5">WORLD CONGRESS OF ANAESTHESIOLOGISTS 2026</text>

  <rect x="578" y="138" width="210" height="30" rx="15" fill="rgba(234,179,8,.12)" stroke="rgba(234,179,8,.25)" stroke-width="1"/>
  <text x="588" y="158" fill="#fbbf24" font-size="11" font-weight="700" font-family="Inter,sans-serif" letter-spacing="1.5">PBM COMPETITION MODE</text>

  <!-- Separator line -->
  <line x1="164" y1="182" x2="700" y2="182" stroke="rgba(255,255,255,.08)" stroke-width="1"/>

  <!-- Bottom pills -->
  <g transform="translate(164,198)">
    <rect width="90" height="26" rx="13" fill="rgba(239,68,68,.15)" stroke="rgba(239,68,68,.30)" stroke-width="1"/>
    <text x="45" y="17" text-anchor="middle" fill="#f87171" font-size="10" font-weight="700" font-family="Inter,sans-serif" letter-spacing="1">ANAEMIA</text>
    <rect x="100" width="72" height="26" rx="13" fill="rgba(59,130,246,.15)" stroke="rgba(59,130,246,.30)" stroke-width="1"/>
    <text x="136" y="17" text-anchor="middle" fill="#60a5fa" font-size="10" font-weight="700" font-family="Inter,sans-serif" letter-spacing="1">IRON</text>
    <rect x="182" width="62" height="26" rx="13" fill="rgba(168,85,247,.15)" stroke="rgba(168,85,247,.30)" stroke-width="1"/>
    <text x="213" y="17" text-anchor="middle" fill="#c084fc" font-size="10" font-weight="700" font-family="Inter,sans-serif" letter-spacing="1">ESA</text>
    <rect x="254" width="90" height="26" rx="13" fill="rgba(34,197,94,.15)" stroke="rgba(34,197,94,.30)" stroke-width="1"/>
    <text x="299" y="17" text-anchor="middle" fill="#4ade80" font-size="10" font-weight="700" font-family="Inter,sans-serif" letter-spacing="1">VITAMINS</text>
    <rect x="354" width="125" height="26" rx="13" fill="rgba(236,72,153,.15)" stroke="rgba(236,72,153,.30)" stroke-width="1"/>
    <text x="416" y="17" text-anchor="middle" fill="#f472b6" font-size="10" font-weight="700" font-family="Inter,sans-serif" letter-spacing="1">TRANSFUSION</text>
  </g>

  <!-- Pyramid graphic -->
  <g transform="translate(840,28)">
    <!-- ESA peak -->
    <rect x="120" y="10" width="110" height="38" rx="12" fill="url(#pyr)" stroke="rgba(255,255,255,.40)" stroke-width="1.5" opacity=".92">
      <animate attributeName="opacity" values=".7;.95;.7" dur="4s" repeatCount="indefinite"/>
    </rect>
    <text x="175" y="34" text-anchor="middle" fill="#1e293b" font-size="15" font-weight="900" font-family="Inter,sans-serif">ESA</text>

    <!-- Vitamins row -->
    <rect x="40" y="60" width="270" height="42" rx="12" fill="url(#pyr)" stroke="rgba(255,255,255,.35)" stroke-width="1.5" opacity=".88">
      <animate attributeName="opacity" values=".65;.90;.65" dur="4.5s" repeatCount="indefinite"/>
    </rect>
    <text x="175" y="86" text-anchor="middle" fill="#1e293b" font-size="14" font-weight="800" font-family="Inter,sans-serif">VITAMINS B12 · B9 · B6</text>

    <!-- Iron row -->
    <rect x="4" y="114" width="165" height="46" rx="12" fill="url(#pyr)" stroke="rgba(255,255,255,.30)" stroke-width="1.5" opacity=".85">
      <animate attributeName="opacity" values=".6;.88;.6" dur="5s" repeatCount="indefinite"/>
    </rect>
    <text x="86" y="142" text-anchor="middle" fill="#1e293b" font-size="12" font-weight="800" font-family="Inter,sans-serif">IV IRON</text>
    <rect x="182" y="114" width="165" height="46" rx="12" fill="url(#pyr)" stroke="rgba(255,255,255,.30)" stroke-width="1.5" opacity=".85">
      <animate attributeName="opacity" values=".6;.88;.6" dur="5.2s" repeatCount="indefinite"/>
    </rect>
    <text x="264" y="142" text-anchor="middle" fill="#1e293b" font-size="12" font-weight="800" font-family="Inter,sans-serif">ORAL IRON</text>

    <!-- Base label -->
    <rect x="60" y="172" width="230" height="30" rx="15" fill="rgba(255,255,255,.10)" stroke="rgba(255,255,255,.15)" stroke-width="1"/>
    <text x="175" y="192" text-anchor="middle" fill="rgba(255,255,255,.65)" font-size="10" font-weight="700" font-family="Inter,sans-serif" letter-spacing="2">DIAGNOSIS · OPTIMISE · TREAT</text>
  </g>

  <!-- Magnifier icon -->
  <g transform="translate(1220,44)" filter="url(#glow)">
    <rect x="0" y="12" width="130" height="24" rx="8" fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.15)" stroke-width="1"/>
    <rect x="108" y="14" width="16" height="18" rx="2" fill="#ef4444" opacity=".8"/>
    <line x1="118" y1="42" x2="152" y2="72" stroke="rgba(255,255,255,.35)" stroke-width="4" stroke-linecap="round"/>
    <circle cx="170" cy="82" r="22" fill="none" stroke="rgba(255,255,255,.30)" stroke-width="4"/>
    <path d="M160 82 L167 89 L181 73" fill="none" stroke="rgba(34,197,94,.7)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
</svg>
</div>
<script>
(function(){
  const c=document.getElementById('hdr-canvas'); if(!c)return;
  const w=document.getElementById('header-wrap'); if(!w)return;
  c.width=w.offsetWidth; c.height=w.offsetHeight;
  const ctx=c.getContext('2d');
  const pts=Array.from({length:50},()=>({x:Math.random()*c.width,y:Math.random()*c.height,r:Math.random()*1.8+.4,dx:(Math.random()-.5)*.3,dy:(Math.random()-.5)*.3,o:Math.random()*.35+.05}));
  function draw(){
    ctx.clearRect(0,0,c.width,c.height);
    pts.forEach(p=>{
      p.x+=p.dx; p.y+=p.dy;
      if(p.x<0)p.x=c.width; if(p.x>c.width)p.x=0;
      if(p.y<0)p.y=c.height; if(p.y>c.height)p.y=0;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(255,255,255,${p.o})`; ctx.fill();
    });
    requestAnimationFrame(draw);
  }
  draw();
})();
</script>
""", height=290)

# ─── CLOCK ─────────────────────────────────────────────────────────────────────
def render_clock(seconds, running=False):
    clock_id = f"clk_{int(time.time()*1000)%999999}"
    urgent = seconds < 120
    ring_color = "#ef4444" if urgent else "#6366f1"
    glow = "0 0 30px rgba(239,68,68,.5)" if urgent else "0 0 24px rgba(99,102,241,.3)"
    pulse_anim = "animation:pulse-ring 1s ease-in-out infinite;" if (running and urgent) else ""
    script = f"""
    <script>
    let t={seconds}; const el=document.getElementById("{clock_id}");
    function tk(){{ if(!el||t<0)return; el.textContent=String(Math.floor(t/60)).padStart(2,'0')+':'+String(t%60).padStart(2,'0'); t--; }}
    tk(); if(window._pyrCk)clearInterval(window._pyrCk); window._pyrCk=setInterval(tk,1000);
    </script>
    """ if running else ""
    components.html(f"""
    <style>@keyframes pulse-ring {{0%,100%{{box-shadow:0 0 20px rgba(239,68,68,.3)}}50%{{box-shadow:0 0 40px rgba(239,68,68,.7)}}}}</style>
    <div style="background:linear-gradient(145deg,rgba(15,23,42,.95),rgba(30,41,59,.9));border:1px solid {ring_color}44;
    border-radius:24px;padding:16px 20px;text-align:center;box-shadow:{glow};backdrop-filter:blur(12px);{pulse_anim}">
      <div style="font-size:11px;letter-spacing:3px;color:{ring_color};font-weight:700;font-family:Inter,sans-serif;">{'⏱ LIVE' if running else '⏸ PAUSED'}</div>
      <div id="{clock_id}" style="font-size:46px;font-weight:900;color:{'#fbbf24' if urgent else '#f1f5f9'};
      font-family:'JetBrains Mono',monospace;margin-top:4px;text-shadow:0 0 20px {ring_color}66;">{format_clock(seconds)}</div>
    </div>{script}
    """, height=120)

# ─── WINNER ANNOUNCEMENT ──────────────────────────────────────────────────────
def render_winner_announcement():
    wk=winner_key(state); title="It's a Tie!"; accent="#6366f1"
    if wk!="tie": title=state["teams"][wk]["name"]; accent=TEAM_COLORS[wk]["primary"]
    components.html(f"""
    <style>@keyframes confetti-fall{{0%{{transform:translateY(-10px) rotate(0deg);opacity:1}}100%{{transform:translateY(240px) rotate(720deg);opacity:0}}}}</style>
    <div style="position:relative;overflow:hidden;background:linear-gradient(135deg,{accent}dd,#0f172a);border-radius:28px;padding:28px;color:white;
    box-shadow:0 24px 60px rgba(0,0,0,.5),0 0 40px {accent}44;border:1px solid {accent}55;">
      <canvas id="confetti-c" style="position:absolute;inset:0;z-index:1;pointer-events:none;"></canvas>
      <div style="position:absolute;inset:0;background:radial-gradient(circle at 20% 20%,rgba(255,255,255,.18),transparent 30%),
      radial-gradient(circle at 80% 80%,rgba(255,255,255,.10),transparent 25%);z-index:0;"></div>
      <div style="position:relative;z-index:2;text-align:center;">
        <div style="font-size:13px;letter-spacing:4px;font-weight:700;opacity:.85;font-family:Inter,sans-serif;">🏆 WINNER ANNOUNCEMENT 🏆</div>
        <div style="font-size:52px;font-weight:900;margin-top:8px;text-shadow:0 0 30px {accent}88;font-family:Inter,sans-serif;">{title}</div>
        <div style="font-size:16px;opacity:.85;margin-top:10px;letter-spacing:1px;">Preoperative Anaemia Treatment Pyramid · WCA 2026 Champion</div>
        <div style="margin-top:16px;font-size:42px;">🏆 🩸 🎉</div>
      </div>
    </div>
    <script>
    (function(){{
      const c=document.getElementById('confetti-c'); if(!c)return;
      c.width=c.parentElement.offsetWidth; c.height=c.parentElement.offsetHeight;
      const ctx=c.getContext('2d');
      const colors=['#ef4444','#3b82f6','#eab308','#22c55e','#a855f7','#ec4899','#f97316'];
      const P=Array.from({{length:80}},()=>({{x:Math.random()*c.width,y:Math.random()*-c.height,w:Math.random()*8+4,h:Math.random()*6+3,
        dy:Math.random()*2.5+1.5,dx:(Math.random()-.5)*1.5,rot:Math.random()*360,dr:Math.random()*6-3,
        col:colors[Math.floor(Math.random()*colors.length)],o:Math.random()*.7+.3}}));
      let frame=0;
      function draw(){{
        if(frame>400)return;
        ctx.clearRect(0,0,c.width,c.height);
        P.forEach(p=>{{
          p.y+=p.dy; p.x+=p.dx; p.rot+=p.dr;
          if(p.y>c.height+20){{p.y=-10;p.x=Math.random()*c.width;}}
          ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.rot*Math.PI/180);
          ctx.globalAlpha=p.o; ctx.fillStyle=p.col;
          ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);
          ctx.restore();
        }});
        frame++; requestAnimationFrame(draw);
      }}
      draw();
    }})();
    </script>
    """, height=230)

state = load_state()

# ─── LEADERBOARD ───────────────────────────────────────────────────────────────
def render_leaderboard_table():
    red, blue = state["teams"]["team_red"], state["teams"]["team_blue"]
    rows=[{"Team":red["name"],"Score":red["score"],"Challenges":f"{red['correct_cases']}/{len(CASES)}","Pieces":red["pieces_claimed"],"Status":"✅ Finished" if red["finished"] else f"📋 Challenge {red['current_case']+1}"},
          {"Team":blue["name"],"Score":blue["score"],"Challenges":f"{blue['correct_cases']}/{len(CASES)}","Pieces":blue["pieces_claimed"],"Status":"✅ Finished" if blue["finished"] else f"📋 Challenge {blue['current_case']+1}"}]
    st.dataframe(rows, use_container_width=True, hide_index=True)

def finish_current_case(team):
    team["correct_cases"] += 1; team["pieces_claimed"] += 1; team["current_case"] += 1
    if team["current_case"] >= len(CASES):
        team["finished"] = True; team["score"] += 5; team["finish_ts"] = time.time()
    reset_case_state(team); save_state(state)

# ─── CASE HEADER ───────────────────────────────────────────────────────────────
def render_case_header(case, colors):
    ctype = case.get("type","mcq")
    badge_color = CASE_TYPE_COLORS.get(ctype,"#6366f1")
    badge_label = CASE_TYPE_LABELS.get(ctype,"CHALLENGE")
    icon = case.get("icon","🩺")
    badge_html = f'<span class="case-badge" style="background:{badge_color}22;color:{badge_color};border:1px solid {badge_color}44;">{badge_label}</span>' if badge_label else ''
    st.markdown(f"""<div class="glass-card" style="border-left:6px solid {colors['primary']};animation:fade-in .5s ease;">
<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
<span style="font-size:38px;">{icon}</span>
<div>
<div style="font-size:28px;font-weight:900;color:#0f172a;">{case['title']}</div>
{badge_html}
</div>
</div>
<div style="margin-top:14px;padding:14px 16px;background:#f8fafc;border-radius:14px;border:1px solid #e2e8f0;">
<div style="color:#64748b;font-size:12px;font-weight:700;letter-spacing:1px;margin-bottom:6px;">CLINICAL SCENARIO</div>
<div style="font-size:15px;color:#1e293b;line-height:1.6;">{nl2br(case['scenario'])}</div>
</div>
<div style="margin-top:12px;padding:12px 16px;background:#eef2ff;border-radius:14px;border:1px solid #c7d2fe;">
<div style="color:#4338ca;font-size:12px;font-weight:700;letter-spacing:1px;margin-bottom:4px;">QUESTION</div>
<div style="font-size:15px;color:#312e81;font-weight:600;">{case['question']}</div>
</div>
</div>""", unsafe_allow_html=True)

# ─── MCQ CASE ──────────────────────────────────────────────────────────────────
def render_mcq_case(case, team, team_key, colors):
    if team["last_result"]=="correct":
        play_tone("correct"); st.success(case["feedback"][case["correct"]]); st.success("✅ Correct! You may now claim a pyramid piece from the instructor.")
    elif team["last_result"]=="incorrect" and team["selected_answer"]:
        play_tone("incorrect"); st.error(case["feedback"][team["selected_answer"]]); st.warning("❌ Incorrect. Try again and analyze the clinical scenario.")
    cols=st.columns(2)
    option_icons = {"A":"🅰️","B":"🅱️","C":"©️","D":"🅳"}
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
        if team["case_hint_available"] and not team["answered_correctly"] and st.button("💡 Use hint", key=f"hint_{team_key}_{case['case']}", use_container_width=True):
            team["show_case_hint"]=True; save_state(state); st.rerun()
        if team["show_case_hint"] and not team["answered_correctly"]:
            st.markdown(f'<div class="hint-box"><b>💡 {case["clue"]}</b></div>', unsafe_allow_html=True)
    with r:
        st.markdown(f"""<div style="background:#eef2ff;border:1px solid #c7d2fe;color:#3730a3;border-radius:16px;padding:14px;">
        <b>🎯 Clinical focus:</b> Match the type of anaemia to the available time before surgery.</div>""", unsafe_allow_html=True)
    if team["answered_correctly"]:
        st.markdown(f'<div class="feedback-piece"><b>🏅 Claim from instructor:</b> {case["piece"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feedback-explain"><b>📖 Why this is correct:</b> {nl2br(case["explanation"])}</div>', unsafe_allow_html=True)
        if st.button("▶️ Go to next challenge", key=f"next_{team_key}_{case['case']}", use_container_width=True):
            finish_current_case(team); st.rerun()
    else:
        st.caption("💡 The hint becomes available after the first wrong answer.")

# ─── SEQUENCE CASE ─────────────────────────────────────────────────────────────
def render_sequence_case(case, team, team_key, colors):
    if team["last_result"]=="correct":
        play_tone("correct"); st.success("✅ Correct sequence! You may now claim a pyramid piece from the instructor.")
    elif team["last_result"]=="incorrect":
        play_tone("incorrect"); st.error("❌ Incorrect sequence. Review the order of management."); st.warning("Try again. The hint is available after the first incorrect attempt.")
    st.markdown('<div class="minor-card">', unsafe_allow_html=True)
    st.markdown("### 🃏 Sequence Builder")
    st.caption("Tap a card to place it into the next available slot. Cards appear in random order.")
    card_icons = {"Iron assessment": "🩸", "Calculate iron deficit": "🧮", "IV iron": "💉", "Re-evaluate Hb": "📊", "Oral iron": "💊", "EPO": "⚡"}
    available = [c for c in team["case5_card_pool"] if c not in team["case5_sequence"]]
    cols = st.columns(3)
    for idx, card in enumerate(available):
        with cols[idx % 3]:
            c_icon = card_icons.get(card, "🃏")
            st.markdown(f'<div class="card-pick"><div class="card-pick-icon">{c_icon}</div><div class="card-pick-label">{card}</div><div class="card-pick-hint">tap to place</div></div>', unsafe_allow_html=True)
            if st.button(f"Place", key=f"{team_key}_seq_card_{idx}_{card}", use_container_width=True):
                if len(team["case5_sequence"]) < 4:
                    team["case5_sequence"].append(card); save_state(state); st.rerun()
    st.markdown("### 📥 Drop Zone")
    slots = st.columns(4)
    for i in range(4):
        with slots[i]:
            if i < len(team["case5_sequence"]):
                st.markdown(f"""<div class="sequence-slot-filled">
                <div style="font-size:11px;color:#6366f1;font-weight:800;letter-spacing:1px;">STEP {i+1}</div>
                <div style="margin-top:8px;font-weight:800;color:#1e293b;font-size:14px;">{team["case5_sequence"][i]}</div></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="sequence-slot">
                <div style="font-size:11px;color:#94a3b8;font-weight:800;letter-spacing:1px;">STEP {i+1}</div>
                <div style="margin-top:8px;color:#94a3b8;font-size:13px;">Drop card here</div></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    a,b,c=st.columns([1,1,1])
    with a:
        if st.button("✅ Check sequence", key=f"check_seq_{team_key}", use_container_width=True):
            if team["case5_sequence"] == case["correct_sequence"]:
                team["answered_correctly"]=True; team["last_result"]="correct"; team["score"] += 10
            else:
                team["attempts_in_case"] += 1; team["case_hint_available"]=True; team["last_result"]="incorrect"; team["score"]=max(0, team["score"]-1)
                team["case5_sequence"]=[]; team["case5_card_pool"]=shuffled_sequence_cards()
            save_state(state); st.rerun()
    with b:
        if st.button("🔄 Reset sequence", key=f"reset_seq_{team_key}", use_container_width=True):
            team["case5_sequence"]=[]; team["case5_card_pool"]=shuffled_sequence_cards(); team["last_result"]=None; save_state(state); st.rerun()
    with c:
        st.markdown(f"""<div style="background:#eef2ff;border:1px solid #c7d2fe;color:#3730a3;border-radius:16px;padding:14px;">
        <b>🎯 Clinical focus:</b> This station tests stepwise clinical reasoning.</div>""", unsafe_allow_html=True)
    if team["case_hint_available"] and not team["answered_correctly"] and st.button("💡 Use hint", key=f"hint_seq_{team_key}", use_container_width=True):
        team["show_case_hint"]=True; save_state(state); st.rerun()
    if team["show_case_hint"] and not team["answered_correctly"]:
        st.markdown(f'<div class="hint-box"><b>💡 {case["clue"]}</b></div>', unsafe_allow_html=True)
    if team["answered_correctly"]:
        st.markdown(f'<div class="feedback-piece"><b>🏅 Claim from instructor:</b> {case["piece"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feedback-explain"><b>📖 Why this is correct:</b> {nl2br(case["explanation"])}</div>', unsafe_allow_html=True)
        if st.button("▶️ Go to next challenge", key=f"next_seq_{team_key}", use_container_width=True):
            finish_current_case(team); st.rerun()

# ─── MATCHING CASE ─────────────────────────────────────────────────────────────
def render_matching_case(case, team, team_key, colors):
    if team["last_result"]=="correct":
        play_tone("correct"); st.success("✅ Correct matching! You may now claim a pyramid piece from the instructor.")
    elif team["last_result"]=="incorrect":
        play_tone("incorrect"); st.error("❌ Incorrect matching. Review dose and frequency."); st.warning("Try again. Hint is available after the first incorrect attempt.")
    st.markdown('<div class="minor-card">', unsafe_allow_html=True)
    st.markdown("### 🔗 Match each treatment with the correct dose and frequency")
    for idx, treatment in enumerate(MATCHING_TREATMENTS):
        c1,c2,c3=st.columns([1.25,1.2,1.1])
        with c1:
            st.markdown(f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:10px 14px;margin-top:4px;">
            <span style="font-weight:800;color:#1e293b;">💊 {treatment}</span></div>""", unsafe_allow_html=True)
        with c2:
            dose_options = team["case6_dose_order"]
            current_dose = team["case6_matches"].get(treatment, None)
            if current_dose and current_dose in dose_options:
                selected_idx = dose_options.index(current_dose)
            else:
                selected_idx = 0
            dose = st.selectbox(f"Dose for {treatment}", dose_options, index=selected_idx, key=f"{team_key}_dose_{idx}", label_visibility="collapsed")
            team["case6_matches"][treatment]=dose
        with c3:
            freq_options = team["case6_freq_order"]
            current_freq = team["case6_freqs"].get(treatment, None)
            if current_freq and current_freq in freq_options:
                selected_idx = freq_options.index(current_freq)
            else:
                selected_idx = 0
            freq = st.selectbox(f"Frequency for {treatment}", freq_options, index=selected_idx, key=f"{team_key}_freq_{idx}", label_visibility="collapsed")
            team["case6_freqs"][treatment]=freq
        save_state(state)
    st.markdown('</div>', unsafe_allow_html=True)
    a,b=st.columns([1,1])
    with a:
        if st.button("✅ Check matching", key=f"check_match_{team_key}", use_container_width=True):
            ok = all(team["case6_matches"].get(t)==d and team["case6_freqs"].get(t)==f for t,(d,f) in MATCHING_CORRECT.items())
            if ok:
                team["answered_correctly"]=True; team["last_result"]="correct"; team["score"] += 10
            else:
                team["attempts_in_case"] += 1; team["case_hint_available"]=True; team["last_result"]="incorrect"; team["score"]=max(0, team["score"]-1)
            save_state(state); st.rerun()
    with b:
        st.markdown(f"""<div style="background:#ecfdf5;border:1px solid #6ee7b7;color:#065f46;border-radius:16px;padding:14px;">
        <b>🎯 Clinical focus:</b> Practical dosing and frequency knowledge.</div>""", unsafe_allow_html=True)
    if team["case_hint_available"] and not team["answered_correctly"] and st.button("💡 Use hint", key=f"hint_matching_{team_key}", use_container_width=True):
        team["show_case_hint"]=True; save_state(state); st.rerun()
    if team["show_case_hint"] and not team["answered_correctly"]:
        st.markdown(f'<div class="hint-box"><b>💡 {case["clue"]}</b></div>', unsafe_allow_html=True)
    if team["answered_correctly"]:
        st.markdown(f'<div class="feedback-piece"><b>🏅 Claim from instructor:</b> {case["piece"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feedback-explain"><b>📖 Why this is correct:</b> {nl2br(case["explanation"])}</div>', unsafe_allow_html=True)
        if st.button("▶️ Go to next challenge", key=f"next_matching_{team_key}", use_container_width=True):
            finish_current_case(team); st.rerun()

# ─── BOARD CASE ────────────────────────────────────────────────────────────────
def board_is_revealed(team, card_id): return card_id in team["case7_matched"] or card_id in team["case7_selected"]

def handle_board_click(team, card_id):
    if card_id in team["case7_matched"] or card_id in team["case7_selected"]: return
    if len(team["case7_selected"])==2: team["case7_selected"]=[]
    team["case7_selected"].append(card_id)
    if len(team["case7_selected"])==2:
        cards={c["id"]:c for c in team["case7_cards"]}
        c1,c2=cards[team["case7_selected"][0]], cards[team["case7_selected"][1]]
        if c1["pair"]==c2["pair"]:
            team["case7_matched"].extend(team["case7_selected"]); team["case7_selected"]=[]; team["case7_message"]="Correct relation uncovered!"; team["last_result"]="correct"; team["case7_anim"]=f"{c1['label']} ↔ {c2['label']}"
            if len(team["case7_matched"])==len(team["case7_cards"]): team["answered_correctly"]=True; team["score"] += 10
        else:
            team["attempts_in_case"] += 1; team["case_hint_available"]=True; team["case7_message"]="Not a match. Try again."; team["last_result"]="incorrect"; team["score"]=max(0, team["score"]-1); team["case7_selected"]=[]; team["case7_anim"]=""
    save_state(state)

def render_match_animation(team):
    if team["case7_anim"]:
        components.html(f"""
        <div style="margin:8px 0;padding:16px;border-radius:20px;
        background:linear-gradient(135deg,#ecfdf5,#eff6ff);
        border:1px solid #86efac;text-align:center;
        animation:pop .5s cubic-bezier(.68,-.55,.27,1.55) 1;">
          <div style="font-size:12px;color:#16a34a;font-weight:800;letter-spacing:3px;">MATCH DISCOVERED</div>
          <div style="font-size:26px;font-weight:900;color:#0f172a;margin-top:6px;">{team["case7_anim"]}</div>
        </div>
        <style>@keyframes pop {{0%{{transform:scale(.8);opacity:0}}60%{{transform:scale(1.05)}}100%{{transform:scale(1);opacity:1}}}}</style>
        """, height=100)

def render_board_case(case, team, team_key, colors):
    if team["last_result"]=="correct" and not team["answered_correctly"]:
        play_tone("correct"); st.success(team["case7_message"] or "Correct relation!"); render_match_animation(team)
    elif team["last_result"]=="incorrect":
        play_tone("incorrect"); st.error(team["case7_message"] or "Incorrect."); st.warning("Try again. Hint available after first wrong attempt.")
    elif team["answered_correctly"]:
        play_tone("winner"); st.success("🎉 Board completed! All concept pairs uncovered!"); st.success("You may now claim a pyramid piece from the instructor.")
    st.markdown('<div class="minor-card">', unsafe_allow_html=True)
    st.markdown("### 🧩 Hidden Concept Board")
    st.caption("Reveal related concepts by selecting two cards. Win by uncovering all pairs.")
    matched_count = len(team["case7_matched"])//2
    total_pairs = len(BOARD_PAIRS)
    st.markdown(f"""<div style="margin-bottom:12px;"><span style="background:#ecfdf5;color:#166534;padding:4px 12px;border-radius:99px;font-weight:700;font-size:13px;border:1px solid #86efac;">
    Pairs found: {matched_count}/{total_pairs}</span></div>""", unsafe_allow_html=True)
    cards=team["case7_cards"]; ncols=4
    for row_start in range(0,len(cards),ncols):
        cols=st.columns(ncols)
        for i,card in enumerate(cards[row_start:row_start+ncols]):
            revealed = board_is_revealed(team, card["id"])
            matched = card["id"] in team["case7_matched"]
            if matched:
                label = f"✅ {card['label']}"
            elif revealed:
                label = f"👁 {card['label']}"
            else:
                label = "❓"
            with cols[i]:
                if st.button(label, key=f"{team_key}_card_{card['id']}", use_container_width=True):
                    handle_board_click(team, card["id"]); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    if team["case_hint_available"] and not team["answered_correctly"] and st.button("💡 Use hint", key=f"hint_board_{team_key}", use_container_width=True):
        team["show_case_hint"]=True; save_state(state); st.rerun()
    if team["show_case_hint"] and not team["answered_correctly"]:
        st.markdown(f'<div class="hint-box"><b>💡 {case["clue"]}</b></div>', unsafe_allow_html=True)
    st.markdown(f"""<div style="background:#fdf2f8;border:1px solid #f9a8d4;color:#9d174d;border-radius:16px;padding:14px;margin-top:10px;">
    <b>🎯 Clinical focus:</b> Integrate pathology, timing and treatment choice into one PBM reasoning map.</div>""", unsafe_allow_html=True)
    if team["answered_correctly"]:
        st.markdown(f'<div class="feedback-piece"><b>🏅 Claim from instructor:</b> {case["piece"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feedback-explain"><b>📖 Why this is correct:</b> {nl2br(case["explanation"])}</div>', unsafe_allow_html=True)
        if st.button("🏁 Finish game", key=f"finish_board_{team_key}", use_container_width=True):
            finish_current_case(team); st.rerun()

# ─── TEAM SCREEN ───────────────────────────────────────────────────────────────
def render_team_screen(team_key):
    team=state["teams"][team_key]; other_key="team_blue" if team_key=="team_red" else "team_red"; other_team=state["teams"][other_key]; colors=TEAM_COLORS[team_key]
    top1,top2,top3=st.columns([1.7,.8,.8])
    with top1:
        pct = int(team["correct_cases"]/len(CASES)*100)
        st.markdown(f"""
        <div class="glass-card" style="border-top:5px solid {colors['primary']};box-shadow:0 20px 50px {colors['glow']};">
          <div style="display:flex;align-items:center;gap:14px;">
            <div style="width:54px;height:54px;border-radius:16px;background:{colors['gradient']};display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 8px 20px {colors['glow']};">🩸</div>
            <div>
              <div style="font-size:32px;font-weight:900;color:{colors['primary']};">{team['name']}</div>
              <div style="font-size:13px;color:#64748b;letter-spacing:1px;">WCA 2026 · PBM Competition</div>
            </div>
          </div>
          <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
            <span class="metric-pill-neutral" style="font-size:.95rem;">🏆 {team['score']} pts</span>
            <span class="metric-pill-neutral">📋 {team['correct_cases']}/{len(CASES)} challenges</span>
            <span class="metric-pill-neutral">🔺 {team['pieces_claimed']} pieces</span>
            <span class="metric-pill-neutral">📊 {pct}%</span>
          </div>
        </div>""", unsafe_allow_html=True)
    with top2: render_clock(remaining_seconds(state), state.get("timer_running", False))
    with top3:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚔️ Competition</div>', unsafe_allow_html=True)
        st.write(f"Opponent: **{other_team['name']}**")
        st.write(f"Leader: **{winner_name(state)}**")
        if st.button("🔄 Refresh", use_container_width=True): st.rerun()
        if st.button("🚪 Logout", use_container_width=True): st.session_state.pop("logged_role",None); st.session_state.pop("logged_team",None); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("📖 Game Instructions", expanded=False):
        st.markdown("""
- **Challenges 1–4** — Clinical multiple-choice stations (MCQ)
- **Challenge 5** — Management sequence challenge with randomised cards
- **Challenge 6** — Treatment-dose-frequency matching challenge
- **Challenge 7** — Hidden concept discovery board
- 💡 After the first wrong answer, **Use hint** becomes available
- ❌ Wrong answers subtract **1 point** · ✅ Correct challenges add **10 points**
""")
    if team["finished"]:
        render_winner_announcement(); st.success(f"🎉 {team['name']} completed all challenges!"); return
    case=CASES[team["current_case"]]; st.progress(team["current_case"]/len(CASES)); render_case_header(case, colors)
    if case["type"]=="mcq": render_mcq_case(case, team, team_key, colors)
    elif case["type"]=="sequence": render_sequence_case(case, team, team_key, colors)
    elif case["type"]=="matching": render_matching_case(case, team, team_key, colors)
    else: render_board_case(case, team, team_key, colors)

# ─── FACILITATOR ───────────────────────────────────────────────────────────────
def render_facilitator():
    red,blue=state["teams"]["team_red"],state["teams"]["team_blue"]
    top_left,top_mid=st.columns([1.5,.8])
    with top_left:
        st.markdown(f"""<div class="glass-card">
          <div class="section-title">🎛️ Facilitator Control Room</div>
          <div style="margin-top:8px;">
            <span class="metric-pill-red">🔴 {red["name"]}: {red["score"]} pts</span>
            <span class="metric-pill-blue">🔵 {blue["name"]}: {blue["score"]} pts</span>
            <span class="metric-pill-neutral">👑 Leader: {winner_name(state)}</span>
          </div>
        </div>""", unsafe_allow_html=True)
    with top_mid: render_clock(remaining_seconds(state), state.get("timer_running", False))
    m1,m2,m3,m4=st.columns(4)
    m1.metric(red["name"], red["score"], f"{red['correct_cases']} challenges")
    m2.metric(blue["name"], blue["score"], f"{blue['correct_cases']} challenges")
    m3.metric("Pieces", f"{red['pieces_claimed']} – {blue['pieces_claimed']}")
    m4.metric("Winner so far", winner_name(state))
    left,right=st.columns([1,1])
    with left:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">⚙️ Competition Setup</div>', unsafe_allow_html=True)
        state["teams"]["team_red"]["name"]=st.text_input("Red team name", value=red["name"]); state["teams"]["team_blue"]["name"]=st.text_input("Blue team name", value=blue["name"])
        previous_minutes = int(state["timer_minutes"]); state["timer_minutes"]=st.number_input("Timer (minutes)", min_value=1, max_value=60, value=previous_minutes, step=1)
        if int(state["timer_minutes"]) != previous_minutes and not state["timer_running"]:
            state["paused_remaining_seconds"] = int(state["timer_minutes"] * 60)
        if st.button("💾 Save names and timer", key="save_names_timer", use_container_width=True): save_state(state); st.success("Setup saved.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">🔑 Access Codes</div>', unsafe_allow_html=True)
        state["team_codes"]["team_red"]=st.text_input("Red team code", value=state["team_codes"]["team_red"]); state["team_codes"]["team_blue"]=st.text_input("Blue team code", value=state["team_codes"]["team_blue"]); state["facilitator_code"]=st.text_input("Facilitator code", value=state["facilitator_code"])
        if st.button("💾 Save access codes", key="save_access_codes", use_container_width=True): save_state(state); st.success("Codes saved.")
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">⏱️ Timer & Control</div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            if st.button("▶️ Start / restart timer", key="facilitator_start_restart_timer", use_container_width=True):
                state["paused_remaining_seconds"] = int(state["timer_minutes"]*60)
                state["competition_end_ts"]=time.time()+state["paused_remaining_seconds"]
                state["timer_running"]=True; save_state(state); st.rerun()
        with c2:
            if st.button("⏸ Stop timer", key="facilitator_stop_timer", use_container_width=True):
                state["paused_remaining_seconds"] = remaining_seconds(state)
                state["competition_end_ts"] = None; state["timer_running"]=False; save_state(state); st.rerun()
        if st.button("🔄 Reset whole competition", key="facilitator_reset_competition", use_container_width=True): restart_competition(state); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">📊 Leaderboard</div>', unsafe_allow_html=True)
        render_leaderboard_table(); st.markdown('</div>', unsafe_allow_html=True)
    if red["finished"] or blue["finished"]: render_winner_announcement()
    if st.button("🚪 Logout facilitator"): st.session_state.pop("logged_role",None); st.rerun()

# ─── PROJECTION ────────────────────────────────────────────────────────────────
def _projection_video_phase(state):
    """Return 'inicio', 'juegos' or 'final' depending on competition state."""
    red, blue = state["teams"]["team_red"], state["teams"]["team_blue"]
    both_finished = red["finished"] and blue["finished"]
    timer_expired = state["timer_running"] and state["competition_end_ts"] is not None and time.time() >= state["competition_end_ts"]
    if both_finished or timer_expired:
        return "final"
    if state["timer_running"]:
        return "juegos"
    return "inicio"

def render_projection():
    red,blue=state["teams"]["team_red"],state["teams"]["team_blue"]; wk=winner_key(state)
    components.html(f"""
    <div style="background:linear-gradient(135deg,#312e81,#1e3a8a,#7f1d1d);border:1px solid rgba(255,255,255,.15);
    border-radius:28px;padding:24px;text-align:center;box-shadow:0 20px 50px rgba(15,23,42,.25);">
      <div style="font-size:14px;letter-spacing:5px;color:rgba(255,255,255,.7);font-weight:700;">WORLD CONGRESS OF ANAESTHESIOLOGISTS 2026</div>
      <div style="font-size:48px;font-weight:900;color:#ffffff;margin-top:4px;
      background:linear-gradient(135deg,#ffffff,#c7d2fe);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">AUDITORIUM MODE</div>
      <div style="font-size:15px;color:rgba(255,255,255,.6);margin-top:4px;">Preoperative Anaemia Treatment Pyramid · Live Competition</div>
    </div>
    """, height=140)
    btn1, btn2, btn3, btn4, btn5 = st.columns(5)
    with btn1:
        if st.button("🔄 Refresh", key="projection_refresh", use_container_width=True): st.rerun()
    with btn2:
        if st.button("🎬 Intro Video", key="proj_phase_inicio", use_container_width=True):
            st.session_state["projection_video_override"] = "inicio"; st.rerun()
    with btn3:
        if st.button("⚔️ Game Videos", key="proj_phase_juegos", use_container_width=True):
            st.session_state["projection_video_override"] = "juegos"; st.rerun()
    with btn4:
        if st.button("🏆 Final Video", key="proj_phase_final", use_container_width=True):
            st.session_state["projection_video_override"] = "final"; st.rerun()
    with btn5:
        if st.button("🚪 Logout", key="projection_logout", use_container_width=True):
            st.session_state.pop("logged_role",None); st.session_state.pop("logged_team",None); st.rerun()

    # ── Video section ──────────────────────────────────────────────────────────
    phase = st.session_state.get("projection_video_override") or _projection_video_phase(state)
    if phase == "inicio" and VIDEO_INICIO.exists():
        st.markdown("""<div style="background:rgba(99,102,241,.08);border-radius:20px;padding:16px 20px;margin:12px 0;
            border:1px solid rgba(99,102,241,.2);text-align:center;">
            <span style="font-size:22px;">🎬</span>
            <span style="font-size:16px;font-weight:700;color:#4f46e5;margin-left:8px;">Welcome — Introduction Video</span>
        </div>""", unsafe_allow_html=True)
        st.video(str(VIDEO_INICIO), autoplay=True, loop=True, muted=True)
    elif phase == "juegos":
        existing = [v for v in VIDEOS_JUEGOS if v.exists()]
        if existing:
            if "projection_juego_idx" not in st.session_state:
                st.session_state["projection_juego_idx"] = random.randint(0, len(existing) - 1)
            vid_idx = st.session_state["projection_juego_idx"]
            st.markdown(f"""<div style="background:rgba(245,158,11,.08);border-radius:20px;padding:16px 20px;margin:12px 0;
                border:1px solid rgba(245,158,11,.25);text-align:center;">
                <span style="font-size:22px;">⚔️</span>
                <span style="font-size:16px;font-weight:700;color:#d97706;margin-left:8px;">Competition in progress — Video {vid_idx+1}/{len(existing)}</span>
            </div>""", unsafe_allow_html=True)
            st.video(str(existing[vid_idx]), autoplay=True, loop=True, muted=True)
            nav1, nav2, nav3 = st.columns([1, 1, 1])
            with nav1:
                if st.button("⏮ Previous video", key="proj_vid_prev", use_container_width=True):
                    st.session_state["projection_juego_idx"] = (vid_idx - 1) % len(existing); st.rerun()
            with nav2:
                if st.button("🔀 Random video", key="proj_vid_rand", use_container_width=True):
                    st.session_state["projection_juego_idx"] = random.randint(0, len(existing) - 1); st.rerun()
            with nav3:
                if st.button("⏭ Next video", key="proj_vid_next", use_container_width=True):
                    st.session_state["projection_juego_idx"] = (vid_idx + 1) % len(existing); st.rerun()
    elif phase == "final" and VIDEO_FINAL.exists():
        st.markdown("""<div style="background:rgba(16,185,129,.08);border-radius:20px;padding:16px 20px;margin:12px 0;
            border:1px solid rgba(16,185,129,.25);text-align:center;">
            <span style="font-size:22px;">🏆</span>
            <span style="font-size:16px;font-weight:700;color:#059669;margin-left:8px;">Competition Complete — Final Video</span>
        </div>""", unsafe_allow_html=True)
        st.video(str(VIDEO_FINAL), autoplay=True, loop=True, muted=True)

    t1,t2=st.columns([1.2,.8])
    with t1: render_winner_announcement()
    with t2: render_clock(remaining_seconds(state), state.get("timer_running", False))
    cols=st.columns(2)
    for idx,tk in enumerate(["team_red","team_blue"]):
        team=state["teams"][tk]; clrs=TEAM_COLORS[tk]; badge="🏆 LEADING" if wk==tk else "⚔️ COMPETING"
        pct = int(team["correct_cases"]/len(CASES)*100)
        with cols[idx]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,.88);
            border-radius:28px;padding:28px;border-top:6px solid {clrs['primary']};
            box-shadow:0 24px 50px {clrs['glow']};backdrop-filter:blur(16px);border:1px solid rgba(148,163,184,.15);">
              <div style="font-size:38px;font-weight:900;color:{clrs['primary']};">{team['name']}</div>
              <div style="margin-top:6px;font-size:16px;color:#64748b;">{badge}</div>
              <div style="margin-top:20px;font-size:72px;font-weight:900;color:#0f172a;letter-spacing:-2px;">{team['score']}</div>
              <div style="margin-top:4px;font-size:14px;color:#64748b;">POINTS</div>
              <div style="margin-top:20px;display:flex;gap:12px;flex-wrap:wrap;">
                <span class="metric-pill-neutral">📋 {team['correct_cases']}/{len(CASES)}</span>
                <span class="metric-pill-neutral">🔺 {team['pieces_claimed']}</span>
                <span class="metric-pill-neutral">📊 {pct}%</span>
                <span class="metric-pill-neutral">{"✅ Done" if team['finished'] else "🔄 Playing"}</span>
              </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('<div class="minor-card">', unsafe_allow_html=True); st.markdown('<div class="section-title">📊 Professional Leaderboard</div>', unsafe_allow_html=True)
    render_leaderboard_table(); st.markdown('</div>', unsafe_allow_html=True)

# ─── LOGIN PORTAL ──────────────────────────────────────────────────────────────
role=st.session_state.get("logged_role")
if role is None:
    col1,col2=st.columns([1.15,.85])
    with col1:
        st.markdown(f"""
        <div class="glass-card" style="border-top:4px solid #6366f1;">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
            <span style="font-size:32px;">🔐</span>
            <div class="section-title" style="margin-bottom:0;">Access Portal</div>
          </div>
          <div style="color:#64748b;font-size:14px;">Choose your role. Each team sees only its own screen.</div>
        </div>""", unsafe_allow_html=True)
        role_choice=st.radio("Role", ["Team","Facilitator","Auditorium Projection"], horizontal=True)
        if role_choice=="Team":
            team_label=st.selectbox("Team", ["Team Red","Team Blue"]); team_key="team_red" if team_label=="Team Red" else "team_blue"
            code=st.text_input("Team access code", type="password")
            if st.button("🔓 Login as team", use_container_width=True):
                if code==state["team_codes"][team_key]:
                    st.session_state["logged_role"]="team"; st.session_state["logged_team"]=team_key; st.rerun()
                else: st.error("Incorrect team access code.")
        elif role_choice=="Facilitator":
            code=st.text_input("Facilitator access code", type="password")
            if st.button("🔓 Login as facilitator", use_container_width=True):
                if code==state["facilitator_code"]:
                    st.session_state["logged_role"]="facilitator"; st.rerun()
                else: st.error("Incorrect facilitator code.")
        else:
            st.caption("📽️ Projection mode is view-only and ideal for the auditorium screen.")
            if st.button("📽️ Open auditorium projection", use_container_width=True):
                st.session_state["logged_role"]="projection"; st.rerun()
    with col2:
        st.markdown("""
        <div class="minor-card" style="border-top:4px solid #eab308;">
          <div class="section-title">📖 Game Instructions</div>
          <div style="margin-top:8px;color:#334155;line-height:1.7;font-size:14px;">
            <div style="margin-bottom:8px;">🩺 <b>Challenges 1–4</b> — Clinical MCQ stations</div>
            <div style="margin-bottom:8px;">🔢 <b>Challenge 5</b> — Management sequence builder</div>
            <div style="margin-bottom:8px;">🔗 <b>Challenge 6</b> — Treatment matching challenge</div>
            <div style="margin-bottom:8px;">🧩 <b>Challenge 7</b> — Concept discovery board</div>
            <div style="margin-bottom:8px;">💡 Hints available after first wrong answer</div>
            <div>🏅 Claim pyramid pieces from the instructor after each correct challenge</div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="minor-card" style="margin-top:14px;border-top:4px solid #22c55e;">
          <div class="section-title">🌍 WCA 2026</div>
          <div style="color:#475569;margin-top:6px;font-size:14px;line-height:1.7;">
            World Congress of Anaesthesiologists<br/>
            Patient Blood Management Competition<br/>
            <span style="color:#16a34a;font-weight:700;">Build the Treatment Pyramid!</span>
          </div>
        </div>""", unsafe_allow_html=True)
elif role=="facilitator":
    render_facilitator()
elif role=="projection":
    render_projection()
else:
    render_team_screen(st.session_state.get("logged_team","team_red"))
