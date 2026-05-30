# ============================================
# TalentAI — CV Screener with Signup/Login
# Database: Supabase | AI: Groq
# ============================================

import streamlit as st
from groq import Groq
import fitz
import pandas as pd
import os
import hashlib
import httpx
from datetime import datetime

# ── Keys ─────────────────────────────────────
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
SUPA_URL = os.environ.get("SUPABASE_URL", "")
SUPA_KEY = os.environ.get("SUPABASE_KEY", "")
client = Groq(api_key=GROQ_KEY)

st.set_page_config(
    page_title="TalentAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp{font-family:'Inter',sans-serif!important;background-color:#0d1117!important;color:#e6edf3!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0 40px 40px!important;max-width:1200px!important;}

/* Auth page */
.auth-wrap{max-width:440px;margin:60px auto 0;padding:40px;background:#161b22;border:1px solid #30363d;border-radius:20px;box-shadow:0 8px 40px rgba(0,0,0,0.4);}
.auth-logo{text-align:center;font-size:48px;margin-bottom:8px;}
.auth-title{text-align:center;font-size:26px;font-weight:700;color:#e6edf3;margin-bottom:4px;}
.auth-sub{text-align:center;font-size:14px;color:#8b949e;margin-bottom:28px;}

/* Tabs override */
.stTabs [data-baseweb="tab-list"]{background:#0d1117!important;border-bottom:1px solid #30363d!important;gap:0;}
.stTabs [data-baseweb="tab"]{background:#0d1117!important;color:#8b949e!important;border:none!important;padding:12px 32px!important;font-weight:500!important;font-size:14px!important;}
.stTabs [aria-selected="true"]{color:#e6edf3!important;border-bottom:2px solid #58a6ff!important;}

/* Inputs */
.stTextInput>div>div>input{background-color:#0d1117!important;color:#e6edf3!important;border:1px solid #30363d!important;border-radius:10px!important;font-size:14px!important;padding:12px 16px!important;}
.stTextInput>div>div>input:focus{border-color:#58a6ff!important;box-shadow:0 0 0 3px rgba(88,166,255,0.12)!important;}
.stTextInput>div>div>input::placeholder{color:#484f58!important;}
.stTextInput label{color:#8b949e!important;font-size:13px!important;font-weight:500!important;}
.stTextArea>div>div>textarea{background-color:#0d1117!important;color:#e6edf3!important;border:1px solid #30363d!important;border-radius:10px!important;font-size:14px!important;line-height:1.6!important;}
.stTextArea>div>div>textarea:focus{border-color:#58a6ff!important;box-shadow:0 0 0 3px rgba(88,166,255,0.12)!important;}
.stTextArea>div>div>textarea::placeholder{color:#484f58!important;}

/* Buttons */
.stButton>button{background:linear-gradient(135deg,#1f6feb,#388bfd)!important;border:none!important;border-radius:10px!important;color:#fff!important;font-size:15px!important;font-weight:600!important;padding:12px 28px!important;box-shadow:0 0 20px rgba(31,111,235,0.3)!important;transition:all 0.2s!important;width:100%!important;}
.stButton>button:hover{background:linear-gradient(135deg,#388bfd,#58a6ff)!important;box-shadow:0 0 30px rgba(88,166,255,0.4)!important;transform:translateY(-1px)!important;}

/* File uploader */
[data-testid="stFileUploader"]>div{background:#0d1117!important;border:2px dashed #30363d!important;border-radius:12px!important;padding:24px!important;}
[data-testid="stFileUploader"]>div:hover{border-color:#58a6ff!important;}

/* Hero */
.hero-wrap{text-align:center;padding:48px 20px 36px;}
.hero-badge{display:inline-block;background:rgba(88,166,255,0.1);border:1px solid rgba(88,166,255,0.3);color:#58a6ff;font-size:11px;font-weight:600;letter-spacing:2px;text-transform:uppercase;padding:5px 16px;border-radius:30px;margin-bottom:18px;}
.hero-title{font-size:52px;font-weight:800;color:#e6edf3;line-height:1.1;margin-bottom:10px;}
.hero-title span{background:linear-gradient(135deg,#58a6ff,#bc8cff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero-sub{font-size:17px;color:#8b949e;}

/* Cards */
.card-label{font-size:11px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#58a6ff;margin-bottom:6px;}
.card-title{font-size:18px;font-weight:600;color:#e6edf3;margin-bottom:16px;}

/* Metrics */
.met-box{background:#161b22;border:1px solid #30363d;border-radius:14px;padding:20px;text-align:center;}
.met-val{font-size:36px;font-weight:700;color:#58a6ff;line-height:1;}
.met-lbl{font-size:12px;color:#8b949e;margin-top:6px;font-weight:500;}

/* Progress bars */
.pbar-wrap{margin:10px 0;}
.pbar-top{display:flex;justify-content:space-between;font-size:12px;color:#8b949e;margin-bottom:5px;}
.pbar-bg{height:6px;background:#21262d;border-radius:6px;overflow:hidden;}
.pbar-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,#1f6feb,#58a6ff);}

/* Big score */
.big-score{text-align:center;padding:20px;background:#0d1117;border-radius:12px;border:1px solid #30363d;}
.big-score-num{font-size:52px;font-weight:800;line-height:1;}
.big-score-lbl{font-size:12px;color:#8b949e;margin-top:4px;}

/* Badges */
.badge{display:inline-block;padding:4px 14px;border-radius:30px;font-size:12px;font-weight:600;}
.badge-green{background:rgba(35,134,54,0.2);color:#3fb950;border:1px solid rgba(63,185,80,0.3);}
.badge-yellow{background:rgba(187,128,9,0.2);color:#d29922;border:1px solid rgba(210,153,34,0.3);}
.badge-red{background:rgba(218,54,51,0.2);color:#f85149;border:1px solid rgba(248,81,73,0.3);}
.badge-blue{background:rgba(31,111,235,0.2);color:#58a6ff;border:1px solid rgba(88,166,255,0.3);}

/* Expander */
.streamlit-expanderHeader{background:#161b22!important;border:1px solid #30363d!important;border-radius:10px!important;color:#e6edf3!important;font-weight:500!important;}
.streamlit-expanderContent{background:#161b22!important;border:1px solid #30363d!important;border-top:none!important;color:#e6edf3!important;}
details:first-of-type>summary{background:linear-gradient(135deg,#2a1f00,#3d2e00)!important;border:1px solid #d29922!important;box-shadow:0 0 12px rgba(210,153,34,0.2)!important;}

/* Navbar */
.navbar{display:flex;align-items:center;justify-content:space-between;padding:14px 0;border-bottom:1px solid #21262d;margin-bottom:8px;}
.nav-logo{font-size:18px;font-weight:700;color:#e6edf3;}
.nav-logo span{color:#58a6ff;}
.nav-user{font-size:13px;color:#8b949e;background:#161b22;border:1px solid #30363d;padding:6px 14px;border-radius:30px;}

/* Admin */
.admin-row{display:flex;align-items:center;padding:10px 16px;background:#161b22;border:1px solid #30363d;border-radius:10px;margin-bottom:8px;font-size:13px;color:#e6edf3;}
.admin-email{flex:1;color:#58a6ff;}
.admin-time{color:#8b949e;font-size:12px;}

hr{border-color:#21262d!important;}
[data-testid="stDataFrame"]{border:1px solid #30363d!important;border-radius:12px!important;overflow:hidden!important;}
[data-testid="stDownloadButton"] button{background:#21262d!important;border:1px solid #30363d!important;color:#e6edf3!important;border-radius:10px!important;font-weight:500!important;}
[data-testid="stDownloadButton"] button:hover{border-color:#58a6ff!important;color:#58a6ff!important;}

.logout-btn>button{background:transparent!important;border:1px solid #30363d!important;color:#8b949e!important;font-size:13px!important;padding:6px 16px!important;border-radius:30px!important;box-shadow:none!important;width:auto!important;}
.logout-btn>button:hover{border-color:#f85149!important;color:#f85149!important;transform:none!important;box-shadow:none!important;background:transparent!important;}
</style>
""", unsafe_allow_html=True)


# ── Supabase helpers ──────────────────────────
def supa_headers():
    return {
        "apikey": SUPA_KEY,
        "Authorization": f"Bearer {SUPA_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(email, password, full_name):
    """Register new user in Supabase"""
    try:
        hashed = hash_password(password)
        r = httpx.post(
            f"{SUPA_URL}/rest/v1/users",
            headers=supa_headers(),
            json={
                "email": email,
                "password": hashed,
                "full_name": full_name,
                "is_approved": True,
                "is_admin": False,
                "created_at": datetime.utcnow().isoformat()
            }
        )
        if r.status_code in [200, 201]:
            return True, "Account created successfully!"
        elif r.status_code == 409 or "duplicate" in r.text.lower():
            return False, "Email already registered. Please login."
        else:
            return False, f"Error: {r.text}"
    except Exception as e:
        return False, f"Connection error: {e}"

def login_user(email, password):
    """Check credentials against Supabase"""
    try:
        hashed = hash_password(password)
        r = httpx.get(
            f"{SUPA_URL}/rest/v1/users",
            headers=supa_headers(),
            params={"email": f"eq.{email}", "select": "*"}
        )
        if r.status_code == 200 and r.json():
            user = r.json()[0]
            if user["password"] == hashed:
                if not user.get("is_approved", True):
                    return False, None, "Your account is pending approval."
                # Update last login
                httpx.patch(
                    f"{SUPA_URL}/rest/v1/users",
                    headers=supa_headers(),
                    params={"email": f"eq.{email}"},
                    json={"last_login": datetime.utcnow().isoformat()}
                )
                return True, user, "Login successful!"
            else:
                return False, None, "Wrong password. Please try again."
        else:
            return False, None, "Email not found. Please sign up first."
    except Exception as e:
        return False, None, f"Connection error: {e}"

def log_activity(email, action, detail=""):
    """Log user activity to Supabase"""
    try:
        httpx.post(
            f"{SUPA_URL}/rest/v1/activity_log",
            headers=supa_headers(),
            json={
                "user_email": email,
                "action": action,
                "detail": detail,
                "created_at": datetime.utcnow().isoformat()
            }
        )
    except:
        pass

def get_all_users():
    """Get all users for admin panel"""
    try:
        r = httpx.get(
            f"{SUPA_URL}/rest/v1/users",
            headers=supa_headers(),
            params={"select": "*", "order": "created_at.desc"}
        )
        return r.json() if r.status_code == 200 else []
    except:
        return []

def get_activity_log():
    """Get recent activity"""
    try:
        r = httpx.get(
            f"{SUPA_URL}/rest/v1/activity_log",
            headers=supa_headers(),
            params={"select": "*", "order": "created_at.desc", "limit": "30"}
        )
        return r.json() if r.status_code == 200 else []
    except:
        return []

def update_screening_count(email):
    """Increment user's screening count"""
    try:
        r = httpx.get(
            f"{SUPA_URL}/rest/v1/users",
            headers=supa_headers(),
            params={"email": f"eq.{email}", "select": "total_screenings"}
        )
        if r.status_code == 200 and r.json():
            current = r.json()[0].get("total_screenings", 0) or 0
            httpx.patch(
                f"{SUPA_URL}/rest/v1/users",
                headers=supa_headers(),
                params={"email": f"eq.{email}"},
                json={"total_screenings": current + 1}
            )
    except:
        pass


# ── CV helpers ────────────────────────────────
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
            try: return int("".join(filter(str.isdigit, line.split(":",1)[1].strip().split()[0])))
            except: return 0
    return 0

def get_str(text, key):
    for line in text.splitlines():
        if line.strip().upper().startswith(key.upper()):
            try: return line.split(":",1)[1].strip()
            except: return ""
    return ""

def badge_info(rec):
    rec = rec.upper()
    if rec == "STRONG YES": return "badge-blue",   "🚀 STRONG YES"
    if rec == "YES":         return "badge-green",  "✅ YES"
    if rec == "MAYBE":       return "badge-yellow", "⚠️ MAYBE"
    return "badge-red", "❌ NO"

def score_color(s):
    if s >= 75: return "#3fb950"
    if s >= 50: return "#d29922"
    return "#f85149"


# ── Session state ─────────────────────────────
for key, val in [
    ("logged_in", False), ("user_email", ""),
    ("user_name", ""), ("is_admin", False)
]:
    if key not in st.session_state:
        st.session_state[key] = val


# ════════════════════════════════════════════
# AUTH PAGE
# ════════════════════════════════════════════
if not st.session_state.logged_in:

    st.markdown("""
    <div class="auth-wrap">
      <div class="auth-logo">🧠</div>
      <div class="auth-title">TalentAI</div>
      <div class="auth-sub">AI-Powered CV Screening Platform</div>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        tab_login, tab_signup = st.tabs(["🔑  Sign In", "✨  Create Account"])

        # ── LOGIN TAB ──
        with tab_login:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            l_email = st.text_input("📧 Email", placeholder="you@example.com", key="l_email")
            l_pass  = st.text_input("🔒 Password", type="password", placeholder="Your password", key="l_pass")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("Sign In →", key="login_btn"):
                if not l_email or not l_pass:
                    st.error("Please fill in all fields.")
                else:
                    ok, user, msg = login_user(l_email, l_pass)
                    if ok:
                        st.session_state.logged_in  = True
                        st.session_state.user_email = l_email
                        st.session_state.user_name  = user.get("full_name", "User")
                        st.session_state.is_admin   = user.get("is_admin", False)
                        log_activity(l_email, "LOGIN")
                        st.success("Welcome back! 👋")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

        # ── SIGNUP TAB ──
        with tab_signup:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            s_name  = st.text_input("👤 Full Name", placeholder="Your full name", key="s_name")
            s_email = st.text_input("📧 Email", placeholder="you@example.com", key="s_email")
            s_pass  = st.text_input("🔒 Password", type="password", placeholder="Min 6 characters", key="s_pass")
            s_pass2 = st.text_input("🔒 Confirm Password", type="password", placeholder="Repeat password", key="s_pass2")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("Create Account →", key="signup_btn"):
                if not all([s_name, s_email, s_pass, s_pass2]):
                    st.error("Please fill in all fields.")
                elif len(s_pass) < 6:
                    st.error("Password must be at least 6 characters.")
                elif s_pass != s_pass2:
                    st.error("Passwords do not match.")
                elif "@" not in s_email:
                    st.error("Please enter a valid email address.")
                else:
                    ok, msg = signup_user(s_email, s_pass, s_name)
                    if ok:
                        log_activity(s_email, "SIGNUP")
                        st.success("✅ Account created! Please sign in now.")
                    else:
                        st.error(f"❌ {msg}")

        st.markdown("""
        <div style='text-align:center;margin-top:20px;font-size:12px;color:#484f58'>
          By signing up, you agree to our Terms of Service
        </div>""", unsafe_allow_html=True)

    st.stop()


# ════════════════════════════════════════════
# MAIN APP
# ════════════════════════════════════════════

# Navbar
nav_l, nav_r = st.columns([4, 1])
with nav_l:
    st.markdown(f"""
    <div class="navbar">
      <div class="nav-logo">🧠 <span>Talent</span>AI</div>
    </div>""", unsafe_allow_html=True)
with nav_r:
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='nav-user'>👤 {st.session_state.user_name}</div>", unsafe_allow_html=True)

# Tabs
if st.session_state.is_admin:
    tab1, tab2 = st.tabs(["🚀  CV Screener", "👑  Admin Panel"])
else:
    tab1, = st.tabs(["🚀  CV Screener"])


# ════════════════════════════════════════════
# TAB 1 — CV SCREENER
# ════════════════════════════════════════════
with tab1:

    st.markdown("""
    <div class="hero-wrap">
      <div class="hero-badge">AI-Powered Recruitment</div>
      <div class="hero-title">Welcome to <span>TalentAI</span></div>
      <div class="hero-sub">Upload CVs · Set requirements · Get instant AI rankings</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="card-label">Step 1</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📋 Job Description</div>', unsafe_allow_html=True)
        job_desc = st.text_area("jd", label_visibility="collapsed", height=240,
            placeholder="Job Title: Senior Finance Officer\n\nRequirements:\n- MBA / M.COM degree\n- 5+ years finance experience\n- Financial reporting & budgeting\n\nLocation: Lahore\nSalary: Market competitive")

    with col2:
        st.markdown('<div class="card-label">Step 2</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📄 Upload Candidate CVs</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("cvs", label_visibility="collapsed", type=["pdf"], accept_multiple_files=True)
        if uploaded:
            for f in uploaded:
                st.markdown(f"<div style='font-size:13px;color:#3fb950;padding:2px 0'>✅ {f.name}</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    go = st.button("🚀  Analyze & Rank All Candidates", use_container_width=True)

    if go:
        if not job_desc.strip():
            st.error("⚠️ Please enter a Job Description first.")
            st.stop()
        if not uploaded:
            st.error("⚠️ Please upload at least one CV.")
            st.stop()

        st.markdown("---")
        prog    = st.progress(0, text="Starting AI analysis...")
        results = []

        for i, f in enumerate(uploaded):
            prog.progress(i / len(uploaded), text=f"Analyzing {f.name}  ({i+1}/{len(uploaded)})")
            try:
                text = extract_text(f)
                if not text:
                    st.warning(f"Could not extract text from **{f.name}** — skipped.")
                    continue
                raw = analyze_cv(text, job_desc)
                rec = get_str(raw, "RECOMMENDATION").upper()
                bc, bt = badge_info(rec)
                results.append({
                    "file": f.name, "score": get_int(raw, "OVERALL SCORE"),
                    "sk": get_int(raw, "SKILLS MATCH"), "ex": get_int(raw, "EXPERIENCE MATCH"),
                    "rec": rec, "badge_css": bc, "badge_txt": bt,
                    "summary": get_str(raw, "SUMMARY"), "full": raw,
                })
            except Exception as e:
                st.error(f"Error on {f.name}: {e}")

        prog.progress(1.0, text="✅ Analysis complete!")
        log_activity(st.session_state.user_email, "SCREENED", f"{len(results)} CVs")
        update_screening_count(st.session_state.user_email)

        if not results:
            st.error("No results generated.")
            st.stop()

        results.sort(key=lambda x: x["score"], reverse=True)

        # Metrics
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        for col, val, lbl in [
            (m1, len(results), "CVs Analyzed"),
            (m2, results[0]["score"], "Top Score"),
            (m3, round(sum(r["score"] for r in results)/len(results)), "Avg Score"),
            (m4, sum(1 for r in results if r["rec"] in ["STRONG YES","YES"]), "Recommended"),
        ]:
            with col:
                st.markdown(f'<div class="met-box"><div class="met-val">{val}</div><div class="met-lbl">{lbl}</div></div>', unsafe_allow_html=True)

        # Rankings
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="card-label">Ranked Results</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🏆 Candidate Rankings</div>', unsafe_allow_html=True)

        medals = ["🥇","🥈","🥉"]
        for i, r in enumerate(results):
            medal = medals[i] if i < 3 else f"#{i+1}"
            sc    = score_color(r["score"])
            with st.expander(f"{medal}  {r['file']}   ·   Score: {r['score']}/100   ·   {r['badge_txt']}", expanded=(i==0)):
                left, right = st.columns([3,1])
                with left:
                    st.markdown(f"<div style='font-size:14px;color:#8b949e;margin-bottom:16px'>📝 {r['summary']}</div>", unsafe_allow_html=True)
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
                      <div style="margin-top:10px"><span class="badge {r['badge_css']}">{r['badge_txt']}</span></div>
                    </div>""", unsafe_allow_html=True)
                with st.expander("📄 Full AI Analysis"):
                    st.code(r["full"], language=None)

        # Table
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Summary Table</div>', unsafe_allow_html=True)
        df = pd.DataFrame([{
            "Rank": medals[i] if i<3 else i+1,
            "Candidate": r["file"], "Score": r["score"],
            "Skills": f"{r['sk']}%", "Experience": f"{r['ex']}%",
            "Recommendation": r["rec"],
        } for i, r in enumerate(results)])
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Download
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        report = "\n\n".join(
            f"RANK {i+1}: {r['file']}\nScore: {r['score']}/100\n{'='*50}\n{r['full']}"
            for i, r in enumerate(results)
        )
        st.download_button("💾  Download Full Report", data=report,
            file_name="talentai_report.txt", mime="text/plain", use_container_width=True)

    # Logout
    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown("---")
    _, _, logout_col = st.columns([3,3,1])
    with logout_col:
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            log_activity(st.session_state.user_email, "LOGOUT")
            for key in ["logged_in","user_email","user_name","is_admin"]:
                st.session_state[key] = False if key == "logged_in" else ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 2 — ADMIN PANEL
# ════════════════════════════════════════════
if st.session_state.is_admin:
    with tab2:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="card-title">👑 Admin Panel</div>', unsafe_allow_html=True)

        users = get_all_users()
        logs  = get_activity_log()

        # Stats
        a1, a2, a3, a4 = st.columns(4)
        total_screens = sum(u.get("total_screenings", 0) or 0 for u in users)
        for col, val, lbl in [
            (a1, len(users), "Total Users"),
            (a2, total_screens, "Total Screenings"),
            (a3, sum(1 for u in users if u.get("is_admin")), "Admins"),
            (a4, len(logs), "Activity Logs"),
        ]:
            with col:
                st.markdown(f'<div class="met-box"><div class="met-val">{val}</div><div class="met-lbl">{lbl}</div></div>', unsafe_allow_html=True)

        # Users list
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="card-label">Registered Users</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">👥 All Users</div>', unsafe_allow_html=True)

        for u in users:
            role    = "👑 Admin" if u.get("is_admin") else "👤 User"
            screens = u.get("total_screenings", 0) or 0
            joined  = u.get("created_at", "")[:10] if u.get("created_at") else "—"
            st.markdown(f"""
            <div class="admin-row">
              <span class="admin-email">{u.get('email','')}</span>
              <span style="color:#e6edf3;margin-right:16px">{u.get('full_name','')}</span>
              <span style="color:#8b949e;font-size:12px;margin-right:16px">{role}</span>
              <span style="color:#58a6ff;font-size:12px;margin-right:16px">📊 {screens} screenings</span>
              <span class="admin-time">Joined: {joined}</span>
            </div>""", unsafe_allow_html=True)

        # Activity log
        if logs:
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="card-label">Activity</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📋 Recent Activity</div>', unsafe_allow_html=True)
            for log in logs:
                action_color = {"LOGIN":"#3fb950","LOGOUT":"#8b949e","SCREENED":"#58a6ff","SIGNUP":"#bc8cff"}.get(log.get("action",""),"#e6edf3")
                time_str = log.get("created_at","")[:16].replace("T"," ") if log.get("created_at") else "—"
                st.markdown(f"""
                <div class="admin-row">
                  <span class="admin-email">{log.get('user_email','')}</span>
                  <span style="color:{action_color};font-size:12px;margin-right:12px;min-width:80px">{log.get('action','')}</span>
                  <span style="color:#8b949e;font-size:12px;margin-right:12px">{log.get('detail','')}</span>
                  <span class="admin-time">{time_str}</span>
                </div>""", unsafe_allow_html=True)
