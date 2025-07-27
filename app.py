import streamlit as st
from datetime import datetime
from utils import get_local_time

now = get_local_time()

st.set_page_config(
    page_title="My Life Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌟 My Life Productivity Dashboard")

st.markdown("""
Welcome to your personal productivity system!  
Use the sidebar to navigate between:
- 🎯 Goals
- 📝 Daily Planner
- ✅ Daily Review
- 📊 Progress Charts
- 🧠 Timetable Suggestions

Stay consistent. Reflect daily. Build your future 💪
""")

# Optional reminder message
now = datetime.now().hour
if 22 <= now <= 23:
    st.warning("🛌 It's getting late. Consider planning for proper sleep!")
elif 13 <= now <= 14:
    st.info("🍽️ Time for lunch! Recharge to stay productive.")
