from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import Column, Integer, String
from app.database import Base

# SQLAlchemy User table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

# Pydantic Schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class CompanySearchRequest(BaseModel):
    company_name: str

class CompanyLink(BaseModel):
    title: str
    url: str

class CompanyReview(BaseModel):
    platform: str
    summary: str
    rating: Optional[str]

class CompanyJob(BaseModel):
    title: str
    platform: str
    location: Optional[str]
    url: str

class CompanyResponse(BaseModel):
    company_name: str
    website: Optional[str]
    linkedin: Optional[str]
    founded_year: Optional[str]
    company_type: Optional[str]
    location: Optional[str]
    legitimacy_status: str
    trust_score: int
    ai_summary: str
    jobs: List[CompanyJob]
    reviews: List[CompanyReview]
    source_links: List[CompanyLink]
