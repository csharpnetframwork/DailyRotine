import streamlit as st
import pandas as pd
import os
from utils import get_local_time  # ✅ Import local time helper

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Normalize task columns
def normalize_tasks(df):
    return df.rename(columns={
        'date': 'Date',
        'time': 'Time',
        'task': 'Task',
        'category': 'Category',
        'status': 'Completed'
    })

st.header("✅ Daily Review")

task_path = "data/daily_tasks.csv"
review_path = "data/daily_reviews.csv"

# ✅ Use IST time
today = str(get_local_time().date())

# Load and normalize today's tasks
if os.path.exists(task_path):
    tasks_df = normalize_tasks(pd.read_csv(task_path, on_bad_lines='skip'))
    today_tasks = tasks_df[tasks_df["Date"] == today]
else:
    today_tasks = pd.DataFrame()

# Proceed only if tasks exist
if not today_tasks.empty:
    total = len(today_tasks)
    completed_numeric = today_tasks['Completed'].astype(str).str.lower().isin(["yes", "true", "1", "complete"]).astype(int)
    done = completed_numeric.sum()
    pct = int((done / total) * 100) if total else 0

    # Display score
    st.metric("🎯 Productivity Score", f"{pct}%")
    st.progress(pct)

    # Feedback
    feedback = "Great job! 🎉" if pct >= 80 else "You can improve tomorrow! 💪"
    st.write(f"**Feedback:** {feedback}")

    # Ensure review file exists
    if not os.path.exists(review_path):
        pd.DataFrame(columns=["Date", "Productivity (%)"]).to_csv(review_path, index=False)

    review_df = pd.read_csv(review_path)
    review_df.columns = review_df.columns.str.strip().str.title()  # Normalize column names

    # Append if not already reviewed today
    if today not in review_df["Date"].astype(str).values:
        new_review = pd.DataFrame([[today, pct]], columns=["Date", "Productivity (%)"])
        new_review.to_csv(review_path, mode='a', header=False, index=False)

else:
    st.info("📭 No tasks to review today. Plan your day first.")
