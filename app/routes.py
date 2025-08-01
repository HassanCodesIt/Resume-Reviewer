import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session, send_file, make_response
from markupsafe import Markup
from werkzeug.utils import secure_filename
from .resume_utils import get_text_from_input, extract_text_from_pdf, check_ats_compatibility
from .similarity_engine import get_embeddings, compute_cosine_similarity, extract_skills, top_missing_skills
from .feedback_generator import generate_feedback

try:
    import markdown as md_lib
    def markdown_to_html(text):
        return Markup(md_lib.markdown(text))
except ImportError:
    def markdown_to_html(text):
        html = text.replace('**', '<b>').replace('* ', '<li>').replace('\n', '<br>')
        html = html.replace('<b>', '</b>', 1) if html.count('<b>') % 2 == 1 else html
        return Markup(html)

main = Blueprint('main', __name__)

def save_text_to_tempfile(text, upload_folder, prefix):
    filename = f"{prefix}_{uuid.uuid4().hex}.txt"
    file_path = os.path.join(upload_folder, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"[DEBUG] Saved text to temp file: {file_path}")
    return file_path

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        upload_folder = os.path.join(current_app.root_path, '..', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        print(f"[DEBUG] Upload folder: {upload_folder}")
        resume_file = request.files.get('resume_file')
        resume_text_input = request.form.get('resume_text')
        resume_text, resume_path = get_text_from_input(resume_file, resume_text_input, upload_folder, 'resume')
        if not resume_path and resume_text:
            resume_path = save_text_to_tempfile(resume_text, upload_folder, 'resume')
        print(f"[DEBUG] Resume path: {resume_path}")
        job_file = request.files.get('job_file')
        job_text_input = request.form.get('job_text')
        job_text, job_path = get_text_from_input(job_file, job_text_input, upload_folder, 'jd')
        if not job_path and job_text:
            job_path = save_text_to_tempfile(job_text, upload_folder, 'jd')
        print(f"[DEBUG] JD path: {job_path}")
        if not resume_path or not job_path:
            flash('Please provide both a resume and a job description (file or text).', 'danger')
            return render_template('index.html')
        session['resume_path'] = resume_path
        session['job_path'] = job_path
        print(f"[DEBUG] Session resume_path: {session.get('resume_path')}")
        print(f"[DEBUG] Session job_path: {session.get('job_path')}")
        return redirect(url_for('main.results'))
    return render_template('index.html')

@main.route('/results', methods=['GET'])
def results():
    resume_path = session.get('resume_path')
    job_path = session.get('job_path')
    print(f"[DEBUG] Results - resume_path: {resume_path}")
    print(f"[DEBUG] Results - job_path: {job_path}")
    if not resume_path or not job_path:
        flash('Session expired or invalid. Please re-submit your documents.', 'danger')
        return redirect(url_for('main.index'))
    try:
        print(f"[DEBUG] Checking if resume file exists: {os.path.exists(resume_path)}")
        print(f"[DEBUG] Checking if JD file exists: {os.path.exists(job_path)}")
        if resume_path.lower().endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_path)
        else:
            with open(resume_path, 'r', encoding='utf-8') as f:
                resume_text = f.read()
        if job_path.lower().endswith('.pdf'):
            job_text = extract_text_from_pdf(job_path)
        else:
            with open(job_path, 'r', encoding='utf-8') as f:
                job_text = f.read()
    except Exception as e:
        print(f"[DEBUG] Exception reading files: {e}")
        flash('Could not read uploaded files. Please try again.', 'danger')
        return redirect(url_for('main.index'))
    try:
        resume_emb = get_embeddings(resume_text)
        job_emb = get_embeddings(job_text)
        fit_score = int(compute_cosine_similarity(resume_emb, job_emb) * 100)
        fit_score = max(0, min(100, fit_score))
    except Exception as e:
        print(f"[DEBUG] Error in similarity computation: {e}")
        fit_score = 50  # Default neutral score
        
    try:
        jd_skills = set(extract_skills(job_text))
        resume_skills = set(extract_skills(resume_text))
        matched_skills = list(resume_skills & jd_skills)
        missing_skills = top_missing_skills(jd_skills, resume_skills, limit=10)
    except Exception as e:
        print(f"[DEBUG] Error in skills extraction: {e}")
        matched_skills = []
        missing_skills = []
        
    try:
        feedback = generate_feedback(resume_text, job_text)
    except Exception as e:
        print(f"[DEBUG] Error in feedback generation: {e}")
        feedback = {'improvements': ['Unable to generate feedback due to technical issues.'], 'summary': 'Analysis completed with limited functionality.'}
    def fallback_list(val, raw):
        if not val or val == ['**'] or all(x.strip() in ('', '**') for x in val):
            return [raw] if raw else ['[No data]']
        return val
    def fallback_str(val, raw):
        if not val or val.strip() in ('', '**'):
            return raw or '[No data]'
        return val
    improvements = fallback_list(feedback.get('improvements', []), feedback.get('raw_output', ''))
    summary = fallback_str(feedback.get('summary', ''), feedback.get('raw_output', ''))
    improvements_html = [markdown_to_html(s) for s in improvements]
    summary_html = markdown_to_html(summary)
    ats_report = check_ats_compatibility(resume_text, job_text, matched_skills)
    try:
        os.remove(resume_path)
        os.remove(job_path)
        print(f"[DEBUG] Temp files removed.")
    except Exception as e:
        print(f"[DEBUG] Exception removing temp files: {e}")
        pass
    session.pop('resume_path', None)
    session.pop('job_path', None)
    # Store results in session for PDF download
    session['last_results'] = {
        'fit_score': fit_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'improvements': improvements,
        'summary': summary,
        'ats_report': ats_report
    }
    return render_template('results.html',
        fit_score=fit_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        improvements=improvements_html,
        summary=summary_html,
        ats_report=ats_report
    )

@main.route('/download_report')
def download_report():
    import pdfkit
    results = session.get('last_results')
    if not results:
        flash('No report available. Please analyze a resume first.', 'danger')
        return redirect(url_for('main.index'))
    # Render a special template for PDF (no JS, print-friendly)
    rendered = render_template('report_pdf.html', **results)
    try:
        # Generate PDF
        pdf = pdfkit.from_string(rendered, False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=resume_report.pdf'
        return response
    except Exception as e:
        flash('PDF export is currently unavailable. Please install wkhtmltopdf or contact support if you need this feature.', 'danger')
        return redirect(url_for('main.results'))

@main.route('/health')
def health_check():
    """Health check endpoint for deployment monitoring"""
    return {'status': 'healthy', 'service': 'resume-reviewer'}, 200

@main.route('/test')
def test_endpoint():
    """Simple test endpoint to verify deployment"""
    return {'message': 'Resume Reviewer is running!', 'status': 'ok'}, 200 