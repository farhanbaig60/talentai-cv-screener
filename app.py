import streamlit as st
from groq import Groq
import fitz
import pandas as pd
import os
MERI_API_KEY = os.environ.get("GROQ_API_KEY", "")

client = Groq(api_key=MERI_API_KEY)

st.set_page_config(
    page_title="TalentAI — CV Screener",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding: 0 40px 40px 40px !important; max-width: 1200px !important;}

/* ── HERO ── */
.hero-wrap {
    text-align: center;
    padding: 56px 20px 40px;
}
.hero-badge {
    display: inline-block;
    background: rgba(88,166,255,0.1);
    border: 1px solid rgba(88,166,255,0.3);
    color: #58a6ff;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 30px;
    margin-bottom: 20px;
}
.hero-title {
    font-size: 56px;
    font-weight: 800;
    color: #e6edf3;
    line-height: 1.1;
    margin-bottom: 12px;
}
.hero-title span {
    background: linear-gradient(135deg, #58a6ff, #bc8cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 18px;
    color: #8b949e;
    font-weight: 400;
}

/* ── CARDS ── */
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 16px;
}
.card-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #58a6ff;
    margin-bottom: 6px;
}
.card-title {
    font-size: 18px;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 18px;
}

/* ── TEXT AREA FIX ── */
.stTextArea > div > div > textarea {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.6 !important;
    caret-color: #58a6ff !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.12) !important;
    outline: none !important;
}
.stTextArea > div > div > textarea::placeholder {
    color: #484f58 !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] > div {
    background: #0d1117 !important;
    border: 2px dashed #30363d !important;
    border-radius: 12px !important;
    padding: 32px 20px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: #58a6ff !important;
}
[data-testid="stFileUploader"] label {
    color: #8b949e !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #1f6feb, #388bfd) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 14px 28px !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 0 20px rgba(31,111,235,0.35) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #388bfd, #58a6ff) !important;
    box-shadow: 0 0 32px rgba(88,166,255,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── METRIC BOX ── */
.met-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}
.met-val {
    font-size: 36px;
    font-weight: 700;
    color: #58a6ff;
    line-height: 1;
}
.met-lbl {
    font-size: 12px;
    color: #8b949e;
    margin-top: 6px;
    font-weight: 500;
}

/* ── RANK CARD ── */
.rcard {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 10px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.rcard:hover {
    border-color: #58a6ff;
    box-shadow: 0 0 20px rgba(88,166,255,0.1);
}

/* ── PROGRESS BAR ── */
.pbar-wrap { margin: 10px 0; }
.pbar-top {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #8b949e;
    margin-bottom: 5px;
}
.pbar-bg {
    height: 6px;
    background: #21262d;
    border-radius: 6px;
    overflow: hidden;
}
.pbar-fill {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #1f6feb, #58a6ff);
}

/* ── BADGES ── */
.badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 600;
}
.badge-green  { background: rgba(35,134,54,0.2);  color: #3fb950; border: 1px solid rgba(63,185,80,0.3); }
.badge-yellow { background: rgba(187,128,9,0.2);  color: #d29922; border: 1px solid rgba(210,153,34,0.3); }
.badge-red    { background: rgba(218,54,51,0.2);  color: #f85149; border: 1px solid rgba(248,81,73,0.3); }
.badge-blue   { background: rgba(31,111,235,0.2); color: #58a6ff; border: 1px solid rgba(88,166,255,0.3); }

/* ── BIG SCORE ── */
.big-score {
    text-align: center;
    padding: 16px;
    background: #0d1117;
    border-radius: 12px;
    border: 1px solid #30363d;
}
.big-score-num {
    font-size: 52px;
    font-weight: 800;
    color: #58a6ff;
    line-height: 1;
}
.big-score-lbl {
    font-size: 12px;
    color: #8b949e;
    margin-top: 4px;
}

/* ── DIVIDER ── */
hr { border-color: #21262d !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    color: #e6edf3 !important;
    font-weight: 500 !important;
}
.streamlit-expanderContent {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-top: none !important;
    color: #e6edf3 !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── DOWNLOAD BTN ── */
[data-testid="stDownloadButton"] button {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}
[data-testid="stDownloadButton"] button:hover {
    border-color: #58a6ff !important;
    color: #58a6ff !important;
}

/* ── ALERT ── */
.stAlert { border-radius: 10px !important; }

/* ── PROGRESS ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #1f6feb, #58a6ff) !important;
    border-radius: 6px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────

def extract_text(pdf_file):
    doc  = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "".join(p.get_text() for p in doc)
    doc.close()
    return text.strip()

def analyze_cv(cv_text, job_desc):
    prompt = f"""You are a senior HR recruiter and talent acquisition specialist.
Carefully analyze the candidate CV against the job description.
Reply ONLY in this exact format — no extra text:

OVERALL SCORE: [0-100]
RECOMMENDATION: [STRONG YES / YES / MAYBE / NO]
SKILLS MATCH: [0-100]
EXPERIENCE MATCH: [0-100]
MATCHING SKILLS: [comma-separated]
MISSING SKILLS: [comma-separated]
STRENGTHS:
- [point]
- [point]
- [point]
CONCERNS:
- [point or None]
SUMMARY: [2 professional sentences]

===JOB DESCRIPTION===
{job_desc}

===CANDIDATE CV===
{cv_text[:3500]}"""

    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def get_int(text, key):
    for line in text.splitlines():
        if line.strip().upper().startswith(key.upper()):
            try:
                return int("".join(filter(str.isdigit, line.split(":",1)[1].strip().split()[0])))
            except: return 0
    return 0

def get_str(text, key):
    for line in text.splitlines():
        if line.strip().upper().startswith(key.upper()):
            try: return line.split(":",1)[1].strip()
            except: return ""
    return ""

def badge(rec):
    rec = rec.upper()
    if rec == "STRONG YES": return "badge-blue",  "🚀 STRONG YES"
    if rec == "YES":         return "badge-green", "✅ YES"
    if rec == "MAYBE":       return "badge-yellow","⚠️ MAYBE"
    return "badge-red", "❌ NO"

def score_color(s):
    if s >= 75: return "#3fb950"
    if s >= 50: return "#d29922"
    return "#f85149"


# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">AI-Powered Recruitment</div>
  <div class="hero-title">Welcome to <span>TalentAI</span></div>
  <div class="hero-sub">Upload CVs · Set job requirements · Get instant AI-powered rankings</div>
</div>
""", unsafe_allow_html=True)


# ── INPUT SECTION ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="card-label">Step 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📋 Job Description</div>', unsafe_allow_html=True)
    job_desc = st.text_area(
        "jd", label_visibility="collapsed", height=240,
        placeholder="Job Title: Finance Officer\n\nRequirements:\n- M.COM / MBA degree\n- 5+ years finance experience\n- Financial reporting & analysis\n- ERP software (SAP/Oracle)\n- Strong Excel skills\n\nLocation: Lahore\nSalary: Market competitive"
    )

with col2:
    st.markdown('<div class="card-label">Step 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📄 Upload Candidate CVs</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "cvs", label_visibility="collapsed",
        type=["pdf"], accept_multiple_files=True
    )
    if uploaded:
        for f in uploaded:
            st.markdown(f"<div style='font-size:13px;color:#3fb950;padding:3px 0'>✅ {f.name}</div>",
                        unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
go = st.button("🚀  Analyze & Rank All Candidates", use_container_width=True)


# ── PROCESSING ────────────────────────────────────────────────────────────────
if go:
    if not job_desc.strip():
        st.error("⚠️  Please enter a Job Description before proceeding.")
        st.stop()
    if not uploaded:
        st.error("⚠️  Please upload at least one CV (PDF).")
        st.stop()

    st.markdown("---")
    prog = st.progress(0, text="Initializing AI analysis...")
    results = []

    for i, f in enumerate(uploaded):
        prog.progress(i / len(uploaded), text=f"Analyzing {f.name}  ({i+1} of {len(uploaded)})")
        try:
            text = extract_text(f)
            if not text:
                st.warning(f"Could not extract text from **{f.name}** — skipped.")
                continue
            raw  = analyze_cv(text, job_desc)
            rec  = get_str(raw,  "RECOMMENDATION").upper()
            bc, bt = badge(rec)
            results.append({
                "file":       f.name,
                "score":      get_int(raw, "OVERALL SCORE"),
                "sk":         get_int(raw, "SKILLS MATCH"),
                "ex":         get_int(raw, "EXPERIENCE MATCH"),
                "rec":        rec,
                "badge_css":  bc,
                "badge_txt":  bt,
                "summary":    get_str(raw, "SUMMARY"),
                "full":       raw,
            })
        except Exception as e:
            st.error(f"Error on {f.name}: {e}")

    prog.progress(1.0, text="✅  Analysis complete!")

    if not results:
        st.error("No results to show.")
        st.stop()

    results.sort(key=lambda x: x["score"], reverse=True)

    # ── METRICS ──────────────────────────────────────────────────────────────
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    for col, val, lbl in [
        (m1, len(results),                               "CVs Analyzed"),
        (m2, results[0]["score"],                        "Top Score"),
        (m3, round(sum(r["score"] for r in results)/len(results)), "Average Score"),
        (m4, sum(1 for r in results if r["rec"] in ["STRONG YES","YES"]), "Recommended"),
    ]:
        with col:
            st.markdown(f"""
            <div class="met-box">
              <div class="met-val">{val}</div>
              <div class="met-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    # ── RANKINGS ─────────────────────────────────────────────────────────────
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="card-label">Ranked Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🏆 Candidate Rankings</div>', unsafe_allow_html=True)

    medals = ["🥇","🥈","🥉"]

    for i, r in enumerate(results):
        medal = medals[i] if i < 3 else f"#{i+1}"
        sc    = score_color(r["score"])

        with st.expander(f"{medal}  {r['file']}   ·   Score: {r['score']}/100   ·   {r['badge_txt']}", expanded=(i==0)):
            left, right = st.columns([3, 1])

            with left:
                st.markdown(f"<div style='font-size:14px;color:#8b949e;margin-bottom:16px'>📝 {r['summary']}</div>",
                            unsafe_allow_html=True)
                st.markdown(f"""
                <div class="pbar-wrap">
                  <div class="pbar-top"><span>Skills Match</span><span>{r['sk']}%</span></div>
                  <div class="pbar-bg"><div class="pbar-fill" style="width:{r['sk']}%"></div></div>
                </div>
                <div class="pbar-wrap">
                  <div class="pbar-top"><span>Experience Match</span><span>{r['ex']}%</span></div>
                  <div class="pbar-bg"><div class="pbar-fill" style="width:{r['ex']}%"></div></div>
                </div>""", unsafe_allow_html=True)

            with right:
                st.markdown(f"""
                <div class="big-score">
                  <div class="big-score-num" style="color:{sc}">{r['score']}</div>
                  <div class="big-score-lbl">out of 100</div>
                  <div style="margin-top:10px">
                    <span class="badge {r['badge_css']}">{r['badge_txt']}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

            with st.expander("📄 Full AI Analysis"):
                st.code(r["full"], language=None)

    # ── TABLE ─────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 Summary Table</div>', unsafe_allow_html=True)
    df = pd.DataFrame([{
        "Rank": f"{medals[i] if i<3 else i+1}",
        "Candidate": r["file"],
        "Score": r["score"],
        "Skills Match": f"{r['sk']}%",
        "Exp Match": f"{r['ex']}%",
        "Recommendation": r["rec"],
    } for i, r in enumerate(results)])
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ── DOWNLOAD ──────────────────────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    report = "\n\n".join(
        f"RANK {i+1}: {r['file']}\nScore: {r['score']}/100\n{'='*50}\n{r['full']}"
        for i, r in enumerate(results)
    )
    st.download_button(
        "💾  Download Full Report (.txt)",
        data=report,
        file_name="talentai_report.txt",
        mime="text/plain",
        use_container_width=True
    )
