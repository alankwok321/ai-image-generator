import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- Config ---
st.set_page_config(page_title="AI Step-by-Step Solver", page_icon="🎓")
st.title("🎓 AI Step-by-Step Solver (AI 解題導師)")

# API Key Handling (You can replace this with st.secrets)
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
if not api_key:
    st.info("請輸入 API Key 以開始使用。")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro') # Using multimodal model

# --- System Prompt ---
SYSTEM_PROMPT = """
你是一位擁有蘇格拉底式教學法的頂尖數學/科學導師。
當學生上傳題目或發問時，請遵循以下原則：
1. **絕不直接給出答案**。
2. **引導思考**：提出關鍵問題，讓學生自己發現下一步。例如：「這題看起來像是一元二次方程式，你記得第一步通常要做什麼嗎？」
3. **錯誤偵測**：如果學生算出錯誤答案，請指出具體的邏輯漏洞（例如：「你的負號是不是在移項時忘記變號了？」）。
4. **語氣溫柔且鼓勵**：像一位有耐心的家教老師。
5. **分步驟**：一次只引導一步，不要一次講完所有概念。
"""

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add system prompt as context (hidden from UI, but sent to model)
    # Note: Streamlit chat history usually stores displayable messages. 
    # We'll prepend the system prompt logic in the API call.

# --- UI ---
with st.sidebar:
    st.header("上傳題目")
    uploaded_file = st.file_uploader("拍照或上傳圖片", type=["jpg", "png", "jpeg"])
    image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="題目預覽", use_column_width=True)

# Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "image" in msg and msg["image"]:
            st.image(msg["image"], width=200)

# Input
user_input = st.chat_input("輸入你的問題或是算式...")

if user_input or (image and len(st.session_state.messages) == 0):
    # Handle initial image upload trigger or text input
    prompt_parts = [SYSTEM_PROMPT]
    
    # Add history
    for msg in st.session_state.messages:
        prompt_parts.append(f"{msg['role']}: {msg['content']}")
    
    # Current input
    user_msg_content = user_input if user_input else "請幫我看看這題怎麼做？"
    prompt_parts.append(f"user: {user_msg_content}")
    
    # Display User Message
    with st.chat_message("user"):
        st.write(user_msg_content)
        if image and len(st.session_state.messages) == 0:
            st.image(image, width=200)
    
    st.session_state.messages.append({"role": "user", "content": user_msg_content, "image": image if len(st.session_state.messages) == 0 else None})

    # Call AI
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                inputs = [user_msg_content]
                if image and len(st.session_state.messages) == 1: # Only send image on first turn or if strictly needed
                     inputs.append(image)
                
                # Full prompt construction for simple chat (stateless API usage for demo)
                # Ideally use chat = model.start_chat()
                
                chat = model.start_chat(history=[])
                # We need to inject system prompt behavior. Gemini supports system instructions in newer versions or via prompt.
                # For simplicity in this demo, we prepend text.
                
                if image:
                    response = model.generate_content([SYSTEM_PROMPT, image, user_msg_content])
                else:
                    # Construct history for text-only context if needed, but start_chat handles it better.
                    # Simplified for "one-shot" feel + history context in prompt if not using chat session object
                    # Let's use specific prompt construction:
                    full_prompt = [SYSTEM_PROMPT]
                    for m in st.session_state.messages:
                        if m["image"]: full_prompt.append(m["image"])
                        full_prompt.append(f"{m['role']}: {m['content']}")
                    
                    response = model.generate_content(full_prompt)

                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"發生錯誤: {e}")
