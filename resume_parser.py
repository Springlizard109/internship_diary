import PyPDF2

def extract_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text.lower()