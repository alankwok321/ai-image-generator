import streamlit as st

st.set_page_config(page_title="Education AI Suite", page_icon="🏫", layout="wide")

st.title("🏫 AI Education Suite")
st.markdown("### Select an App to Launch")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("🎓 AI Solver")
    st.write("Step-by-step guidance for math/science problems using Socratic method.")
    st.info("Run specific app: `streamlit run education-apps/ai-solver/app.py`")

with col2:
    st.header("🗺️ Knowledge RPG")
    st.write("Diagnose learning gaps and generate personalized remedial paths.")
    st.info("Run specific app: `streamlit run education-apps/knowledge-rpg/app.py`")

with col3:
    st.header("🗣️ Debate Partner")
    st.write("Practice critical thinking with an AI opponent in various personas.")
    st.info("Run specific app: `streamlit run education-apps/debate-partner/app.py`")

st.markdown("---")
st.markdown("### How to Deploy")
st.markdown("""
To run these apps online for free:
1. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Connect your GitHub account.
3. Select this repository: `alankwok321/ai-image-generator`.
4. **Main App Path**: Enter the path to the specific app you want to run (e.g., `education-apps/ai-solver/app.py`).
5. Click **Deploy**.
""")
