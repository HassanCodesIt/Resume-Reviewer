from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load models globally for efficiency
try:
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
    nlp = spacy.load('en_core_web_sm')
    logger.info("Successfully loaded SBERT and spaCy models")
except Exception as e:
    logger.error(f"Error loading models: {e}")
    # Try to download spaCy model if not available
    try:
        import subprocess
        subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'], check=True)
        nlp = spacy.load('en_core_web_sm')
        logger.info("Successfully downloaded and loaded spaCy model")
    except Exception as download_error:
        logger.error(f"Failed to download spaCy model: {download_error}")
        nlp = None
    
    sbert_model = None if 'sbert_model' not in locals() else sbert_model

# Curated list of common AI/ML/Data/Software skills
CURATED_SKILLS = set([
    'python', 'java', 'c++', 'c#', 'sql', 'pandas', 'numpy', 'scikit-learn', 'sklearn', 'tensorflow', 'pytorch', 'keras', 'matplotlib', 'seaborn', 'data analysis', 'data engineering', 'data science', 'machine learning', 'deep learning', 'nlp', 'natural language processing', 'computer vision', 'opencv', 'mlflow', 'dvc', 'kubeflow', 'hugging face', 'transformers', 'llm', 'llms', 'mistral', 'llama', 'vector databases', 'faiss', 'chromadb', 'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'git', 'github', 'ci/cd', 'flask', 'fastapi', 'rest apis', 'api', 'web scraping', 'big data', 'cloud', 'mlops', 'data structures', 'algorithms', 'linear algebra', 'probability', 'statistics', 'model tuning', 'hyperparameter optimization', 'model accuracy', 'model evaluation', 'model deployment', 'production', 'experimentation', 'team collaboration', 'team', 'collaboration', 'communication', 'leadership', 'research', 'design', 'build', 'training', 'testing', 'deployment', 'data ingestion', 'data processing', 'data pipelines', 'end-to-end', 'llm fine-tuning', 'rag', 'retrieval augmented generation', 'chatbot', 'intelligent automation', 'intelligent assistants', 'ai', 'ml', 'data', 'ml solutions', 'ai/ml', 'ai/ml engineer', 'data scientist', 'data engineer', 'ml engineer', 'ai engineer', 'ml researcher', 'data analyst', 'ml developer', 'ai developer', 'ml architect', 'ai architect', 'ml specialist', 'ai specialist', 'ml consultant', 'ai consultant', 'ml lead', 'ai lead', 'ml manager', 'ai manager', 'ml director', 'ai director', 'ml head', 'ai head', 'ml principal', 'ai principal', 'ml fellow', 'ai fellow', 'ml expert', 'ai expert', 'ml guru', 'ai guru', 'ml ninja', 'ai ninja', 'ml wizard', 'ai wizard', 'ml rockstar', 'ai rockstar', 'ml superstar', 'ai superstar', 'ml champion', 'ai champion', 'ml hero', 'ai hero', 'ml legend', 'ai legend', 'ml master', 'ai master', 'ml sensei', 'ai sensei', 'ml samurai', 'ai samurai', 'ml jedi', 'ai jedi', 'ml sith', 'ai sith', 'ml padawan', 'ai padawan', 'ml apprentice', 'ai apprentice', 'ml intern', 'ai intern', 'ml trainee', 'ai trainee', 'ml student', 'ai student', 'ml scholar', 'ai scholar', 'ml enthusiast', 'ai enthusiast', 'ml hobbyist', 'ai hobbyist', 'ml tinkerer', 'ai tinkerer', 'ml builder', 'ai builder', 'ml creator', 'ai creator', 'ml innovator', 'ai innovator', 'ml pioneer', 'ai pioneer', 'ml visionary', 'ai visionary', 'ml evangelist', 'ai evangelist', 'ml advocate', 'ai advocate', 'ml ambassador', 'ai ambassador', 'ml influencer', 'ai influencer', 'ml speaker', 'ai speaker', 'ml author', 'ai author', 'ml blogger', 'ai blogger', 'ml podcaster', 'ai podcaster', 'ml youtuber', 'ai youtuber', 'ml streamer', 'ai streamer', 'ml educator', 'ai educator', 'ml teacher', 'ai teacher', 'ml mentor', 'ai mentor', 'ml coach', 'ai coach', 'ml trainer', 'ai trainer', 'ml consultant', 'ai consultant', 'ml advisor', 'ai advisor', 'ml analyst', 'ai analyst', 'ml strategist', 'ai strategist', 'ml planner', 'ai planner', 'ml organizer', 'ai organizer', 'ml coordinator', 'ai coordinator', 'ml administrator', 'ai administrator', 'ml operator', 'ai operator', 'ml technician', 'ai technician', 'ml technologist', 'ai technologist'
])

# Lowercase for matching
CURATED_SKILLS = set(s.lower() for s in CURATED_SKILLS)

def get_embeddings(text):
    """Get embeddings with error handling and fallback"""
    if sbert_model is None:
        logger.error("SBERT model not loaded, returning fallback embedding")
        # Return a simple fallback embedding
        return np.zeros(384)  # Default size for all-MiniLM-L6-v2
    
    try:
        return sbert_model.encode([text])[0]
    except Exception as e:
        logger.error(f"Error getting embeddings: {e}")
        # Return a simple fallback embedding
        return np.zeros(384)

def compute_cosine_similarity(emb1, emb2):
    """Compute cosine similarity with error handling"""
    try:
        # Use numpy for manual computation as fallback
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    except Exception as e:
        logger.error(f"Error computing cosine similarity: {e}")
        return 0.5  # Return neutral score as fallback

def extract_skills(text, skill_list=None):
    """Extract skills with error handling"""
    if nlp is None:
        logger.error("spaCy model not loaded, returning empty skills list")
        return []
    
    try:
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
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        return []

def top_missing_skills(jd_skills, resume_skills, limit=10):
    """Get top missing skills with error handling"""
    try:
        missing = list(jd_skills - resume_skills)
        return missing[:limit]
    except Exception as e:
        logger.error(f"Error computing missing skills: {e}")
        return [] 