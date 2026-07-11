# SmartHire — AI-Powered Resume Intelligence & Career Guidance System

SmartHire is an end-to-end Machine Learning-based Resume Intelligence platform that analyzes an uploaded resume and provides intelligent career insights using **Classical Machine Learning techniques**.

The system performs:

1. **Resume Category Classification** (Supervised Learning)
2. **Job Recommendation** (Content-Based Recommendation)
3. **Career Clustering** (Unsupervised Learning)
4. **Skill Gap Analysis** (Word2Vec-Based Skill Matching)

Unlike modern AI assistants, **SmartHire does not use Large Language Models (LLMs), Generative AI, or external AI APIs**. Every prediction is generated using the original Machine Learning models developed in this project.

---

# Project Structure

```text
SmartHire/
│
├── app.py              # Streamlit Web Application
│
├── notebooks/
│   ├── 02_resume_classifier.ipynb
│   ├── 03_recommender.ipynb
│   └── 04_clustering_topics.ipynb
│   └── 05_skills_gap_analyzer.ipynb
├── datas/
│   ├── Cleaned_data/
│   │   ├── 02_resume_classifier_dataset.csv
│   │   ├── 03_recommender_dataset.csv
│   │   └── 04_Clustering_dataset.csv
│   │   └── skills_gap_corpus.csv
│   └── old_data/
│       ├── Resume_25.csv
│       ├── naukri.csv
│       └── LinkedIn_dataset.csv
│
├── models/
│   ├── 02_resume_classification_model.pkl
│   ├── 02_resume_classifier_tfidf_vectorizer.pkl
│   ├── 03_recommender_tfidf_vectorizer.pkl
│   ├── 04_KMeans_model.pkl
│   └── 04_skills_word2vec.model
│── src/
│   ├── config.py
│   ├── data/                   # load_data.py, preprocess.py
│   ├── features/                # text_features.py, match_features.py
│   ├── models/                  # classifier.py, recommender.py, fit_predictor.py
│   ├── parsing/                  # resume_parser.py (PDF/DOCX/TXT extraction)
│   └── evaluate.py              # shared evaluation metrics
├── requirements.txt
│
└── README.md
```

---

# Machine Learning Pipeline

```
Resume Upload
      │
      ▼
Resume Parsing
      │
      ▼
Text Preprocessing
      │
      ▼
Feature Extraction (TF-IDF)
      │
      ├───────────────► Resume Category Classification
      │
      ├───────────────► Job Recommendation Engine
      │
      ├───────────────► Career Clustering
      │
      └───────────────► Skill Gap Analysis
                      │
                      ▼
            SmartHire Dashboard
```

---

# Machine Learning Models

| Module | Learning Type | Algorithm / Technique | Purpose |
|----------|---------------|----------------------|---------|
| Resume Category Classification | Supervised | TF-IDF + Logistic Regression | Predicts the candidate's job domain |
| Job Recommendation | Unsupervised | TF-IDF + Cosine Similarity | Recommends the most relevant jobs |
| Career Clustering | Unsupervised | K-Means Clustering | Groups related job families |
| Skill Gap Analysis | Unsupervised | Word2Vec | Identifies missing skills required for target jobs |

---

# Setup

## Clone Repository

```bash
git clone https://github.com/<your-username>/SmartHire.git

cd SmartHire
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Streamlit Application

```bash
streamlit run app/streamlit_app.py
```

---

# Model Performance

| Model | Algorithm | Evaluation Metric | Performance |
|--------|-----------|------------------|-------------|
| Resume Category Classifier | Logistic Regression | Accuracy | XX.XX % |
| Resume Category Classifier | Logistic Regression | Precision | XX.XX % |
| Resume Category Classifier | Logistic Regression | Recall | XX.XX % |
| Resume Category Classifier | Logistic Regression | F1-Score | XX.XX % |
| Job Recommendation | TF-IDF + Cosine Similarity | Precision@10 | XX.XX |
| Career Clustering | K-Means | Silhouette Score | XX.XX |
| Skill Gap Analysis | Word2Vec | Skill Matching Accuracy | XX.XX % |

> Replace the values above with the final evaluation results obtained from your notebooks.

---

# Technologies Used

### Programming Language

- Python

### Machine Learning

- Scikit-learn
- TF-IDF
- Logistic Regression
- K-Means Clustering
- Cosine Similarity
- Word2Vec

### Data Processing

- Pandas
- NumPy
- Regular Expressions

### Resume Parsing

- PyMuPDF
- python-docx

### Visualization

- Matplotlib
- Plotly

### Web Framework

- Streamlit

---

# Datasets

| Dataset | Purpose |
|----------|---------|
| Resume Dataset | Resume Category Classification |
| Naukri Job Dataset | Job Recommendation |
| LinkedIn Job Dataset | Career Clustering & Skill Gap Analysis |

---

# Project Outputs

After uploading a resume, SmartHire generates:

- Resume Summary
- Predicted Resume Category
- Top Job Recommendations
- Similarity Scores
- Career Cluster
- Skill Gap Report
- Recommended Skills

---

# Current Limitations

- Fit Prediction module has not been implemented.
- Job recommendations depend on the quality of the available job corpus.
- Skill Gap Analysis is based on Word2Vec similarity and extracted job skills.
- Resume quality directly affects prediction accuracy.

---

# Future Enhancements

- Resume Fit Prediction
- Salary Prediction
- Resume Score Calculation
- Interview Question Recommendation
- User Authentication
- Cloud Deployment
- Admin Dashboard
- Resume History Tracking

---

# Live Demo

**Streamlit Application**

https://your-streamlit-url.streamlit.app

---

# Author

**Anand S**

B.Tech Student

Artificial Intelligence & Machine Learning

GitHub: https://github.com/<your-github>

LinkedIn: https://linkedin.com/in/<your-linkedin>

---

## License

This project is developed for educational and research purposes.

---

⭐ If you found this project useful, consider giving it a star on GitHub.
