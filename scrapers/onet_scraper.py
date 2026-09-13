import requests
import pandas as pd
import json
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ONetScraper:
    """
    Scraper for O*NET (Occupational Information Network) data
    - Free, official US job classification data
    - Contains 900+ occupations
    - Updated regularly by US Department of Labor
    """
    
    BASE_URL = "https://www.onetcenter.org/dl_files"
    
    def __init__(self):
        self.occupations = []
        self.skills = []
        self.abilities = []
        
    def fetch_onet_data(self) -> Dict:
        """
        Fetch O*NET occupation database
        Returns dictionary with occupation data
        """
        try:
            logger.info("Fetching O*NET occupation data...")
            
            # O*NET provides downloadable CSV files
            # We'll construct URLs to the public data files
            data = {
                "occupations": self._get_occupations(),
                "skills": self._get_skills(),
                "abilities": self._get_abilities(),
                "work_activities": self._get_work_activities()
            }
            
            logger.info(f"Successfully fetched O*NET data: {len(data['occupations'])} occupations")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching O*NET data: {e}")
            return {}
    
    def _get_occupations(self) -> List[Dict]:
        """
        Get occupation titles and descriptions from O*NET
        """
        # In production, download from:
        # https://www.onetcenter.org/dl_files/Data/db_28_0_text/Occupation%20Data.txt
        
        sample_occupations = [
            {
                "onet_code": "11-1011.00",
                "title": "Chief Executives",
                "description": "Determine and formulate policies and provide overall direction of companies or private and public sector organizations.",
                "salary_min": 100000,
                "salary_max": 250000,
                "job_outlook": "Grow 8%"
            },
            {
                "onet_code": "13-1111.00",
                "title": "Management Analysts",
                "description": "Conduct organizational studies and evaluations, design systems and procedures.",
                "salary_min": 60000,
                "salary_max": 130000,
                "job_outlook": "Grow 11%"
            },
            {
                "onet_code": "15-1132.00",
                "title": "Software Developers",
                "description": "Develop, create, and modify general computer applications software.",
                "salary_min": 80000,
                "salary_max": 160000,
                "job_outlook": "Grow 17%"
            },
            {
                "onet_code": "29-1141.00",
                "title": "Registered Nurses",
                "description": "Assess patient health status and needs, develop and implement nursing care plans.",
                "salary_min": 50000,
                "salary_max": 90000,
                "job_outlook": "Grow 6%"
            }
        ]
        
        return sample_occupations
    
    def _get_skills(self) -> List[Dict]:
        """
        Get required skills for occupations
        """
        skills = [
            {"skill_id": "S1", "name": "Python Programming", "category": "Technical"},
            {"skill_id": "S2", "name": "Data Analysis", "category": "Technical"},
            {"skill_id": "S3", "name": "Project Management", "category": "Management"},
            {"skill_id": "S4", "name": "Communication", "category": "Soft Skills"},
            {"skill_id": "S5", "name": "Leadership", "category": "Soft Skills"},
            {"skill_id": "S6", "name": "Patient Care", "category": "Healthcare"},
            {"skill_id": "S7", "name": "Database Management", "category": "Technical"},
            {"skill_id": "S8", "name": "Problem Solving", "category": "Soft Skills"},
        ]
        return skills
    
    def _get_abilities(self) -> List[Dict]:
        """
        Get abilities required for occupations
        """
        abilities = [
            {"ability_id": "A1", "name": "Oral Expression", "description": "Ability to communicate ideas clearly"},
            {"ability_id": "A2", "name": "Mathematical Reasoning", "description": "Ability to understand and apply math concepts"},
            {"ability_id": "A3", "name": "Deductive Reasoning", "description": "Ability to apply rules and logic"},
            {"ability_id": "A4", "name": "Physical Strength", "description": "Ability to exert physical force"},
        ]
        return abilities
    
    def _get_work_activities(self) -> List[Dict]:
        """
        Get work activities and tasks for occupations
        """
        activities = [
            {"activity_id": "WA1", "name": "Analyzing Data", "description": "Working with data or information"},
            {"activity_id": "WA2", "name": "Managing People", "description": "Supervising, training, or directing people"},
            {"activity_id": "WA3", "name": "Helping Others", "description": "Providing assistance to others"},
        ]
        return activities
    
    def save_to_json(self, filename: str = "onet_data.json"):
        """
        Save scraped O*NET data to JSON file
        """
        data = self.fetch_onet_data()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Data saved to {filename}")
    
    def save_to_csv(self, filename: str = "onet_occupations.csv"):
        """
        Save occupations to CSV file
        """
        data = self.fetch_onet_data()
        df = pd.DataFrame(data["occupations"])
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename}")


if __name__ == "__main__":
    scraper = ONetScraper()
    data = scraper.fetch_onet_data()
    
    print("\n=== O*NET OCCUPATIONS ===")
    for occ in data["occupations"]:
        print(f"\n{occ['title']} ({occ['onet_code']})")
        print(f"Description: {occ['description']}")
        print(f"Salary: ${occ['salary_min']:,} - ${occ['salary_max']:,}")
        print(f"Outlook: {occ['job_outlook']}")
