import os
import json
import requests

def search_company(company_name: str) -> dict:
    """
    Searches for the company using Serper.dev API and returns top links.
    """
    api_key = os.getenv("SERPAPI_KEY") 
    if not api_key or api_key == "your_serpapi_key_here":
        raise ValueError("Search API Key is missing. Please configure it in .env to proceed.")

    url = "https://google.serper.dev/search"
    payload = json.dumps({
      "q": f"{company_name} official website OR site:linkedin.com/company OR site:naukri.com OR site:indeed.com OR site:glassdoor.com OR site:ambitionbox.com",
      "num": 15
    })
    headers = {
      'X-API-KEY': api_key,
      'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        
        if response.status_code != 200:
            raise ValueError(f"Serper API Error: {response.text}")
            
        results = response.json()
        organic_results = results.get("organic", [])
        
        links = []
        for result in organic_results:
            links.append({
                "title": result.get("title", ""),
                "url": result.get("link", ""),
                "snippet": result.get("snippet", "")
            })
            
        return {"links": links}
    except Exception as e:
        print(f"Error in Serper search: {e}")
        raise ValueError(f"Search Engine Error: {e}")
