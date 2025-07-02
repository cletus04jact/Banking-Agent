import requests
from bs4 import BeautifulSoup
import os
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}
BANK_URLS = {
    "RBI": "https://www.rbi.org.in/Scripts/FAQView.aspx?head=General",
    "SBI": "https://www.onlinesbi.sbi/help",
    "ICICI": "https://www.icicibank.com/help-and-contact-us/faqs",
    "HDFC": "https://www.hdfcbank.com/personal/help/faqs"
}
SAVE_DIR = "scraped_data"
os.makedirs(SAVE_DIR, exist_ok=True)

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def scrape_and_save(name, url):
    try:
        print(f"Scraping {name}...")
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        for script in soup(["script", "style", "noscript"]):
            script.extract()
        text = soup.get_text(separator="\n")
        cleaned = "\n".join([clean_text(line) for line in text.splitlines() if line.strip()])
        with open(os.path.join(SAVE_DIR, f"{name.lower()}_faq.txt"), "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"Saved {name} FAQ ✅")
    except Exception as e:
        print(f"Error with {name}: {e}")

if __name__ == "__main__":
    for bank, url in BANK_URLS.items():
        scrape_and_save(bank, url)
