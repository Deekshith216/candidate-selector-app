import streamlit as st
import pandas as pd
import glob

st.set_page_config(page_title="Smart Candidate Selector", layout="wide")
st.title("📋 Smart Multi-Role Candidate Selector")

# Get CSV files
csv_files = glob.glob("data/*.csv")
if not csv_files:
    st.warning("⚠️ No CSV files found in data/ folder.")
    st.stop()

selected_file = st.sidebar.selectbox("Select CSV file", options=csv_files)
df = pd.read_csv(selected_file)
st.write("📂 Loaded file:", selected_file)
st.write("📝 Columns:", df.columns.tolist())

# -----------------------------------
# Dynamically normalize the columns
# -----------------------------------

# Name
if "name" not in df.columns:
    name_col = next((c for c in df.columns if "Full Name" in c), None)
    df["name"] = df[name_col] if name_col else "N/A"

# Education
if "education" not in df.columns:
    edu_col = next((c for c in df.columns if "Educational Qualification" in c), "")
    branch_col = next((c for c in df.columns if "Branch / Stream" in c), "")
    df["education"] = df.get(edu_col, "") + " " + df.get(branch_col, "")

# Experience
if "experience" not in df.columns:
    exp_col = next((c for c in df.columns if "Relevant experience" in c), "")
    df["experience"] = df.get(exp_col, 0).replace({"Fresher": 0, "No": 0}).fillna(0)
    df["experience"] = df["experience"].apply(lambda x: float(x) if str(x).replace(".","",1).isdigit() else 0)

# Skills (fallback: default set)
if "skills" not in df.columns:
    df["skills"] = "Docker, Kubernetes, CI/CD"

# -----------------------------------
# Scoring
# -----------------------------------
def score(row):
    skills = str(row.get("skills", "")).split(",")
    experience = float(row.get("experience", 0))
    education = str(row.get("education", ""))
    score = 0
    score += len(skills) * 2
    score += experience * 3
    if "BTech" in education or "BE" in education:
        score += 5
    elif "MTech" in education or "ME" in education:
        score += 4
    elif "MCA" in education or "MSc" in education:
        score += 3
    return score

df["score"] = df.apply(score, axis=1)
df_sorted = df.sort_values(by="score", ascending=False).head(10)

# -----------------------------------
# Display cards
# -----------------------------------
st.subheader(f"Top 10 Candidates from {selected_file}")

cols = st.columns(2)
for idx, (_, row) in enumerate(df_sorted.iterrows()):
    with cols[idx % 2]:
        st.markdown(f"""
            <div style="border: 1px solid #ccc; border-radius: 10px; padding: 16px; margin-bottom: 16px;">
                <h4>{row.get("name", "N/A")}</h4>
                <p><b>Skills:</b> {row.get("skills", "N/A")}</p>
                <p><b>Experience:</b> {row.get("experience", "N/A")} years</p>
                <p><b>Education:</b> {row.get("education", "N/A")}</p>
                <p><b>Score:</b> {row.get("score", 0)}</p>
            </div>
        """, unsafe_allow_html=True)
