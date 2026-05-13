from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# ===================== CLEAN TEXT =====================
def clean_text(text: str) -> str:
    """Lowercase and remove special characters from text."""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ===================== MATCH SCORE =====================
def calculate_match_score(resume_text: str, job_description: str) -> float:
    """
    Calculate the ATS match score between resume and job description
    using TF-IDF vectorization and cosine similarity.
    Returns a score between 0 and 100.
    """
    if not resume_text.strip() or not job_description.strip():
        return 0.0

    cleaned_resume = clean_text(resume_text)
    cleaned_jd     = clean_text(job_description)

    vectorizer = TfidfVectorizer()
    vectors    = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    score      = cosine_similarity(vectors[0], vectors[1])[0][0]

    return round(score * 100, 1)

# ===================== MATCHING KEYWORDS =====================
def get_matching_keywords(resume_text: str, job_description: str) -> list:
    """
    Returns a list of important keywords from the job description
    that ARE present in the resume.
    """
    resume_words = set(clean_text(resume_text).split())
    jd_words     = set(clean_text(job_description).split())

    # Filter out common stop words for more meaningful results
    stop_words = {
        "and", "the", "is", "in", "it", "of", "to", "a", "an", "for",
        "on", "with", "as", "at", "by", "we", "are", "or", "be", "that",
        "this", "will", "have", "has", "from", "our", "you", "your",
        "their", "they", "was", "were", "been", "not", "but", "can",
        "all", "any", "do", "if", "so", "up", "out", "who", "its",
        "him", "his", "her", "she", "he", "us", "me", "my", "no",
        "which", "more", "also", "than", "into", "about", "other",
        "what", "would", "there", "when", "one", "how", "each"
    }

    jd_keywords = jd_words - stop_words
    matching    = sorted([kw for kw in jd_keywords if kw in resume_words])

    return matching

# ===================== MISSING KEYWORDS =====================
def get_missing_keywords(resume_text: str, job_description: str) -> list:
    """
    Returns a list of important keywords from the job description
    that are NOT present in the resume.
    """
    resume_words = set(clean_text(resume_text).split())
    jd_words     = set(clean_text(job_description).split())

    stop_words = {
        "and", "the", "is", "in", "it", "of", "to", "a", "an", "for",
        "on", "with", "as", "at", "by", "we", "are", "or", "be", "that",
        "this", "will", "have", "has", "from", "our", "you", "your",
        "their", "they", "was", "were", "been", "not", "but", "can",
        "all", "any", "do", "if", "so", "up", "out", "who", "its",
        "him", "his", "her", "she", "he", "us", "me", "my", "no",
        "which", "more", "also", "than", "into", "about", "other",
        "what", "would", "there", "when", "one", "how", "each"
    }

    jd_keywords = jd_words - stop_words
    missing     = sorted([kw for kw in jd_keywords if kw not in resume_words])

    return missing