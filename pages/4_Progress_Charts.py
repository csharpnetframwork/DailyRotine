import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.header("📊 Progress Charts")

# Ensure data folder
os.makedirs("data", exist_ok=True)

# Paths
ltg_path = "data/long_term_goals.csv"
stg_path = "data/short_term_goals.csv"
review_path = "data/daily_reviews.csv"

# === Short-Term Goals Progress ===
if os.path.exists(stg_path):
    df = pd.read_csv(stg_path, on_bad_lines='skip')

    # Normalize column names
    col_map = {
        'long_term_goal': 'Parent Goal',
        'progress': 'Progress (%)',
        'Progress': 'Progress (%)'
    }
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

    if {'Parent Goal', 'Progress (%)'}.issubset(df.columns):
        grouped = df.groupby("Parent Goal")["Progress (%)"].mean().reset_index()
        st.subheader("🎯 Goal Progress")
        st.bar_chart(data=grouped.set_index("Parent Goal"))
    else:
        st.warning("Short-term goals file is missing expected columns; cannot draw progress chart.")
else:
    st.info("No short-term goal data found.")

# === Daily Productivity Trend ===
if os.path.exists(review_path):
    review_df = pd.read_csv(review_path, on_bad_lines='skip')

    # Normalize columns
    review_df = review_df.rename(columns={
        'date': 'Date',
        'productivity (%)': 'Productivity (%)',
        'productivity': 'Productivity (%)'
    })

    # Compute productivity if not available
    if 'Productivity (%)' not in review_df.columns and {'completed_tasks', 'total_tasks'}.issubset(review_df.columns):
        completed = pd.to_numeric(review_df['completed_tasks'], errors='coerce')
        total = pd.to_numeric(review_df['total_tasks'], errors='coerce')
        review_df['Productivity (%)'] = ((completed / total) * 100).fillna(0).round(0)

    if 'Date' not in review_df.columns:
        st.warning('Daily review file missing Date column; cannot plot productivity trend.')
    else:
        review_df['Date'] = pd.to_datetime(review_df['Date'])
        st.subheader("📈 Daily Productivity Over Time")
        st.line_chart(review_df.set_index("Date")["Productivity (%)"])
else:
    st.info("No daily review data available.")
