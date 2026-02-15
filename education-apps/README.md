# Education AI App Suite (教育科技應用)

這是一套基於 Python (Streamlit) 與 Gemini API 的教育科技應用概念驗證。

## 1. AI Step-by-Step Solver (AI 解題導師)
*   **功能**: 學生上傳數學/科學題目圖片，AI 使用蘇格拉底式引導法，一步步提問，幫助學生自己找到答案。
*   **核心**: 多模態 (Vision + Text) 理解，錯誤偵測，分段引導。
*   **啟動**: `streamlit run education-apps/ai-solver/app.py`

## 2. Knowledge RPG (知識漏洞地圖)
*   **功能**: 學生進行診斷測驗，AI 自動判斷弱點並生成個人化補救路徑。
*   **核心**: 知識關聯圖譜，動態難度調整。
*   **啟動**: `streamlit run education-apps/knowledge-rpg/app.py`

## 3. Virtual Debate Partner (虛擬辯論對手)
*   **功能**: AI 扮演不同立場的角色（科學家、懷疑論者），與學生針對議題進行辯論，並即時分析邏輯漏洞。
*   **核心**: 邏輯思辨訓練，即時回饋。
*   **啟動**: `streamlit run education-apps/debate-partner/app.py`

## 安裝

```bash
pip install -r education-apps/requirements.txt
```

## 使用需知

這些應用程式需要有效的 **Google Gemini API Key** 才能運作。請確保您已申請並在側邊欄輸入 Key。
