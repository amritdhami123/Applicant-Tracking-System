import io
import pdfplumber

def extract_text_from_pdf(uploaded_file):
    """Extracts text safely from a Streamlit uploaded PDF file."""
    text = ""
    try:
        # 1. CRITICAL FIX: Reset the file pointer to the beginning
        uploaded_file.seek(0)
        
        # 2. Read into a pure byte stream so pdfplumber doesn't crash
        file_bytes = uploaded_file.read()
        pdf_stream = io.BytesIO(file_bytes)
        
        with pdfplumber.open(pdf_stream) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    
    return text.strip()
