import streamlit as st
import pandas as pd
from datetime import datetime, time
import os
os.makedirs("data", exist_ok=True)

def normalize_tasks(df):
    """Ensure consistent column names and order for tasks DataFrame."""
    df = df.rename(columns={
        'date': 'Date',
        'time': 'Time',
        'task': 'Task',
        'category': 'Category',
        'status': 'Completed'
    })
    # Add missing columns
    for col in ["Date", "Time", "Task", "Category", "Completed"]:
        if col not in df.columns:
            df[col] = None
    return df[["Date", "Time", "Task", "Category", "Completed"]]

st.header("📝 Daily Planner")

task_path = "data/daily_tasks.csv"

# Load tasks
if os.path.exists(task_path):
    tasks_df = normalize_tasks(pd.read_csv(task_path, on_bad_lines='skip'))
else:
    tasks_df = pd.DataFrame(columns=["Date", "Time", "Task", "Category", "Completed"])

# Task input
with st.form("add_task"):
    st.subheader("➕ Add Task for Today")
    task = st.text_input("Task")
    task_time = st.time_input("Time", value=time(9, 0))
    category = st.selectbox("Category", ["Work", "Health", "Study", "Personal", "Other"])
    submitted = st.form_submit_button("Add Task")
    if submitted and task:
        new_task = pd.DataFrame([[datetime.today().date(), task_time, task, category, False]],
                                columns=["Date", "Time", "Task", "Category", "Completed"])
        new_task.to_csv(task_path, mode='a', header=not os.path.exists(task_path), index=False)
        st.success("Task added!")

# Show today's tasks
st.subheader("📅 Today's Plan")
today = str(datetime.today().date())
tasks_df = normalize_tasks(pd.read_csv(task_path, on_bad_lines='skip'))
today_tasks = tasks_df[tasks_df["Date"] == today]

if not today_tasks.empty:
    for i, row in today_tasks.iterrows():
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"{row['Time']} - {row['Task']} ({row['Category']})")
        with col2:
            if st.checkbox("Done", key=f"chk_{i}"):
                tasks_df.at[i, "Completed"] = True
                tasks_df.to_csv(task_path, index=False)
else:
    st.info("No tasks planned for today.")