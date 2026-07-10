import pandas as pd
import joblib
import ast
from src.config import MASTER_JOBS
from src.config import WORD2VEC_MODEL
from src.config import SKILLS_KEYWORDS
from collections import Counter
from itertools import chain
import re
from gensim.models import Word2Vec

class SkillGapAnalyzer:

    GENERIC_SKILLS = {
        "management",
        "analysis",
        "analytics",
        "learning",
        "github",
        "google",
        "api",
        "actions",
        "action",
        "platform",
        "systems",
        "system",
        "product",
        "products",
        "team",
        "teams",
        "support",
        "service",
        "services",
        "data",
        "science",
        "research",
        "engineering",
        "manager",
        "senior",
        "staff",
        "principal",
        "director",
        "lead",
        "developer",
        "developers",
        "time",
        "work",
        "skills",
        "skill"
    }

    def __init__(self):

        self.skill_df = pd.read_csv(
            MASTER_JOBS
        )

        self.word2vec_model = Word2Vec.load(WORD2VEC_MODEL)
    
        self.skill_df["top_skills"] = self.skill_df["top_skills"].apply(
            ast.literal_eval
        )

        self.master_skills = joblib.load(SKILLS_KEYWORDS)

    def search_jobs(self):

        return sorted(
        self.skill_df["title"].unique().tolist()
        )
    
    def get_core_role(self, title):

        row = self.skill_df[
        self.skill_df["title"] == title
        ]

        if row.empty:
            return None

        return row.iloc[0]["core_role"]
    
    def get_job_details(self, title):

        job = self.skill_df[
            self.skill_df["title"] == title
        ]

        if job.empty:
            return None

        return job.iloc[0]

   

    def clean_text(self, text):

        text = str(text).lower()

        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)

        text = re.sub(r'[^a-zA-Z0-9\s+#.]', ' ', text)

        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def _normalize_skill(self, skill):
        if pd.isna(skill):
            return None

        normalized = self.clean_text(skill)

        if not normalized:
            return None

        tokens = normalized.split()

        if len(tokens) == 1 and normalized in self.GENERIC_SKILLS:
            return None

        if len(tokens) == 1 and len(normalized) <= 2:
            return None

        if len(tokens) == 1 and normalized in {"ml", "ai", "nlp"}:
            return normalized

        if len(tokens) > 1 and normalized.split()[0] in self.GENERIC_SKILLS:
            if any(token in {"learning", "machine", "python", "deep", "neural", "vision", "nlp", "ai", "model", "models", "forecast", "risk", "analytics", "analysis"} for token in tokens):
                return normalized
            return None

        return normalized

    def _normalize_title(self, title):
        cleaned = self.clean_text(title)
        tokens = [token for token in cleaned.split() if token]
        stopwords = {"senior", "staff", "principal", "lead", "director", "sr", "jr", "ii", "iii", "manager", "engineering", "data"}
        return [token for token in tokens if token not in stopwords]

    def _title_similarity(self, title_a, title_b):
        tokens_a = set(self._normalize_title(title_a))
        tokens_b = set(self._normalize_title(title_b))

        if not tokens_a or not tokens_b:
            return 0.0

        union = tokens_a | tokens_b
        if not union:
            return 0.0

        return round(len(tokens_a & tokens_b) / len(union), 3)

    def get_required_skills(self, title, top_n=20):

        if pd.isna(title):
            return []

        title_text = str(title).strip()

        exact_matches = self.skill_df[
            self.skill_df["title"].astype(str).str.lower() == title_text.lower()
        ]

        if not exact_matches.empty:
            core_role = exact_matches.iloc[0]["core_role"]
            candidate_rows = self.skill_df[
                self.skill_df["core_role"].astype(str).str.lower() == str(core_role).lower()
            ].copy()
        else:
            candidate_rows = self.skill_df.copy()

        if candidate_rows.empty:
            return []

        candidate_rows["title_similarity"] = candidate_rows["title"].apply(
            lambda job_title: self._title_similarity(title_text, job_title)
        )

        candidate_rows = candidate_rows.sort_values(
            by=["title_similarity", "title"],
            ascending=[False, True]
        )

        if not exact_matches.empty:
            candidate_rows = candidate_rows.head(max(10, top_n))
        else:
            candidate_rows = candidate_rows.head(max(15, top_n))

        weighted_skills = Counter()

        for _, row in candidate_rows.iterrows():
            row_weight = 2.0 if str(row["title"]).lower() == title_text.lower() else 1.0
            similarity_weight = row_weight + float(row.get("title_similarity", 0.0))

            skills = row["top_skills"]
            if isinstance(skills, str):
                try:
                    skills = ast.literal_eval(skills)
                except (ValueError, SyntaxError):
                    skills = [skills]

            for skill in skills:
                normalized_skill = self._normalize_skill(skill)
                if normalized_skill:
                    weighted_skills[normalized_skill] += similarity_weight

        title_tokens = self._normalize_title(title_text)
        if title_tokens:
            for skill in self.master_skills:
                lowered_skill = self.clean_text(skill)
                if not lowered_skill:
                    continue
                skill_tokens = lowered_skill.split()
                if any(token in title_tokens for token in skill_tokens):
                    normalized_skill = self._normalize_skill(skill)
                    if normalized_skill:
                        weighted_skills[normalized_skill] += 1.0

        top_skills = [
            skill
            for skill, _ in weighted_skills.most_common(top_n)
        ]

        return top_skills
    
    def extract_resume_skills(self, resume_text):

        resume = self.clean_text(resume_text)

        found = []

        for skill in self.master_skills:

            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, resume):

                found.append(skill.lower())

        return sorted(set(found))
     
        
    def exact_skill_matching(
        self,
        candidate_skills,
        required_skills
):

        candidate = set(
            skill.lower().strip()
            for skill in candidate_skills
        )

        required = set(
            skill.lower().strip()
            for skill in required_skills
        )

        matched = sorted(
            candidate.intersection(required)
        )

        missing = sorted(
            required.difference(candidate)
        )

        return matched, missing
    

    def semantic_skill_matching(
        self,
        candidate_skills,
        missing_skills,
        threshold=0.70
):

        related_skills = []
        true_missing = []

        for required_skill in missing_skills:

            found = False

            # Convert multi-word skills to Word2Vec format
            required_token = required_skill.lower().replace(" ", "_")

            for candidate_skill in candidate_skills:

                candidate_token = candidate_skill.lower().replace(" ", "_")

                if (
                    required_token in self.word2vec_model.wv.key_to_index
                    and
                    candidate_token in self.word2vec_model.wv.key_to_index
                ):

                    similarity = self.word2vec_model.wv.similarity(
                        required_token,
                        candidate_token
                    )

                    if similarity >= threshold:

                        related_skills.append({

                            "required_skill": required_skill,

                            "candidate_skill": candidate_skill,

                            "similarity": round(similarity, 2)

                        })

                        found = True
                        break

            if not found:

                true_missing.append(required_skill)

        return related_skills, true_missing
    
    def calculate_match_score(
        self,
        matched,
        related,
        required_skills
):

        if len(required_skills) == 0:
            return 0

        score = (
            len(matched) +
            len(related)
        ) / len(required_skills)

        return round(score * 100,2)

    def generate_report(

        self,

        title,

        core_role,

        candidate_skills,

        required_skills,

        matched,

        related,

        missing,

        score

):

        return {

            "title": title,

            "core_role": core_role,

            "candidate_skills": candidate_skills,

            "required_skills": required_skills,

            "matched_skills": matched,

            "related_skills": related,

            "missing_skills": missing,

            "match_score": score

        }
    
    def analyze(self, resume_text, title):

        core_role = self.get_core_role(title)

        required_skills = self.get_required_skills(title)

        candidate_skills = self.extract_resume_skills(
            resume_text,
         
        )

        matched, missing = self.exact_skill_matching(
            candidate_skills,
            required_skills
        )

        related, true_missing = self.semantic_skill_matching(
            candidate_skills,
            missing
        )

        score = self.calculate_match_score(
            matched,
            related,
            required_skills
        )

        report = self.generate_report(

            title,

            core_role,

            candidate_skills,

            required_skills,

            matched,

            related,

            true_missing,

            score

        )

        return report