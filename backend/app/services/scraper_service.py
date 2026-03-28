import requests
from bs4 import BeautifulSoup

def scrape_url(url: str) -> str:
    """
    Fetches the URL and extracts text content using BeautifulSoup.
    Keeps extraction small to prevent token limits in Gemini.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts and styles
        for ele in soup(["script", "style", "nav", "footer", "header"]):
            ele.extract()
            
        text = soup.get_text(separator=' ', strip=True)
        # return first 4000 characters to ensure jobs and reviews are captured
        return text[:4000]
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""
