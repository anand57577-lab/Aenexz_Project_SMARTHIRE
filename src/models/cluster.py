# import os
# import re
# import joblib
# import pandas as pd
# import json
# import nltk
# import ast
# nltk.download("stopwords")
# nltk.download("wordnet")
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from src.config import MASTER_JOBS, CLUSTER_MAPPING, CLUSTER_TFIDF, KMEANS_MODEL

# class ClusterSearch:

#     def __init__(self):
#         self.jobs = pd.read_csv(MASTER_JOBS)
#         self.jobs = self.jobs.fillna("")

#     def search_jobs(self):

#         titles = (
#             self.jobs["title"]
#             .drop_duplicates()
#             .sort_values()
#             .tolist()
#         )

#         return titles
    
#     def get_job_details(self, job_title):
#         job = self.jobs[self.jobs["title"] == job_title]

#         if job.empty:
#             return None 
        
#         return job.iloc[0]

   

#     def get_top20_skills(self, job_title):
#         """
#         Returns the Top 20 cluster skills for the selected job title.
#         """

#         job = self.jobs[self.jobs["title"] == job_title]

#         if job.empty:
#             return []

#         skills = job.iloc[0]["top20_skills"]

#         # If stored as a string representation of a list
#         if isinstance(skills, str):
#             try:
#                 skills = ast.literal_eval(skills)
#             except Exception:
#                 skills = [s.strip() for s in skills.split(",") if s.strip()]

#         return skills
    
    
        
#     def get_job_family(self, job_title):
#         job = self.get_job_details(job_title)

#         if job is None:
#             return None
        
#         return job["job_family"]
    
#     def get_job_cluster(self, job_title):
#         job = self.get_job_details(job_title)

#         if job is None:
#             return None
        
#         return job["cluster"]
    
#     def get_required_skills(self, job_title):
#         job = self.get_job_details(job_title)

#         if job is None:
#             return None
        
#         return job["required_skills"]
    
