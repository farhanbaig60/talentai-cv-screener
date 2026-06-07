# ============================================
# TalentAI — Professional CV Maker (Clean)
# Simple, reliable, beautifully formatted
# ============================================

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import io
from groq import Groq
import os

GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_KEY)

# Colors
C_DARK = colors.HexColor("#1a1a1a")
C_BLUE = colors.HexColor("#0052cc")
C_GRAY = colors.HexColor("#555555")
C_LGRAY = colors.HexColor("#999999")


def ai_enhance_summary(name, title, summary, skills, experience):
    """AI writes a powerful professional summary"""
    prompt = f"""Write a professional 2-sentence CV summary for someone.

Name: {name}
Role: {title}
Current note: {summary if summary else 'Not provided'}
Skills: {', '.join(skills[:10]) if skills else ''}

Rules:
- Sentence 1: "Results-driven {title} with X years of experience in [field]"
- Sentence 2: Key achievement or expertise
- Professional, confident tone
- 30-50 words total
- No bullet points

Write ONLY the summary:"""

    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        result = r.choices[0].message.content.strip()
        return result if result else summary
    except:
        return summary


def generate_cv_pdf(data: dict, photo_bytes=None) -> bytes:
    """Generate a clean, professional CV"""
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
    )

    story = []
    W = A4[0] - 30*mm

    # ── STYLES ────────────────────────────
    style_name = ParagraphStyle(
        "name",
        fontName="Helvetica-Bold",
        fontSize=24,
        textColor=C_DARK,
        spaceAfter=2,
        leading=28
    )

    style_title = ParagraphStyle(
        "title",
        fontName="Helvetica",
        fontSize=11,
        textColor=C_BLUE,
        spaceAfter=6,
        leading=14
    )

    style_contact = ParagraphStyle(
        "contact",
        fontName="Helvetica",
        fontSize=8.5,
        textColor=C_GRAY,
        spaceAfter=2,
        leading=12
    )

    style_section = ParagraphStyle(
        "section",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        textColor=C_BLUE,
        spaceBefore=10,
        spaceAfter=5,
        leading=12
    )

    style_body = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=9,
        textColor=C_GRAY,
        spaceAfter=4,
        leading=13
    )

    style_job_title = ParagraphStyle(
        "job_title",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        textColor=C_DARK,
        spaceAfter=0,
        leading=12
    )

    style_company = ParagraphStyle(
        "company",
        fontName="Helvetica",
        fontSize=9,
        textColor=C_BLUE,
        spaceAfter=1,
        leading=11
    )

    style_duration = ParagraphStyle(
        "duration",
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        textColor=C_LGRAY,
        spaceAfter=3,
        leading=11
    )

    style_bullet = ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=9,
        textColor=C_GRAY,
        leftIndent=12,
        spaceAfter=2,
        leading=12
    )

    # ── DATA ───────────────────────────────
    name = data.get("name", "Your Name")
    title = data.get("title", "Your Title")
    email = data.get("email", "")
    phone = data.get("phone", "")
    location = data.get("location", "")
    linkedin = data.get("linkedin", "")
    summary = data.get("summary", "")
    skills = data.get("skills", [])
    experience = data.get("experience", [])
    education = data.get("education", [])
    certs = data.get("certifications", [])
    languages = data.get("languages", [])
    use_ai = data.get("use_ai", True)

    # ── HEADER ─────────────────────────────
    story.append(Paragraph(name, style_name))
    story.append(Paragraph(title, style_title))

    # Contact info
    contact_parts = []
    if email:
        contact_parts.append(email)
    if phone:
        contact_parts.append(phone)
    if location:
        contact_parts.append(location)
    if linkedin:
        contact_parts.append(f"linkedin.com/in/{linkedin}")

    if contact_parts:
        story.append(Paragraph(" • ".join(contact_parts), style_contact))

    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_BLUE, spaceAfter=6*mm))

    # ── PROFESSIONAL SUMMARY ──────────────
    if summary or (use_ai and name and title):
        story.append(Paragraph("PROFESSIONAL SUMMARY", style_section))
        
        if use_ai and (summary or skills):
            final_summary = ai_enhance_summary(name, title, summary, skills, experience)
        else:
            final_summary = summary

        if final_summary:
            story.append(Paragraph(final_summary, style_body))
            story.append(Spacer(1, 3*mm))

    # ── CORE SKILLS ────────────────────────
    if skills:
        story.append(Paragraph("CORE SKILLS", style_section))
        
        # 3 columns
        per_col = (len(skills) + 2) // 3
        cols = [skills[i:i+per_col] for i in range(0, len(skills), per_col)]
        
        skills_text = ""
        for col in cols:
            if col:
                col_text = " • ".join(col)
                skills_text += col_text + "\n\n"
        
        story.append(Paragraph(skills_text.strip().replace("\n\n", " • "), style_body))
        story.append(Spacer(1, 3*mm))

    # ── WORK EXPERIENCE ────────────────────
    valid_exp = [e for e in experience if e.get("title")]
    if valid_exp:
        story.append(Paragraph("WORK EXPERIENCE", style_section))

        for exp in valid_exp:
            # Title
            story.append(Paragraph(exp.get("title", ""), style_job_title))

            # Company + Duration
            company_duration = []
            if exp.get("company"):
                company_duration.append(exp["company"])
            if exp.get("duration"):
                company_duration.append(exp["duration"])
            
            if company_duration:
                story.append(Paragraph(" • ".join(company_duration), style_company))

            # Description
            desc = exp.get("description", "").strip()
            if desc:
                # Remove bullets if present, we'll re-add them
                desc = desc.replace("•", "").strip()
                
                # Split by newlines
                for line in desc.split("\n"):
                    line = line.strip()
                    if line:
                        story.append(Paragraph(f"• {line}", style_bullet))

            story.append(Spacer(1, 2*mm))

    # ── EDUCATION ──────────────────────────
    valid_edu = [e for e in education if e.get("degree")]
    if valid_edu:
        story.append(Paragraph("EDUCATION", style_section))

        for edu in valid_edu:
            story.append(Paragraph(edu.get("degree", ""), style_job_title))

            edu_parts = []
            if edu.get("institution"):
                edu_parts.append(edu["institution"])
            if edu.get("year"):
                edu_parts.append(str(edu["year"]))

            if edu_parts:
                story.append(Paragraph(" • ".join(edu_parts), style_company))

            if edu.get("grade"):
                story.append(Paragraph(f"Grade: {edu['grade']}", style_duration))

            story.append(Spacer(1, 2*mm))

    # ── CERTIFICATIONS ─────────────────────
    valid_certs = [c for c in certs if c.get("name")]
    if valid_certs:
        story.append(Paragraph("CERTIFICATIONS", style_section))

        for cert in valid_certs:
            cert_text = cert.get("name", "")
            if cert.get("issuer"):
                cert_text += f" • {cert['issuer']}"
            if cert.get("year"):
                cert_text += f" • {cert['year']}"

            story.append(Paragraph(cert_text, style_bullet))

        story.append(Spacer(1, 2*mm))

    # ── LANGUAGES ──────────────────────────
    if languages:
        story.append(Paragraph("LANGUAGES", style_section))
        lang_text = " • ".join(languages)
        story.append(Paragraph(lang_text, style_body))

    # ── BUILD PDF ──────────────────────────
    doc.build(story)
    buffer.seek(0)
    return buffer.read()
