import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
os.makedirs("data", exist_ok=True)

st.header("📊 Progress Charts")

# Load goals
ltg_path = "data/long_term_goals.csv"
stg_path = "data/short_term_goals.csv"

if os.path.exists(stg_path):
    df = pd.read_csv(stg_path, on_bad_lines='skip')
    # Harmonize column names in case of older schema
    col_map = {
        'long_term_goal': 'Parent Goal',
        'progress': 'Progress (%)',
        'Progress': 'Progress (%)'
    }
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
    required_cols = {'Parent Goal', 'Progress (%)'}
    if required_cols.issubset(df.columns):
        grouped = df.groupby("Parent Goal")["Progress (%)"].mean().reset_index()
    else:
        st.warning("Short-term goals file is missing expected columns; cannot draw progress chart.")
        grouped = pd.DataFrame()

    st.subheader("🎯 Goal Progress")
    st.bar_chart(data=grouped.set_index("Parent Goal"))
else:
    st.info("No goal data found.")

# Load review data
review_path = "data/daily_reviews.csv"
if os.path.exists(review_path):
    review_df = pd.read_csv(review_path, on_bad_lines='skip')
    # Harmonize columns
    review_df = review_df.rename(columns={'date': 'Date', 'productivity (%)': 'Productivity (%)', 'productivity': 'Productivity (%)'})
    if 'Productivity (%)' not in review_df.columns and {'completed_tasks','total_tasks'}.issubset(review_df.columns):
        # Convert to numeric to avoid dtype issues
        completed = pd.to_numeric(review_df['completed_tasks'], errors='coerce')
        total = pd.to_numeric(review_df['total_tasks'], errors='coerce')
        review_df['Productivity (%)'] = ((completed / total) * 100).fillna(0).round(0)


    if 'Date' not in review_df.columns:
        st.warning('Daily review file missing Date column; cannot plot productivity trend.')
    else:
        review_df['Date'] = pd.to_datetime(review_df['Date'])
    
    st.subheader("📈 Daily Productivity Over Time")
    st.line_chart(review_df.set_index("Date"))
else:
    st.info("No daily review data available.")