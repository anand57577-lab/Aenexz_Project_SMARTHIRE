

import os

import streamlit as st

from src.parsing.resume_parser import ResumeParser
from src.models.classifier import Classifier
from src.models.recommender import JobRecommender

from src.models.skill_gap import SkillGapAnalyzer


@st.cache_resource(show_spinner=False)
def load_ai_components():
    parser = ResumeParser()
    classifier = Classifier()
    recommender = JobRecommender()
    skill_gap = SkillGapAnalyzer()
    return parser, classifier, recommender, skill_gap


# Streamlit Page Configuration

st.set_page_config(
    page_title="SmartHire AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


  
# Create Upload Folder
  

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


  
# Sidebar
  

with st.sidebar:

    st.title("🤖 SmartHire AI")

    st.markdown("---")

    st.write("### AI Modules")

    st.success("✅ Resume Parser")

    st.info(" ✅ Resume Classification")

    st.info(" ✅ Job Recommendation")

    st.info("✅ Skill Gap Analysis")

    st.info("✅ Fit Prediction")

    st.markdown("---")

    st.caption("Version 1.0")


  
# Header
  

with st.spinner("Preparing AI models..."):
    load_ai_components()

st.title("🤖 SmartHire AI")

st.subheader(
    "AI-Powered Resume Screening & Job Recommendation System"
)

st.markdown("---")


  
# Resume Upload Section
  

st.header("📄 Upload Resume")

uploaded_file = st.file_uploader(

    "Choose a Resume",

    type=["pdf", "docx"]

)


  
# Parse Resume
  

if uploaded_file is not None:

    file_path = os.path.join(

        UPLOAD_FOLDER,

        uploaded_file.name

    )

    with open(file_path, "wb") as file:

        file.write(uploaded_file.getbuffer())

    st.success("Resume Uploaded Successfully.")

    with st.spinner("Loading AI models..."):
        parser, classifier, recommender, skill_gap = load_ai_components()

    try:

        resume_text = parser.parse(file_path)
        st.session_state["resume_text"] = resume_text

        result = classifier.predict(resume_text)
        st.session_state["resume_prediction"] = result


        resume_category = result["resume_category"]
        recommendations = recommender.recommend(
            resume_text,
            top_n=10
        )

        st.session_state["recommended_jobs"] = recommendations

        
    # Candidate Profile
    

        st.markdown("---")

        st.header("👤 Candidate Profile")

        col1, col2 = st.columns(2)

        with col1:

            st.success(f"**Resume Category**\n\n{resume_category}")

        with col2:

            st.metric(
                label="Recommended Jobs",
                value=len(recommendations)
            )

    
     # Recommended Jobs


        st.markdown("---")

        st.header("💼 Top Recommended Jobs")

        recommendations = recommendations.copy()

        recommendations.insert(
            0,
            "Rank",
            range(1, len(recommendations) + 1)

            
        )
    
        recommendations["Similarity"] = (
            recommendations["similarity"] * 100
        ).round(2)

        
        display_columns = []

        possible_columns = [
            "Rank",
            "title",
            "companyName",
            "location",
            "experience",
            "Similarity",

            
        ]

        for col in possible_columns:

            if col in recommendations.columns:

                display_columns.append(col)

        display_df = recommendations[display_columns]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


    ## Job search 

        st.markdown("---")

        st.header("🔍 Search Career")

        titles = skill_gap.search_jobs()

        

        selected_job = st.selectbox(

            "Search Carreer Domain",

            options= titles

        )

        st.session_state["selected_job"] = selected_job

        job_details = skill_gap.get_job_details(selected_job)
        st.session_state["career"] = job_details

        required_skills = skill_gap.get_required_skills(
                selected_job
        )
        
       
       
        if st.button("🚀 Analyze Skill Gap"):

            with st.spinner("Analyzing Resume Skills..."):

                report = skill_gap.analyze(
                    resume_text,
                    selected_job
                )

            st.session_state["report"] = report

            st.success("Skill Gap Analysis Completed Successfully!")

        # Load report from session state if available
        report = st.session_state.get("report")

        if report is not None:

            st.markdown("---")

            st.header("📊 Skill Gap Analysis Report")

            score = report["match_score"]

            st.metric(
                "🎯 Overall Match Score",
                f"{score}%"
            )

            st.progress(score / 100)


            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Required Skills",
                    len(report["required_skills"])
                )

            with col2:

                st.metric(
                    "Matched",
                    len(report["matched_skills"])
                )

            with col3:

                st.metric(
                    "Semantic Match",
                    len(report["related_skills"])
                )

            with col4:

                st.metric(
                    "Missing",
                    len(report["missing_skills"])
                )
         
            st.markdown("---")
            st.header("👤 Skills Extracted from Resume")

            candidate_skills = report["candidate_skills"]

            if candidate_skills:

                cols = st.columns(4)

                for i, skill in enumerate(candidate_skills):

                    with cols[i % 4]:
                        st.success(skill)

            else:
                st.warning("No skills found in the resume.")    

            st.markdown("---")

            st.subheader("✅ Matched Skills")

            if report["matched_skills"]:

                cols = st.columns(4)

                for i, skill in enumerate(report["matched_skills"]):

                    with cols[i % 4]:

                        st.success(skill)

            else:

                st.warning("No exact matched skills found.")

            st.markdown("---")


            st.subheader("🧠 Semantic Matches")

            if report["related_skills"]:

                import pandas as pd

                semantic_df = pd.DataFrame(
                    report["related_skills"]
                )

                st.dataframe(
                    semantic_df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info("No semantic matches found.")


            st.markdown("---")

            st.subheader("❌ Missing Skills")

            if report["missing_skills"]:

                cols = st.columns(4)

                for i, skill in enumerate(report["missing_skills"]):

                    with cols[i % 4]:

                        st.error(skill)

            else:

                st.success("No missing skills.")   


            st.markdown("---")

            st.subheader("👤 Skills Found in Resume")

            cols = st.columns(4)

            for i, skill in enumerate(report["candidate_skills"]):

                with cols[i % 4]:

                    st.info(skill)


            st.markdown("---")

            st.subheader("🎯 Required Skills")

            cols = st.columns(4)

            for i, skill in enumerate(report["required_skills"]):

                with cols[i % 4]:

                    st.warning(skill)


            

        else:

            st.info("Click '🚀 Analyze Skill Gap' to run the analysis and view the report.")

    except Exception as error:

        st.error(f"Error : {error}")