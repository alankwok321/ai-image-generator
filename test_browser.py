import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # 監聽控制台訊息
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))

        print("正在開啟網頁...")
        await page.goto("https://alankwok321.github.io/ai-image-generator/")
        
        # 等待一段時間讓內容加載
        await asyncio.sleep(3)
        
        # 截圖確認頁面渲染
        await page.screenshot(path="screenshot.png")
        print("截圖已儲存為 screenshot.png")
        
        await browser.close()

asyncio.run(run())
