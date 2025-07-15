import streamlit as st
import pandas as pd

st.set_page_config(page_title="Candidate Selector App", layout="wide")
st.title("🚀 Top Candidate Selector App")

uploaded_file = st.file_uploader("Upload your profiles CSV", type="csv")

if uploaded_file:
    profiles = pd.read_csv(uploaded_file)
    st.success("Profiles loaded successfully!")

    # Select job role
    job_role = st.selectbox("Select Job Role", ["AWS Engineer", "Python Developer", "Data Analyst"])
    job_keywords = {
        "AWS Engineer": ["AWS", "EC2", "S3", "Lambda"],
        "Python Developer": ["Python", "Flask", "Django"],
        "Data Analyst": ["SQL", "Excel", "PowerBI"]
    }[job_role]

    # Score function
    def score(row):
        skills = row['skills'].split(",")
        skill_match = len(set(skills) & set(job_keywords))
        exp_score = min(row['experience'], 5) * 0.5
        return skill_match + exp_score

    profiles['score'] = profiles.apply(score, axis=1)
    top10 = profiles.sort_values("score", ascending=False).head(10)

    st.subheader(f"Top 10 Matched Profiles for {job_role}")

    # Show as cards
    for _, row in top10.iterrows():
        st.markdown(
            f"""
            <div style='
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            '>
                <h4>{row['name']}</h4>
                <p><strong>Skills:</strong> {row['skills']}</p>
                <p><strong>Experience:</strong> {row['experience']} years</p>
                <p><strong>Education:</strong> {row['education']}</p>
                <p><strong>Score:</strong> {round(row['score'], 2)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Download top 10
    st.download_button(
        label="Download Top 10 as CSV",
        data=top10.to_csv(index=False).encode('utf-8'),
        file_name='top_10_profiles.csv',
        mime='text/csv'
    )
else:
    st.info("Please upload a CSV file to get started.")

