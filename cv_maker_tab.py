# ============================================
# CV Maker Tab — paste this inside app.py
# Add as new tab after CV Screener tab
# ============================================

# Yeh code app.py mein tab2 ke saath add karo
# tabs line change karo:
# tab1, tab2, tab3 = st.tabs(["🚀 CV Screener", "📝 CV Maker", "👑 Admin Panel"])
# phir with tab2: ke andar yeh sara code paste karo

import streamlit as st
from cv_maker import generate_cv_pdf

def show_cv_maker_tab():
    """CV Maker Tab Content"""

    st.markdown("""
    <div class="hero-wrap" style="padding:32px 20px 24px">
      <div class="hero-badge">AI-Powered</div>
      <div class="hero-title" style="font-size:40px">📝 <span>CV Maker</span></div>
      <div class="hero-sub">Fill in your details — AI creates a professional CV in seconds</div>
    </div>
    """, unsafe_allow_html=True)

    # AI toggle
    use_ai = st.toggle(
        "🤖 Use AI to enhance descriptions (recommended)",
        value=True
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── SECTION 1: Personal Info ─────────────
    st.markdown('<div class="card-label">Section 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">👤 Personal Information</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name     = st.text_input("Full Name *", placeholder="Muhammad Ali Khan")
        email    = st.text_input("Email *", placeholder="ali@email.com")
        location = st.text_input("Location", placeholder="Lahore, Pakistan")
    with col2:
        title    = st.text_input("Job Title *", placeholder="Senior Software Engineer")
        phone    = st.text_input("Phone", placeholder="+92-300-1234567")
        linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/alikhann")

    # Photo upload
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    photo_file = st.file_uploader(
        "📷 Profile Photo (Optional — JPG/PNG)",
        type=["jpg","jpeg","png"],
        key="cv_photo"
    )
    if photo_file:
        col_img, _ = st.columns([1,4])
        with col_img:
            st.image(photo_file, width=100, caption="Photo preview")

    st.markdown("---")

    # ── SECTION 2: Summary ───────────────────
    st.markdown('<div class="card-label">Section 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📋 Professional Summary</div>', unsafe_allow_html=True)

    summary = st.text_area(
        "Brief summary about yourself",
        height=100,
        placeholder="Experienced software engineer with 5+ years in Python development. Passionate about building scalable systems and leading technical teams...",
        key="cv_summary"
    )
    if use_ai:
        st.markdown("<div style='font-size:12px;color:#58a6ff'>✨ AI will enhance this summary automatically</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── SECTION 3: Skills ────────────────────
    st.markdown('<div class="card-label">Section 3</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚡ Skills</div>', unsafe_allow_html=True)

    skills_input = st.text_area(
        "Enter skills (one per line or comma separated)",
        height=120,
        placeholder="Python\nFastAPI\nPostgreSQL\nDocker\nReact\nGit\nAWS",
        key="cv_skills"
    )

    st.markdown("---")

    # ── SECTION 4: Experience ────────────────
    st.markdown('<div class="card-label">Section 4</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">💼 Work Experience</div>', unsafe_allow_html=True)

    num_exp = st.number_input("How many jobs to add?", min_value=1, max_value=6, value=2, key="num_exp")

    experience = []
    for i in range(int(num_exp)):
        st.markdown(f"<div style='font-size:13px;font-weight:600;color:#58a6ff;margin:12px 0 8px'>Job {i+1}</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            j_title = st.text_input("Job Title", placeholder="Senior Developer", key=f"jt_{i}")
        with c2:
            j_company = st.text_input("Company", placeholder="Tech Corp", key=f"jc_{i}")
        with c3:
            j_duration = st.text_input("Duration", placeholder="Jan 2022 — Present", key=f"jd_{i}")

        j_desc = st.text_area(
            "What did you do? (AI will make it professional)",
            placeholder="Led backend development team, built REST APIs, improved system performance by 40%, managed database migrations...",
            height=80,
            key=f"jdesc_{i}"
        )
        experience.append({
            "title": j_title,
            "company": j_company,
            "duration": j_duration,
            "description": j_desc
        })

    st.markdown("---")

    # ── SECTION 5: Education ─────────────────
    st.markdown('<div class="card-label">Section 5</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🎓 Education</div>', unsafe_allow_html=True)

    num_edu = st.number_input("How many degrees?", min_value=1, max_value=4, value=1, key="num_edu")

    education = []
    for i in range(int(num_edu)):
        st.markdown(f"<div style='font-size:13px;font-weight:600;color:#58a6ff;margin:12px 0 8px'>Degree {i+1}</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            e_degree = st.text_input("Degree", placeholder="BS Computer Science", key=f"ed_{i}")
        with c2:
            e_inst = st.text_input("Institution", placeholder="LUMS", key=f"ei_{i}")
        with c3:
            e_year = st.text_input("Year", placeholder="2021", key=f"ey_{i}")
        with c4:
            e_grade = st.text_input("Grade/GPA", placeholder="3.8/4.0", key=f"eg_{i}")
        education.append({
            "degree": e_degree,
            "institution": e_inst,
            "year": e_year,
            "grade": e_grade
        })

    st.markdown("---")

    # ── SECTION 6: Certifications ────────────
    st.markdown('<div class="card-label">Section 6 (Optional)</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🏆 Certifications</div>', unsafe_allow_html=True)

    num_cert = st.number_input("How many certifications?", min_value=0, max_value=6, value=1, key="num_cert")

    certifications = []
    if num_cert > 0:
        for i in range(int(num_cert)):
            c1, c2, c3 = st.columns(3)
            with c1:
                cert_name = st.text_input("Certification Name", placeholder="AWS Solutions Architect", key=f"cn_{i}")
            with c2:
                cert_issuer = st.text_input("Issuer", placeholder="Amazon", key=f"ci_{i}")
            with c3:
                cert_year = st.text_input("Year", placeholder="2023", key=f"cy_{i}")
            certifications.append({"name": cert_name, "issuer": cert_issuer, "year": cert_year})

    st.markdown("---")

    # ── SECTION 7: Languages ─────────────────
    st.markdown('<div class="card-label">Section 7 (Optional)</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🌐 Languages</div>', unsafe_allow_html=True)

    lang_input = st.text_input(
        "Languages (comma separated)",
        placeholder="Urdu (Native), English (Fluent), Arabic (Basic)",
        key="cv_langs"
    )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── GENERATE BUTTON ──────────────────────
    gen_btn = st.button(
        "✨  Generate Professional CV",
        use_container_width=True,
        key="gen_cv_btn"
    )

    if gen_btn:
        # Validation
        if not name or not title or not email:
            st.error("⚠️ Please fill in Name, Job Title, and Email — these are required!")
            return

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        with st.spinner("🤖 AI is creating your professional CV..." if use_ai else "📄 Generating your CV..."):

            # Parse skills
            skills = []
            if skills_input:
                for s in skills_input.replace(",", "\n").split("\n"):
                    s = s.strip().strip("•-").strip()
                    if s:
                        skills.append(s)

            # Parse languages
            languages = [l.strip() for l in lang_input.split(",") if l.strip()]

            # Photo
            photo_bytes = None
            if photo_file:
                photo_bytes = photo_file.read()

            # Build data dict
            cv_data = {
                "name":            name,
                "title":           title,
                "email":           email,
                "phone":           phone,
                "location":        location,
                "linkedin":        linkedin,
                "summary":         summary,
                "skills":          skills,
                "experience":      [e for e in experience if e.get("title")],
                "education":       [e for e in education  if e.get("degree")],
                "certifications":  [c for c in certifications if c.get("name")],
                "languages":       languages,
                "use_ai":          use_ai,
            }

            try:
                pdf_bytes = generate_cv_pdf(cv_data, photo_bytes)

                st.success("✅ Your professional CV is ready!")

                # Preview info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'<div class="met-box"><div class="met-val">{len(skills)}</div><div class="met-lbl">Skills Added</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="met-box"><div class="met-val">{len([e for e in experience if e.get("title")])}</div><div class="met-lbl">Jobs Listed</div></div>', unsafe_allow_html=True)
                with col3:
                    ai_status = "✨ Yes" if use_ai else "❌ No"
                    st.markdown(f'<div class="met-box"><div class="met-val" style="font-size:20px">{ai_status}</div><div class="met-lbl">AI Enhanced</div></div>', unsafe_allow_html=True)

                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

                # Download button
                safe_name = name.replace(" ", "_")
                st.download_button(
                    label="📥  Download CV (PDF)",
                    data=pdf_bytes,
                    file_name=f"{safe_name}_CV.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_cv"
                )

                st.markdown("""
                <div style='text-align:center;font-size:13px;color:#8b949e;margin-top:12px'>
                  💡 Tip: You can now upload this CV to our CV Screener to test how well it matches job descriptions!
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error generating CV: {e}")
