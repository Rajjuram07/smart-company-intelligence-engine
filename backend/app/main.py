from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from app.models import User, LoginRequest, CompanySearchRequest, CompanyResponse
from app.database import engine, get_db, Base
from app.services.search_service import search_company
from app.services.scraper_service import scrape_url
from app.services.ai_service import synthesize_company_data
from app.utils.auth import verify_api_key

load_dotenv(override=True)

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Company Intelligence Engine")

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Company Intelligence Engine API"}

@app.post("/signup")
def signup(request: LoginRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == request.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists. Please log in.")
    new_user = User(username=request.username, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"success": True, "message": "Account created! You can now log in."}

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"success": True}

# @app.post("/api/analyze", response_model=CompanyResponse)
@app.post("/analyze", response_model=CompanyResponse)
def analyze_company(request: CompanySearchRequest, auth: str = Depends(verify_api_key)):
    company_name = request.company_name
    if not company_name:
        raise HTTPException(status_code=400, detail="Company name is required.")
        
    try:
        # 1. Search for company links
        search_data = search_company(company_name)
        links = search_data.get("links", [])
        
        # 2. Classify and Scrape links to ensure diverse context
        scraped_texts = {}
        scraped_urls = set()
        
        def add_to_scrape(link):
            url = link.get("url")
            if url and url not in scraped_urls and len(scraped_urls) < 5:
                scraped_texts[url] = scrape_url(url)
                scraped_urls.add(url)
                
        # Grab first link (often official site or wikipedia)
        if links:
            add_to_scrape(links[0])
            
        # Try finding jobs
        for link in links:
            url = link.get("url", "").lower()
            if "naukri.com" in url or "indeed.com" in url or "linkedin.com/jobs" in url or "jobs" in url:
                add_to_scrape(link)
                break
                
        # Try finding reviews
        for link in links:
            url = link.get("url", "").lower()
            if "glassdoor.com" in url or "ambitionbox.com" in url:
                add_to_scrape(link)
                break

        # Fill the rest with top results up to 4 total
        for link in links:
            if len(scraped_urls) >= 4:
                break
            add_to_scrape(link)
                
        # 3. Synthesize with Gemini
        result = synthesize_company_data(company_name, search_data, scraped_texts)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

