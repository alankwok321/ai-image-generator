import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Virtual Debate Partner", page_icon="🗣️")
st.title("🗣️ Virtual Debate Partner (虛擬辯論對手)")

# --- Config ---
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')

# --- Persona Selection ---
persona = st.sidebar.selectbox("選擇對手風格", [
    "理性科學家 (Focus on data & logic)",
    "激進環保主義者 (Focus on ethics & impact)",
    "魔鬼代言人 (Always challenges your point)",
    "蘇格拉底 (Asks deep philosophical questions)"
])

topic = st.sidebar.text_input("設定辯論題目", "核能發電是否應該被推廣？")

# --- System Prompt ---
SYSTEM_PROMPT = f"""
你現在扮演一位「{persona}」。
辯論題目是：「{topic}」。
你的任務是：
1. 堅定地站在使用者的對立面（或根據角色設定）。
2. 指出使用者論點中的邏輯謬誤。
3. 引用數據或理論來支持你的觀點。
4. 保持辯論的專業性，但語氣要符合角色設定。
5. 每次回覆控制在 150 字以內，保持節奏。
"""

# --- Chat History ---
if "debate_history" not in st.session_state:
    st.session_state.debate_history = []

# --- UI ---
st.caption(f"當前題目：{topic}")

for msg in st.session_state.debate_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("提出你的論點...")

if user_input:
    # User Turn
    st.session_state.debate_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # AI Turn
    if api_key:
        with st.chat_message("assistant"):
            with st.spinner("對手正在思考反駁點..."):
                try:
                    # Construct prompt with history
                    full_prompt = [SYSTEM_PROMPT]
                    for m in st.session_state.debate_history:
                        full_prompt.append(f"{m['role']}: {m['content']}")
                    
                    response = model.generate_content(full_prompt)
                    st.write(response.text)
                    st.session_state.debate_history.append({"role": "assistant", "content": response.text})
                    
                    # Analysis (Mock or Real)
                    with st.expander("📊 即時邏輯分析 (AI Coach)"):
                        st.info("分析你的論點強度...")
                        analysis_prompt = f"分析這句話的邏輯強度與漏洞：'{user_input}'。請簡短給出 1 個優點和 1 個改進點。"
                        analysis = model.generate_content(analysis_prompt)
                        st.markdown(analysis.text)

                except Exception as e:
                    st.error(f"API Error: {e}")
    else:
        st.warning("請先輸入 API Key 才能開始辯論。")
