from datetime import datetime
from typing import List, Optional

# SQLAlchemy-style models (for PostgreSQL)

class Occupation:
    """
    Represents a career/occupation based on O*NET data
    """
    def __init__(self, onet_code: str, title: str, description: str, 
                 salary_min: float, salary_max: float, job_outlook: str):
        self.onet_code = onet_code
        self.title = title
        self.description = description
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.job_outlook = job_outlook
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'onet_code': self.onet_code,
            'title': self.title,
            'description': self.description,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'job_outlook': self.job_outlook,
            'created_at': self.created_at.isoformat()
        }


class Skill:
    """
    Represents a professional skill required for occupations
    """
    def __init__(self, name: str, category: str, description: Optional[str] = None):
        self.name = name
        self.category = category  # Technical, Soft Skills, Management, etc.
        self.description = description
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }


class JobListing:
    """
    Represents a scraped job listing
    """
    def __init__(self, title: str, company: str, location: str, 
                 description: str, url: str, source: str = "Unknown"):
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.url = url
        self.source = source
        self.salary_min: Optional[float] = None
        self.salary_max: Optional[float] = None
        self.job_type = "Full-time"  # Full-time, Part-time, Contract, Remote
        self.skills: List[str] = []
        self.posted_at = datetime.now()
        self.scraped_at = datetime.now()
    
    def to_dict(self):
        return {
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'url': self.url,
            'source': self.source,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'job_type': self.job_type,
            'skills': self.skills,
            'posted_at': self.posted_at.isoformat(),
            'scraped_at': self.scraped_at.isoformat()
        }


class UserProfile:
    """
    Represents a user on the career guidance platform
    """
    def __init__(self, name: str, email: str):
        self.id: Optional[str] = None
        self.name = name
        self.email = email
        self.skills: List[str] = []
        self.interests: List[str] = []
        self.experience_years: int = 0
        self.preferred_locations: List[str] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'skills': self.skills,
            'interests': self.interests,
            'experience_years': self.experience_years,
            'preferred_locations': self.preferred_locations,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class CareerRecommendation:
    """
    Represents a career recommendation based on user profile
    """
    def __init__(self, user_id: str, occupation: Occupation, score: float):
        self.user_id = user_id
        self.occupation = occupation
        self.score = score  # 0-100, how well the occupation matches
        self.reason: str = ""  # Why this recommendation was made
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'occupation': self.occupation.to_dict(),
            'score': self.score,
            'reason': self.reason,
            'created_at': self.created_at.isoformat()
        }
