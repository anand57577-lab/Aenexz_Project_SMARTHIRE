import os

# PROJECT PATHS
 

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)

 
# FOLDERS
 

MODEL_DIR = os.path.join(PROJECT_ROOT, "models")

DATA_DIR = os.path.join(PROJECT_ROOT, "datas")

CLEAN_DATA_DIR = os.path.join(DATA_DIR, "processed_data")

RAW_DATA_DIR = os.path.join(DATA_DIR, "raw_data")

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")

ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")

REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")

 
# MODEL FILES
 

RESUME_CLASSIFIER_MODEL = os.path.join(
    MODEL_DIR,
    "02_resume_classification_model.pkl"
)

RESUME_TFIDF = os.path.join(
    MODEL_DIR,
    "02_resume_classifier_tfidf_vectorizer.pkl"
)

RECOMMENDER_TFIDF = os.path.join(
    MODEL_DIR,
    "03_recommender_tfidf_vectorizer.pkl"
)

CLUSTER_TFIDF = os.path.join(MODEL_DIR,"04_clustering_tfidf.pkl")

KMEANS_MODEL = os.path.join(
    MODEL_DIR,
    "04_Kmeans_model.pkl"
)

WORD2VEC_MODEL = os.path.join(
    MODEL_DIR,
    "word2vec.model"
)

FIT_PREDICTOR_MODEL = os.path.join(
    MODEL_DIR,
    "05_fit_predictor_model.pkl"
)

CLUSTER_MAPPING = os.path.join(
    MODEL_DIR,
    "clusters_maping.json"
)


SKILLS_KEYWORDS = os.path.join(
    MODEL_DIR,
    "skills_word_dictonary_analysis.pkl"
)

 
# DATASETS
 

RESUME_DATASET = os.path.join(
    CLEAN_DATA_DIR,
    "02_resume_classifer_dataset.csv"
)

RECOMMENDER_DATASET = os.path.join(
    CLEAN_DATA_DIR,
    "03_recommender_dataset.csv"
)

CLUSTER_DATASET = os.path.join(
    CLEAN_DATA_DIR,
    "04_clusters_data.csv"
)

MASTER_JOBS = os.path.join(
    CLEAN_DATA_DIR,
    "skills_gap_corpus.csv"
)


 

TOP_RECOMMENDATIONS = 10

SIMILARITY_THRESHOLD = 0.50

 
# WORD2VEC SETTINGS
 

WORD2VEC_SIMILARITY_THRESHOLD = 0.70

TOP_CLUSTER_SKILLS = 20

 
# FIT PREDICTION SETTINGS
 

FIT_THRESHOLD = 70

HIGHLY_RECOMMENDED = 85

MODERATE_RECOMMENDED = 60

 
# FILE UPLOAD SETTINGS
 

ALLOWED_FILE_TYPES = [
    ".pdf",
    ".docx"
]

MAX_FILE_SIZE_MB = 10

 
# RANDOM SEED
 

RANDOM_STATE = 42


# STREAMLIT SETTINGS


PAGE_TITLE = "SmartHire AI"

PAGE_ICON = "🤖"

LAYOUT = "wide"