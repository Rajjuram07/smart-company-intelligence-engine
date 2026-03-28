import os
import google.generativeai as genai
import json

def synthesize_company_data(company_name: str, search_data: dict, scraped_texts: dict) -> dict:
    """
    Sends combined data to Gemini API and requests a structured JSON response.
    Extracts dynamic data based strictly on search and scraped evidence.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is missing. Please configure it in .env to proceed.")
        
    genai.configure(api_key=api_key)
    
    # Use the requested Gemini model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are an AI intelligence engine analyzing the company: '{company_name}'.
    
    You have been provided with real-time Google search results and text scraped from the most relevant URLs.
    Search Results: {json.dumps(search_data)}
    Scraped Texts: {json.dumps(scraped_texts)}
    
    Your task is to extract dynamic, unique information from the provided context.
    IMPORTANT STRICT INSTRUCTIONS:
    - DO NOT use generic or static/mock data. If a specific data point is missing from the search results or scraped text, you MUST fallback exactly as instructed.
    - Extract real open jobs strictly from the context (e.g., from Naukri, Indeed, LinkedIn). 
      - If NO jobs are found in the context, return exactly ONE object in the jobs array: {{"title": "No recent jobs found", "platform": "N/A", "location": "N/A", "url": "#"}}
    - Extract real employee reviews and sentiment from the context (e.g., from Glassdoor, AmbitionBox). 
      - Extract a rating (like "4.5/5") if explicitly found. If you see reviews but no numeric rating, generate an approximate sentiment rating based on the text.
      - If NO reviews are found in the context, return exactly ONE object in the reviews array: {{"platform": "System", "summary": "No reviews available", "rating": "Not available"}}
    - Generate a truly unique, context-aware 2-3 sentence overview for `ai_summary` based ENTIRELY on the provided text. Never use a boilerplate template.
    
    Return a structured JSON with exactly this format:
    {{
      "company_name": "{company_name}",
      "website": "URL or null",
      "linkedin": "URL or null",
      "founded_year": "Year or unknown",
      "company_type": "Type of company or unknown",
      "location": "Location or unknown",
      "legitimacy_status": "Safe, Suspicious, or Unknown",
      "trust_score": Integer (0 to 100) based on positive mentions and reputation,
      "ai_summary": "Your unique summary",
      "jobs": [
        {{"title": "Job Title", "platform": "Platform Name", "location": "Location", "url": "URL"}}
      ],
      "reviews": [
        {{"platform": "Platform Name", "summary": "Detailed summary of the review or sentiment", "rating": "String rating e.g. 4.2/5"}}
      ],
      "source_links": [
        {{"title": "Page Title", "url": "URL"}}
      ]
    }}
    
    Output ONLY valid JSON. Do not wrap it in markdown block quotes (```json).
    """
    
    try:
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        if text_response.startswith("```json"):
            text_response = text_response.replace("```json", "", 1)
            if text_response.endswith("```"):
                text_response = text_response[:-3]
        elif text_response.startswith("```"):
            text_response = text_response.replace("```", "", 1)
            if text_response.endswith("```"):
                text_response = text_response[:-3]
                
        data = json.loads(text_response.strip())
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing Gemini JSON: {e}")
        print(f"Raw response: {text_response}")
        raise ValueError("Failed to parse AI output into valid JSON.")
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "Resource Exhausted" in error_msg or "quota" in error_msg.lower():
            raise ValueError("Gemini Free Tier Rate Limit Exceeded! Please wait about 60 seconds before searching again.")
        print(f"Error calling Gemini: {e}")
        raise ValueError(f"Failed to generate synthesis: {e}")
