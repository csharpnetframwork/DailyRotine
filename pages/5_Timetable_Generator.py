import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
import os
os.makedirs("data", exist_ok=True)

def normalize_tasks(df):
    """Rename legacy lowercase columns to standard ones."""
    df = df.rename(columns={
        'date': 'Date',
        'time': 'Time',
        'task': 'Task',
        'category': 'Category',
        'status': 'Completed'
    })
    # Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]
    # If 'Time' still missing but 'Time ' present, fix
    if 'Time' not in df.columns:
        for col in df.columns:
            if col.lower().strip() == 'time':
                df = df.rename(columns={col: 'Time'})
                break
    return df

st.header("🧠 Timetable Suggestion")

st.subheader("Timetable for Today")

# Try to build from user's planned tasks first
TASK_PATH = "data/daily_tasks.csv"
today_str = str(datetime.today().date())

schedule = []
if os.path.exists(TASK_PATH) and os.path.getsize(TASK_PATH) > 0:
    tasks_df = normalize_tasks(pd.read_csv(TASK_PATH, on_bad_lines='skip'))
    tasks_today = tasks_df[tasks_df["Date"] == today_str]
    if not tasks_today.empty:
        if 'Time' in tasks_today.columns:
            # Convert to datetime and sort
            tasks_today['Time'] = pd.to_datetime(tasks_today['Time'], errors='coerce').dt.time
            tasks_today = tasks_today.sort_values('Time')
            for _, row in tasks_today.iterrows():
                if pd.notna(row['Time']):
                    schedule.append((row['Time'].strftime('%H:%M'), row['Task']))
        else:
            # Fallback: no Time column, just list tasks in entered order
            for _, row in tasks_today.iterrows():
                schedule.append(('--', row['Task']))

if not schedule:
    st.info("No tasks found for today – generating generic focus blocks.")
    wake_time = st.time_input("Wake-up time", value=time(7,0))
    sleep_time = st.time_input("Sleep time", value=time(22,30))
    focus_block = st.slider("Focus Block (mins)", 25, 120, 60)
    current_dt = datetime.combine(datetime.today(), wake_time)
    end_dt = datetime.combine(datetime.today(), sleep_time)
    while current_dt < end_dt:
        activity = "Focus Work" if current_dt.hour < 12 else "Light Tasks / Learning"
        schedule.append((current_dt.strftime("%H:%M"), activity))
        current_dt += timedelta(minutes=focus_block)

st.markdown("### 🕒 Suggested Schedule")
for t, act in schedule:
    st.write(f"**{t}** → {act}")