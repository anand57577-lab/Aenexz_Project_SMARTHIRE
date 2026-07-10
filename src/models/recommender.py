import os
import re 
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

try:
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
except Exception:
    stopwords = None
    WordNetLemmatizer = None

from src.config import RECOMMENDER_TFIDF, RECOMMENDER_DATASET


class _SimpleLemmatizer:
    def lemmatize(self, word):
        return word


try:
    STOP_WORDS = set(stopwords.words("english")) if stopwords else set()
except LookupError:
    STOP_WORDS = set()

LEMMATIZER = WordNetLemmatizer() if WordNetLemmatizer else _SimpleLemmatizer()


class JobRecommender:
    def __init__(self):

        self.lemmatizer = LEMMATIZER

        self.stop_words = STOP_WORDS

        self.vectorizer = joblib.load(RECOMMENDER_TFIDF)

        self.Jobs = pd.read_csv(RECOMMENDER_DATASET)

        self.job_vectors = self.vectorizer.transform(self.Jobs["Job_Text"])

    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r'https?\S+|www\S+', ' ', text)
        text = re.sub(r'\s+@\s+', ' ', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        words = text.split()
        words = [self.lemmatizer.lemmatize(w) for w in words if w not in self.stop_words]
        return ' '.join(words)
    
   


    def vectorize_resume(self, resume_text):
        if isinstance(resume_text, (list, tuple)):
            resume_text = " ".join(map(str, resume_text))

        cleaned_resume = self.clean_text(resume_text)
        vectorized_resume = self.vectorizer.transform([cleaned_resume])
        return vectorized_resume

    def recommend(self, resume_text,top_n = 10):
        resume_vector = self.vectorize_resume([resume_text])
        similarity_scores = cosine_similarity(
            resume_vector,
            self.job_vectors
        ).flatten()

        recommendations = self.Jobs.copy()
        recommendations["similarity"] = similarity_scores
        recommendations = recommendations.sort_values(
            by="similarity",
            ascending=False
        )

        return recommendations.head(top_n).reset_index(drop=True)

        
        
    
