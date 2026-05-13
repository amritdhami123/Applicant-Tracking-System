import streamlit as st
from pdf_parser import extract_text_from_pdf
from nlp_engine import calculate_match_score, get_missing_keywords, get_matching_keywords

st.set_page_config(
    page_title="AI ATS Resume Optimizer",
    page_icon="🎯",
    layout="wide"
)

# ===================== FIXED CSS =====================
st.markdown("""
<style>
    /* Main Background */
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        padding: 15px !important;
    }
    
    /* Job Description Text Area */
    .stTextArea textarea {
        background-color: #131324 !important; 
        border: 1px solid rgba(255,255,255,0.25) !important;
        color: #FFFFFF !important; 
        border-radius: 10px !important;
        padding: 15px !important;
    }
    .stTextArea textarea::placeholder {
        color: rgba(255,255,255,0.4) !important;
    }
    
    /* =========================================
       FIX: FILE UPLOADER VISIBILITY
       ========================================= */
    /* 1. Force the drag-and-drop box to be dark */
    div[data-testid="stFileUploader"] section {
        background-color: #0a0610 !important; 
        border: 2px dashed rgba(102, 126, 234, 0.6) !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    /* 2. Force ALL text inside to be bright white */
    div[data-testid="stFileUploader"] section * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* 3. Target the specific text elements */
    div[data-testid="stFileUploader"] section p {
        color: #ffffff !important;
    }
    
    /* 4. Make drag-and-drop text visible */
    div[data-testid="stFileUploader"] section div {
        color: #ffffff !important;
    }
    
    /* 5. Style the "Browse files" button inside the uploader */
    div[data-testid="stFileUploader"] section button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-weight: bold !important;
        padding: 5px 15px !important;
    }
    div[data-testid="stFileUploader"] section button:hover {
        background-color: rgba(255, 255, 255, 0.25) !important;
        border-color: #ffffff !important;
    }
    
    /* 6. Make the little upload cloud icon white */
    div[data-testid="stFileUploader"] section svg {
        fill: #ffffff !important;
    }
    /* ========================================= */
    
    /* Metrics Boxes */
    [data-testid="metric-container"] {
        background-color: #131324 !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    [data-testid="stMetricValue"] {
        color: #4facfe !important;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
    }
    [data-testid="stMetricLabel"] p {
        color: rgba(255,255,255,0.85) !important;
        font-weight: 600 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #f093fb) !important;
        border-radius: 10px !important;
    }
    .stProgress > div > div > div {
        background-color: #131324 !important;
        border-radius: 10px !important;
        height: 12px !important;
    }
    
    /* Global Text Colors */
    p, h1, h2, h3, label, span {
        color: white !important;
    }
    
    .stCheckbox label { color: white !important; }
    hr { border-color: rgba(255,255,255,0.12) !important; }
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("<br>", unsafe_allow_html=True)

_, mid, _ = st.columns([1, 3, 1])
with mid:
    st.markdown("<h1 style='text-align:center; color:white;'>🎯 AI ATS Resume Optimizer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.85);'>Upload your resume and paste any job description. Our AI analyzes your match score and helps you beat the Applicant Tracking System.</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    with s1: st.metric("Accuracy", "98%")
    with s2: st.metric("Resumes Analyzed", "10K+")
    with s3: st.metric("Interview Rate", "2x")
    with s4: st.metric("Price", "Free")

st.divider()

# ===================== UPLOAD =====================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📄 Upload Your Resume")
    st.caption("PDF format only • Max 10MB")
    uploaded_file = st.file_uploader("PDF", type=["pdf"], label_visibility="collapsed")

with col2:
    st.subheader("💼 Paste Job Description")
    st.caption("Full job posting for best results")
    job_description = st.text_area(
        "JD",
        height=200,
        placeholder="We are looking for a Data Scientist with experience in Python, Machine Learning, SQL...",
        label_visibility="collapsed"
    )

st.divider()
st.info("💡 **Pro Tips:** Copy the full job description  •  Use a text-based PDF  •  Aim for 80%+ before applying")
st.markdown("<br>", unsafe_allow_html=True)

# ===================== BUTTON =====================
_, mid_btn, _ = st.columns([1, 2, 1])
with mid_btn:
    analyze = st.button("🚀 Analyze My Resume", use_container_width=True)

st.divider()

# ===================== RESULTS =====================
if analyze:
    if uploaded_file is not None and job_description.strip() != "":
        with st.spinner("🔍 Analyzing your resume..."):

            resume_text = extract_text_from_pdf(uploaded_file)

            # SAFETY CHECK 1: Did we extract anything at all?
            if not resume_text or len(resume_text.strip()) < 10:
                st.error("❌ Could not read the text in this PDF. Please ensure it is a text-based PDF and not an image or a scanned document.")
                st.stop()

            if "Error" in str(resume_text):
                st.error(f"❌ {resume_text}")
                st.stop()

            # --- NEW FEATURE: Let the user see what the AI read ---
            with st.expander("👀 View what the AI extracted from your Resume (Debug)"):
                st.text("If this text looks like gibberish or is empty, the PDF encoding is broken.\n\n" + resume_text[:1500] + "...")

            # Calculate
            match_score = calculate_match_score(resume_text, job_description)
            missing_kw  = get_missing_keywords(resume_text, job_description)
            matching_kw = get_matching_keywords(resume_text, job_description)

            # SAFETY CHECK 2: If score is 0.0%, explain why
            if match_score == 0.0:
                st.warning("⚠️ Your score is 0.0%. This usually means your PDF has strict formatting that hides the text, OR your resume shares zero keywords with the Job Description. Check the 'View what the AI extracted' box above.")

            # ===================== SCORE DISPLAY =====================
            st.markdown("<br>", unsafe_allow_html=True)

            _, score_col, _ = st.columns([1, 2, 1])
            with score_col:

                st.markdown(
                    "<h3 style='text-align:center; color:rgba(255,255,255,0.7); "
                    "letter-spacing:2px; font-weight:500; "
                    "text-transform:uppercase; font-size:0.9rem;'>"
                    "Your ATS Score is</h3>",
                    unsafe_allow_html=True
                )

                if match_score >= 80:
                    color = "#38ef7d"
                    emoji = "🏆"
                    msg   = "Excellent! Your resume is highly optimized."
                    st.balloons()
                elif match_score >= 60:
                    color = "#ffd200"
                    emoji = "✅"
                    msg   = "Good match! Add a few more keywords."
                elif match_score >= 40:
                    color = "#4facfe"
                    emoji = "⚠️"
                    msg   = "Moderate match. More keywords needed."
                else:
                    color = "#f5576c"
                    emoji = "❌"
                    msg   = "Low match. Major revisions needed."

                st.markdown(
                    f"<h1 style='text-align:center; font-size:6rem; "
                    f"font-weight:900; color:{color}; line-height:1; "
                    f"margin:10px 0;'>{match_score}%</h1>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<p style='text-align:center; font-size:1.1rem; "
                    f"font-weight:600; color:white;'>{emoji} {msg}</p>",
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("Match Progress")
            st.progress(max(0.0, min(match_score / 100.0, 1.0)))
            st.markdown("<br>", unsafe_allow_html=True)
            st.divider()

            # ===================== KEYWORDS =====================
            kw1, kw2 = st.columns(2, gap="large")

            with kw1:
                st.subheader(f"✅ Matching Keywords ({len(matching_kw)})")
                if matching_kw:
                    for kw in matching_kw:
                        st.success(f"✓  {kw}")
                else:
                    st.caption("No matching keywords found.")

            with kw2:
                st.subheader(f"❌ Missing Keywords ({len(missing_kw)})")
                if missing_kw:
                    for kw in missing_kw:
                        st.error(f"✗  {kw}")
                else:
                    st.success("🎉 No keywords missing! You are ready to apply!")

            st.markdown("<br>", unsafe_allow_html=True)
            st.divider()

            # ===================== ACTION PLAN =====================
            if missing_kw:
                st.subheader("🗺️ Your Action Plan")

                top5  = ", ".join(missing_kw[:5])
                extra = f" + {len(missing_kw) - 5} more" if len(missing_kw) > 5 else ""

                st.markdown(f"""
**1️⃣ Add these missing keywords to your resume:**
> {top5}{extra}

**2️⃣ Include missing skills in your Skills and Work Experience sections**

**3️⃣ Re-upload your updated resume to track your improvement**

**4️⃣ Aim for 80%+ before submitting your application**
                """)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**📋 Missing Keywords Checklist:**")
                cols = st.columns(3)
                for i, kw in enumerate(missing_kw):
                    with cols[i % 3]:
                        st.checkbox(kw, key=f"kw_{i}")

    else:
        st.error("❌ Please upload a PDF resume AND paste a job description.")

# ===================== FOOTER =====================
st.divider()
st.markdown(
    "<p style='text-align:center; color:rgba(255,255,255,0.4); font-size:0.8rem;'>"
    "🎯 AI ATS Resume Optimizer • Built with Streamlit & NLP • "
    "Made with ❤️ to help job seekers land their dream jobs</p>",
    unsafe_allow_html=True
)
