import streamlit as st
import json
import random

# --- Load Data ---
@st.cache_data
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

# --- Config ---
st.set_page_config(page_title="Knowledge RPG 知識冒險", page_icon="🗺️")
st.title("🗺️ Knowledge RPG (知識漏洞地圖)")
st.sidebar.markdown("**模式：** 診斷與補救教學")

# --- Session State ---
if "current_q_id" not in st.session_state:
    st.session_state.current_q_id = "q1" # Start
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "path" not in st.session_state:
    st.session_state.path = ["Start"]

# --- Logic ---
def get_question(qid):
    if qid == "win":
        return {"id": "win", "message": "恭喜！你已經掌握了這個單元的核心概念！", "type": "end"}
    if qid == "q_fail":
        return {"id": "fail", "message": "看來需要在基礎運算上多加練習，請複習第一章。", "type": "end"}
    
    for q in questions:
        if q["id"] == qid:
            return q
    return None

current_q = get_question(st.session_state.current_q_id)

# --- UI ---
if current_q["type"] == "end":
    st.success(current_q["message"])
    st.balloons()
    if st.button("重新開始"):
        st.session_state.current_q_id = "q1"
        st.session_state.score = 0
        st.session_state.path = ["Start"]
        st.rerun()
else:
    # Display Question
    st.subheader(f"📍 當前位置：{current_q.get('topic', 'Unknown')}")
    st.progress(len(st.session_state.path) * 10) # Mock progress
    
    st.write(f"### {current_q['question']}")
    
    # Options
    selected_option = st.radio("選擇答案：", current_q["options"], index=None)
    
    if st.button("提交答案"):
        if selected_option:
            if selected_option == current_q["answer"]:
                st.success("✅ 正確！前往下一關...")
                st.session_state.score += 10
                st.session_state.path.append(current_q["id"] + " (Correct)")
                st.session_state.current_q_id = current_q["next_if_correct"]
                st.rerun()
            else:
                st.error(f"❌ 錯誤。提示：{current_q['hint']}")
                st.session_state.path.append(current_q["id"] + " (Wrong)")
                if "next_if_wrong" in current_q:
                    st.warning("🔄 啟動補救教學路徑...")
                    st.session_state.current_q_id = current_q["next_if_wrong"]
                    st.rerun()
                else:
                    st.info(f"正確答案是：{current_q['answer']}")
                    # Simple linear fallback if no specific branch
        else:
            st.warning("請先選擇一個選項。")

# --- Debug/Map View ---
with st.expander("查看我的學習路徑 (Knowledge Map)"):
    st.write(" -> ".join(st.session_state.path))
    st.json(st.session_state.history)
