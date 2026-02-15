import requests
from bs4 import BeautifulSoup
import json

def search_jump_jobs():
    # 明報 JUMP 的搜尋 URL (這裡使用教育類別關鍵字)
    url = "https://jump.mingpao.com/job-search/?keyword=%E6%95%99%E5%B8%AB&industry=8"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    keywords = ["數學", "科學", "Math", "Science", "Physics", "Chemistry", "Biology", "物理", "化學", "生物"]
    found_jobs = []

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return f"Error: Status code {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根據明報 JUMP 的結構尋找職位列表
        # 注意：此處選擇器需根據實際 HTML 調整
        job_items = soup.select('.job-item') # 假設職位項目的 class 是 job-item

        for item in job_items:
            title = item.select_one('.title').text.strip() if item.select_one('.title') else ""
            company = item.select_one('.company-name').text.strip() if item.select_one('.company-name') else ""
            link = item.select_one('a')['href'] if item.select_one('a') else ""

            # 檢查關鍵字
            if any(kw.lower() in title.lower() for kw in keywords):
                found_jobs.append({
                    "title": title,
                    "company": company,
                    "link": link if link.startswith('http') else f"https://jump.mingpao.com{link}"
                })

        return found_jobs
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    results = search_jump_jobs()
    print(json.dumps(results, ensure_ascii=False, indent=2))
