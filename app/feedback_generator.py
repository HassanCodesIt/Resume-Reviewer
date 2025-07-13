import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')

client = InferenceClient(
    provider="novita",
    api_key=HF_TOKEN,
)

PROMPT_TEMPLATE = '''Act as a professional resume reviewer. Given the following resume and job description:

Resume:
{resume_text}

Job Description:
{job_text}

1. **AI Suggestions**: Provide detailed, categorized suggestions in these areas:
   - Content Structure & Section Coverage
   - Grammar, Tone & Clarity
   - Role Relevance & Personalization
   - Impact & Achievement Highlighting
   - Formatting & Readability
For each, give specific, actionable feedback with examples.

2. **Summary**: Write a concise executive summary including:
   - Overall impression and readiness for the job
   - 2–3 key strengths
   - 2–3 major areas for improvement
   - (Optional) ATS/readability score and comments

Format your output with clear headings and bullet points for each section.
'''

def generate_feedback(resume_text, job_text):
    prompt = PROMPT_TEMPLATE.format(resume_text=resume_text, job_text=job_text)
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages=[{"role": "user", "content": prompt}]
        )
        response = completion.choices[0].message.content if hasattr(completion.choices[0].message, 'content') else str(completion.choices[0].message)
    except Exception as e:
        if '401' in str(e) or 'Unauthorized' in str(e):
            response = "[ERROR] Invalid Hugging Face credentials or model access. Please check your HF_TOKEN and model permissions."
        else:
            response = f"[ERROR] LLM call failed: {e}"
    # Parse output: try to split by headings
    ai_suggestions = ''
    summary = ''
    lines = response.split('\n')
    current = None
    buffer = []
    for line in lines:
        if 'AI Suggestions' in line:
            if current:
                if current == 'AI Suggestions':
                    ai_suggestions = '\n'.join(buffer).strip()
                elif current == 'Summary':
                    summary = '\n'.join(buffer).strip()
            current = 'AI Suggestions'
            buffer = []
        elif 'Summary' in line:
            if current == 'AI Suggestions':
                ai_suggestions = '\n'.join(buffer).strip()
            buffer = []
            current = 'Summary'
        else:
            buffer.append(line)
    if current == 'Summary':
        summary = '\n'.join(buffer).strip()
    elif current == 'AI Suggestions':
        ai_suggestions = '\n'.join(buffer).strip()
    # Fallback if parsing fails
    if not ai_suggestions:
        ai_suggestions = response
    if not summary:
        summary = response
    # Return as a single suggestion (for now, can be split further if needed)
    return {
        'improvements': [ai_suggestions],
        'fit_score': 0,
        'summary': summary,
        'raw_output': response
    } 