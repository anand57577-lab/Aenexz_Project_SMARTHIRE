import os 
import re 
import joblib

try:
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
except Exception:
    stopwords = None
    WordNetLemmatizer = None

from src.config import RESUME_TFIDF,RESUME_CLASSIFIER_MODEL


class _SimpleLemmatizer:
    def lemmatize(self, word):
        return word


try:
    STOP_WORDS = set(stopwords.words("english")) if stopwords else set()
except LookupError:
    STOP_WORDS = set()

LEMMATIZER = WordNetLemmatizer() if WordNetLemmatizer else _SimpleLemmatizer()


class Classifier:
    def __init__(self):

        self.lemmatizer = LEMMATIZER

        self.stop_words = STOP_WORDS

        self.model = joblib.load(RESUME_CLASSIFIER_MODEL)

        self.vectorizer = joblib.load(RESUME_TFIDF)

    def clean_text(self, text):

        text = str(text).lower()
        text = re.sub(r'https?\S+|www\S+', ' ', text)
        text = re.sub(r'\s+@\s+', ' ', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        word = text.split()
        word = [self.lemmatizer.lemmatize(w) for w in word if w not in self.stop_words]

        return ' '.join(word)
    
    def vectorize(self, resume_text):
        cleaned_resume = self.clean_text(resume_text)
        vectorized_resume = self.vectorizer.transform([cleaned_resume])
        return vectorized_resume
    
    def predict_category(self, resume_text):
        vector = self.vectorize(resume_text)
        prediction = self.model.predict(vector)[0]
        return prediction
    
    def predict(self, resume_text):
        category = self.predict_category(resume_text)

        return { 
            "resume_category": category
        }

