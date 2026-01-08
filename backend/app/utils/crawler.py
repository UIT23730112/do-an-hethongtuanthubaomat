import requests
from bs4 import BeautifulSoup

def crawl_policy_text(url: str) -> str:
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        raise ValueError(f"Cannot access URL, status code: {resp.status_code}")
    soup = BeautifulSoup(resp.text, "html.parser")
    paragraphs = soup.find_all("p")
    text = "\n".join([p.get_text(strip=True) for p in paragraphs])
    return text
