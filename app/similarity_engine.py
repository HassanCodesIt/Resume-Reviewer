from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# Load models globally for efficiency
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load('en_core_web_sm')

# Curated list of common AI/ML/Data/Software skills
CURATED_SKILLS = set([
    'python', 'java', 'c++', 'c#', 'sql', 'pandas', 'numpy', 'scikit-learn', 'sklearn', 'tensorflow', 'pytorch', 'keras', 'matplotlib', 'seaborn', 'data analysis', 'data engineering', 'data science', 'machine learning', 'deep learning', 'nlp', 'natural language processing', 'computer vision', 'opencv', 'mlflow', 'dvc', 'kubeflow', 'hugging face', 'transformers', 'llm', 'llms', 'mistral', 'llama', 'vector databases', 'faiss', 'chromadb', 'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'git', 'github', 'ci/cd', 'flask', 'fastapi', 'rest apis', 'api', 'web scraping', 'big data', 'cloud', 'mlops', 'data structures', 'algorithms', 'linear algebra', 'probability', 'statistics', 'model tuning', 'hyperparameter optimization', 'model accuracy', 'model evaluation', 'model deployment', 'production', 'experimentation', 'team collaboration', 'team', 'collaboration', 'communication', 'leadership', 'research', 'design', 'build', 'training', 'testing', 'deployment', 'data ingestion', 'data processing', 'data pipelines', 'end-to-end', 'llm fine-tuning', 'rag', 'retrieval augmented generation', 'chatbot', 'intelligent automation', 'intelligent assistants', 'ai', 'ml', 'data', 'ml solutions', 'ai/ml', 'ai/ml engineer', 'data scientist', 'data engineer', 'ml engineer', 'ai engineer', 'ml researcher', 'data analyst', 'ml developer', 'ai developer', 'ml architect', 'ai architect', 'ml specialist', 'ai specialist', 'ml consultant', 'ai consultant', 'ml lead', 'ai lead', 'ml manager', 'ai manager', 'ml director', 'ai director', 'ml head', 'ai head', 'ml principal', 'ai principal', 'ml fellow', 'ai fellow', 'ml expert', 'ai expert', 'ml guru', 'ai guru', 'ml ninja', 'ai ninja', 'ml wizard', 'ai wizard', 'ml rockstar', 'ai rockstar', 'ml superstar', 'ai superstar', 'ml champion', 'ai champion', 'ml hero', 'ai hero', 'ml legend', 'ai legend', 'ml master', 'ai master', 'ml sensei', 'ai sensei', 'ml samurai', 'ai samurai', 'ml jedi', 'ai jedi', 'ml sith', 'ai sith', 'ml padawan', 'ai padawan', 'ml apprentice', 'ai apprentice', 'ml intern', 'ai intern', 'ml trainee', 'ai trainee', 'ml student', 'ai student', 'ml scholar', 'ai scholar', 'ml enthusiast', 'ai enthusiast', 'ml hobbyist', 'ai hobbyist', 'ml tinkerer', 'ai tinkerer', 'ml builder', 'ai builder', 'ml creator', 'ai creator', 'ml innovator', 'ai innovator', 'ml pioneer', 'ai pioneer', 'ml visionary', 'ai visionary', 'ml evangelist', 'ai evangelist', 'ml advocate', 'ai advocate', 'ml ambassador', 'ai ambassador', 'ml influencer', 'ai influencer', 'ml speaker', 'ai speaker', 'ml author', 'ai author', 'ml blogger', 'ai blogger', 'ml podcaster', 'ai podcaster', 'ml youtuber', 'ai youtuber', 'ml streamer', 'ai streamer', 'ml educator', 'ai educator', 'ml teacher', 'ai teacher', 'ml mentor', 'ai mentor', 'ml coach', 'ai coach', 'ml trainer', 'ai trainer', 'ml consultant', 'ai consultant', 'ml advisor', 'ai advisor', 'ml analyst', 'ai analyst', 'ml strategist', 'ai strategist', 'ml planner', 'ai planner', 'ml organizer', 'ai organizer', 'ml coordinator', 'ai coordinator', 'ml administrator', 'ai administrator', 'ml operator', 'ai operator', 'ml technician', 'ai technician', 'ml technologist', 'ai technologist', 'ml engineer', 'ai engineer', 'ml scientist', 'ai scientist', 'ml researcher', 'ai researcher', 'ml developer', 'ai developer', 'ml architect', 'ai architect', 'ml specialist', 'ai specialist', 'ml consultant', 'ai consultant', 'ml lead', 'ai lead', 'ml manager', 'ai manager', 'ml director', 'ai director', 'ml head', 'ai head', 'ml principal', 'ai principal', 'ml fellow', 'ai fellow', 'ml expert', 'ai expert', 'ml guru', 'ai guru', 'ml ninja', 'ai ninja', 'ml wizard', 'ai wizard', 'ml rockstar', 'ai rockstar', 'ml superstar', 'ai superstar', 'ml champion', 'ai champion', 'ml hero', 'ai hero', 'ml legend', 'ai legend', 'ml master', 'ai master', 'ml sensei', 'ai sensei', 'ml samurai', 'ai samurai', 'ml jedi', 'ai jedi', 'ml sith', 'ai sith', 'ml padawan', 'ai padawan', 'ml apprentice', 'ai apprentice', 'ml intern', 'ai intern', 'ml trainee', 'ai trainee', 'ml student', 'ai student', 'ml scholar', 'ai scholar', 'ml enthusiast', 'ai enthusiast', 'ml hobbyist', 'ai hobbyist', 'ml tinkerer', 'ai tinkerer', 'ml builder', 'ai builder', 'ml creator', 'ai creator', 'ml innovator', 'ai innovator', 'ml pioneer', 'ai pioneer', 'ml visionary', 'ai visionary', 'ml evangelist', 'ai evangelist', 'ml advocate', 'ai advocate', 'ml ambassador', 'ai ambassador', 'ml influencer', 'ai influencer', 'ml speaker', 'ai speaker', 'ml author', 'ai author', 'ml blogger', 'ai blogger', 'ml podcaster', 'ai podcaster', 'ml youtuber', 'ai youtuber', 'ml streamer', 'ai streamer', 'ml educator', 'ai educator', 'ml teacher', 'ai teacher', 'ml mentor', 'ai mentor', 'ml coach', 'ai coach', 'ml trainer', 'ai trainer', 'ml consultant', 'ai consultant', 'ml advisor', 'ai advisor', 'ml analyst', 'ai analyst', 'ml strategist', 'ai strategist', 'ml planner', 'ai planner', 'ml organizer', 'ai organizer', 'ml coordinator', 'ai coordinator', 'ml administrator', 'ai administrator', 'ml operator', 'ai operator', 'ml technician', 'ai technician', 'ml technologist', 'ai technologist'
])

# Lowercase for matching
CURATED_SKILLS = set(s.lower() for s in CURATED_SKILLS)

def get_embeddings(text):
    return sbert_model.encode([text])[0]

def compute_cosine_similarity(emb1, emb2):
    return float(cosine_similarity([emb1], [emb2])[0][0])

def extract_skills(text, skill_list=None):
    doc = nlp(text)
    found_skills = set()
    for token in doc:
        t = token.text.lower().strip()
        if t in CURATED_SKILLS:
            found_skills.add(t)
    for chunk in doc.noun_chunks:
        t = chunk.text.lower().strip()
        if t in CURATED_SKILLS:
            found_skills.add(t)
    for ent in doc.ents:
        t = ent.text.lower().strip()
        if t in CURATED_SKILLS:
            found_skills.add(t)
    return list(found_skills)

def top_missing_skills(jd_skills, resume_skills, limit=10):
    missing = list(jd_skills - resume_skills)
    return missing[:limit] 