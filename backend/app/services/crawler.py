import requests
from bs4 import BeautifulSoup
import re

def crawl_policy(url: str) -> str:
    """
    Crawl văn bản chính sách từ URL.
    Trả về text thô.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        # Lấy toàn bộ text trong thẻ <p>, <li>, <h1-h6>
        text_elements = soup.find_all(["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"])
        text = "\n".join([el.get_text(separator=" ", strip=True) for el in text_elements])

        return text
    except Exception as e:
        print(f"[Crawler Error] {e}")
        return ""
    

def normalize_text(text: str) -> str:
    """
    Chuẩn hóa text: xóa ký tự đặc biệt, khoảng trắng thừa, lowercase.
    """
    # Xóa ký tự không cần thiết
    text = re.sub(r"[\r\n]+", "\n", text)          # newline chuẩn
    text = re.sub(r"[ \t]+", " ", text)            # spaces
    text = re.sub(r"[^\w\s.,]", "", text)          # ký tự đặc biệt trừ ., 
    text = text.lower()                            # lowercase
    text = text.strip()
    return text

def crawl_and_normalize(url: str) -> str:
    raw_text = crawl_policy(url)
    clean_text = normalize_text(raw_text)
    return clean_text