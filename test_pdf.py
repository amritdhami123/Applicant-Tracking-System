import streamlit as st
from pdf_parser import extract_text_from_pdf
from nlp_engine import calculate_match_score, get_missing_keywords, get_matching_keywords

st.set_page_config(page_title="AI ATS Resume Optimizer", page_icon="🎯", layout="wide")

st.title("AI ATS Resume Optimizer")
st.markdown("Optimize your resume against any job description to beat the Applicant Tracking System.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume (PDF)")
    uploaded_file = st.file_uploader("Drop your resume here", type=["pdf"])

with col2:
    st.subheader("2. Paste Job Description")
    job_description = st.text_area("Paste the exact job description here...", height=200)

st.divider()

if st.button("Analyze Resume Now", use_container_width=True):
    if uploaded_file is not None and job_description.strip() != "":
        with st.spinner("Analyzing with NLP..."):
            
            # Extract Text
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # --- NEW DEBUG PANEL ---
            with st.expander("🛠️ Debug: See Under the Hood (Click to expand)"):
                st.markdown("**1. Extracted Resume Preview:**")
                # Show first 500 characters so we know it read correctly
                st.text(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
                
                st.markdown(f"**2. Job Description Length:** {len(job_description.split())} words")

            if "Error" in resume_text:
                st.error(f"{resume_text}")
            elif resume_text.strip() == "":
                st.error("Cannot calculate score. No text was found in the PDF. It might be an image-based PDF.")
            else:
                # Calculations
                match_score = calculate_match_score(resume_text, job_description)
                missing_keywords = get_missing_keywords(resume_text, job_description)
                matching_keywords = get_matching_keywords(resume_text, job_description)
                
                st.success("Analysis Complete!")
                
                # Display Score
                st.markdown(f"### 🎯 ATS Match Score: **{match_score}%**")
                
                if match_score >= 80:
                    st.balloons()
                    st.success("Excellent! Your resume is highly optimized for this role.")
                elif match_score >= 60:
                    st.warning("Good match! Try adding some missing keywords to improve further.")
                elif match_score >= 40:
                    st.warning("Moderate match. Add more keywords from the job description.")
                else:
                    st.error("Low match. Significant revisions needed to pass the ATS.")
                
                # Ensure progress bar stays between 0.0 and 1.0
                st.progress(max(0.0, min(float(match_score) / 100, 1.0)))
                
                st.divider()
                
                st.markdown("### ✅ Matching Keywords (Your Strengths)")
                if matching_keywords:
                    st.markdown(" ".join([f"`{kw}`" for kw in matching_keywords]))
                else:
                    st.info("No matching keywords found. (Did you paste a real job description?)")
                
                st.divider()
                
                st.markdown("### ❌ Missing Keywords (Areas to Improve)")
                if missing_keywords:
                    st.markdown(" ".join([f"`{kw}`" for kw in missing_keywords]))
                else:
                    st.success("Perfect! No major keywords missing!")
                    
    else:
        st.error("Please upload a PDF resume AND paste a Job Description.")
