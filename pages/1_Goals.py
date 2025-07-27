import streamlit as st
import pandas as pd
import os
os.makedirs("data", exist_ok=True)

st.header("🎯 Goals: Long-Term and Short-Term")

ltg_path = "data/long_term_goals.csv"
stg_path = "data/short_term_goals.csv"

def load_csv(path, cols):
    """Load CSV safely, returning empty DataFrame with specified columns on failure."""
    if os.path.exists(path) and os.path.getsize(path) > 0:
        try:
            return pd.read_csv(path)
        except pd.errors.ParserError:
            # Skip bad lines to recover from partial writes / corrupted rows
            return pd.read_csv(path, on_bad_lines='skip')
    return pd.DataFrame(columns=cols)

ltg_df = load_csv(ltg_path, ["Goal", "Category", "Deadline"])
stg_df = load_csv(stg_path, ["Short Term Goal", "Parent Goal", "Progress (%)"])

with st.expander("➕ Add Long-Term Goal"):
    goal = st.text_input("Goal")
    category = st.text_input("Category")
    deadline = st.date_input("Deadline")
    if st.button("Add Long-Term Goal"):
        new_row = pd.DataFrame([[goal, category, deadline]], columns=["Goal", "Category", "Deadline"])
        new_row.to_csv(ltg_path, mode='a', header=not os.path.exists(ltg_path) or os.path.getsize(ltg_path)==0, index=False)
        st.success("Goal added!")
        ltg_df = pd.read_csv(ltg_path)

with st.expander("➕ Add Short-Term Goal"):
    parent = st.selectbox("Select Long-Term Goal", ltg_df["Goal"] if not ltg_df.empty else [])
    short_goal = st.text_input("Short-Term Goal")
    progress = st.slider("Progress (%)", 0, 100, 0)
    if st.button("Add Short-Term Goal"):
        new_row = pd.DataFrame([[short_goal, parent, progress]], columns=["Short Term Goal", "Parent Goal", "Progress (%)"])
        new_row.to_csv(stg_path, mode='a', header=not os.path.exists(stg_path) or os.path.getsize(stg_path)==0, index=False)
        st.success("Short-Term Goal added!")
        stg_df = pd.read_csv(stg_path)

st.subheader("📌 Your Goals")
st.write("### Long-Term Goals")
st.dataframe(ltg_df)

st.write("### Short-Term Goals")
st.dataframe(stg_df)