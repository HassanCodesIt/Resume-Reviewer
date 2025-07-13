import os
from pdfminer.high_level import extract_text as pdf_extract_text
import re

SECTION_HEADERS = [
    'experience', 'education', 'skills', 'projects', 'summary', 'contact', 'certifications', 'work history', 'profile', 'objective', 'achievements', 'publications', 'languages', 'interests', 'references'
]

ATS_CRITERIA = [
    ('Section Headers', 'Resume should have clear section headers like Experience, Education, Skills, etc.'),
    ('Keyword Density', 'Important keywords from the job description should appear in the resume.'),
    ('No Tables/Columns', 'Avoid using tables, columns, or graphics as they may confuse ATS.'),
    ('Contact Info', 'Contact information should be in the main body, not in headers/footers.'),
]

def extract_text_from_pdf(pdf_path):
    try:
        return pdf_extract_text(pdf_path)
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""

def clean_text(text):
    return ' '.join(text.strip().split())

def get_text_from_input(file_storage, text_input, upload_folder, filename_prefix):
    if file_storage and file_storage.filename:
        filename = filename_prefix + '_' + file_storage.filename
        file_path = os.path.join(upload_folder, filename)
        file_storage.save(file_path)
        if file_storage.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        return clean_text(text), file_path
    elif text_input and text_input.strip():
        return clean_text(text_input), None
    else:
        return '', None

def check_ats_compatibility(resume_text, job_text, matched_skills):
    issues = []
    suggestions = []
    # 1. Section headers
    found_headers = [h for h in SECTION_HEADERS if re.search(rf'\b{h}\b', resume_text, re.IGNORECASE)]
    if len(found_headers) < 3:
        issues.append('Section Headers')
        suggestions.append('Add more clear section headers (e.g., Experience, Education, Skills).')
    # 2. Keyword density
    if len(matched_skills) < 0.5 * len(set(job_text.lower().split())):
        issues.append('Keyword Density')
        suggestions.append('Include more relevant keywords from the job description in your resume.')
    # 3. Tables/columns (simple check for table-like patterns)
    if re.search(r'\|\t|\n\s*\n', resume_text):
        issues.append('No Tables/Columns')
        suggestions.append('Avoid using tables, columns, or tabular formatting in your resume.')
    # 4. Contact info in header/footer (simple check for email/phone at top/bottom)
    contact_pattern = r'([\w\.-]+@[\w\.-]+)|(\+?\d[\d\s\-]{7,}\d)'
    lines = resume_text.split('\n')
    if lines:
        top = ' '.join(lines[:5])
        bottom = ' '.join(lines[-5:])
        if re.search(contact_pattern, top) or re.search(contact_pattern, bottom):
            pass  # Good
        else:
            issues.append('Contact Info')
            suggestions.append('Make sure your contact info is in the main body, not just in headers/footers.')
    return {
        'criteria': ATS_CRITERIA,
        'issues': issues,
        'suggestions': suggestions
    } 