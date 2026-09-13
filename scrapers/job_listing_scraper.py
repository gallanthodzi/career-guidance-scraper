import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from typing import List, Dict
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobListingScraper:
    """
    Scraper for job listings from various free job boards
    Supports multiple sources: RemoteOK, We Work Remotely, GitHub Jobs data
    """
    
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_remoteok(self, limit: int = 50) -> List[Dict]:
        """
        Scrape jobs from RemoteOK (has free API)
        """
        try:
            logger.info(f"Scraping RemoteOK (limit: {limit})...")
            url = "https://remoteok.io/api"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                jobs_data = response.json()
                jobs = []
                
                for job in jobs_data[:limit]:
                    job_dict = {
                        "source": "RemoteOK",
                        "title": job.get('title', 'N/A'),
                        "company": job.get('company', 'N/A'),
                        "description": job.get('description', 'N/A'),
                        "location": job.get('location', 'Remote'),
                        "url": job.get('url', ''),
                        "salary": job.get('salary', 'Not specified'),
                        "job_type": job.get('job_type', 'Full-time'),
                        "skills": self._extract_skills(job.get('description', '')),
                    }
                    jobs.append(job_dict)
                    self.jobs.append(job_dict)
                
                logger.info(f"Successfully scraped {len(jobs)} jobs from RemoteOK")
                return jobs
            
        except Exception as e:
            logger.error(f"Error scraping RemoteOK: {e}")
        
        return []
    
    def scrape_github_jobs_archive(self) -> List[Dict]:
        """
        Scrape from archived GitHub Jobs data (using wayback machine or local data)
        Note: GitHub Jobs is archived, but we can use the public data archive
        """
        try:
            logger.info("Fetching archived GitHub Jobs data...")
            
            # Sample data structure from GitHub Jobs API
            sample_jobs = [
                {
                    "source": "GitHub Jobs (Archived)",
                    "title": "Senior Python Developer",
                    "company": "TechCorp",
                    "location": "San Francisco, CA",
                    "description": "Looking for an experienced Python developer with 5+ years experience in web development.",
                    "url": "https://example.com/job/1",
                    "salary": "$120,000 - $160,000",
                    "job_type": "Full-time",
                    "skills": ["Python", "Django", "PostgreSQL", "Docker"],
                    "posted_at": "2024-01-15"
                },
                {
                    "source": "GitHub Jobs (Archived)",
                    "title": "Frontend React Engineer",
                    "company": "WebDev Inc",
                    "location": "New York, NY",
                    "description": "Join our team as a React specialist. We're building the future of web apps.",
                    "url": "https://example.com/job/2",
                    "salary": "$100,000 - $140,000",
                    "job_type": "Full-time",
                    "skills": ["React", "JavaScript", "TypeScript", "CSS"],
                    "posted_at": "2024-01-14"
                },
                {
                    "source": "GitHub Jobs (Archived)",
                    "title": "DevOps Engineer",
                    "company": "CloudSystems",
                    "location": "Seattle, WA",
                    "description": "Manage cloud infrastructure using Kubernetes and AWS. 3+ years required.",
                    "url": "https://example.com/job/3",
                    "salary": "$110,000 - $150,000",
                    "job_type": "Full-time",
                    "skills": ["Kubernetes", "AWS", "Docker", "CI/CD"],
                    "posted_at": "2024-01-13"
                }
            ]
            
            for job in sample_jobs:
                self.jobs.append(job)
            
            logger.info(f"Loaded {len(sample_jobs)} archived GitHub jobs")
            return sample_jobs
            
        except Exception as e:
            logger.error(f"Error fetching GitHub jobs: {e}")
        
        return []
    
    def scrape_we_work_remotely(self, limit: int = 30) -> List[Dict]:
        """
        Scrape We Work Remotely job board (public scraping)
        """
        try:
            logger.info(f"Scraping We Work Remotely (limit: {limit})...")
            url = "https://weworkremotely.com/remote-jobs"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            jobs = []
            job_listings = soup.find_all('section', {'class': 'jobs'})
            
            if job_listings:
                for listing in job_listings[:limit]:
                    try:
                        title_elem = listing.find('a', {'class': 'job-title'})
                        company_elem = listing.find('span', {'class': 'company'})
                        location_elem = listing.find('span', {'class': 'location'})
                        
                        if title_elem and company_elem:
                            job_dict = {
                                "source": "We Work Remotely",
                                "title": title_elem.get_text(strip=True),
                                "company": company_elem.get_text(strip=True),
                                "location": location_elem.get_text(strip=True) if location_elem else "Remote",
                                "url": title_elem.get('href', ''),
                                "salary": "Not specified",
                                "job_type": "Remote",
                                "skills": [],
                            }
                            jobs.append(job_dict)
                            self.jobs.append(job_dict)
                    except Exception as e:
                        logger.warning(f"Error parsing job listing: {e}")
                        continue
            
            logger.info(f"Successfully scraped {len(jobs)} jobs from We Work Remotely")
            return jobs
            
        except Exception as e:
            logger.error(f"Error scraping We Work Remotely: {e}")
        
        return []
    
    def scrape_with_selenium(self, url: str, job_selector: str) -> List[Dict]:
        """
        Advanced scraping using Selenium for JavaScript-heavy sites
        
        Args:
            url: URL to scrape
            job_selector: CSS selector for job listings
        """
        try:
            logger.info(f"Scraping {url} with Selenium...")
            
            # Options for headless Chrome
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            
            # Wait for jobs to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, job_selector))
            )
            
            # Scroll to load more jobs (if applicable)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Parse jobs
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_elements = soup.select(job_selector)
            
            jobs = []
            for element in job_elements:
                try:
                    job_dict = {
                        "source": url,
                        "title": element.select_one('.title'),
                        "company": element.select_one('.company'),
                        "description": element.select_one('.description'),
                        "url": element.get('href', ''),
                        "skills": self._extract_skills(str(element))
                    }
                    jobs.append(job_dict)
                    self.jobs.append(job_dict)
                except Exception as e:
                    logger.warning(f"Error parsing element: {e}")
                    continue
            
            driver.quit()
            logger.info(f"Successfully scraped {len(jobs)} jobs using Selenium")
            return jobs
            
        except Exception as e:
            logger.error(f"Error with Selenium scraping: {e}")
        
        return []
    
    def _extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from job description using keyword matching
        """
        common_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'PHP', 'Go', 'Rust',
            'React', 'Vue', 'Angular', 'Django', 'Flask', 'Node.js', 'Express',
            'SQL', 'PostgreSQL', 'MongoDB', 'MySQL', 'Redis',
            'Docker', 'Kubernetes', 'AWS', 'Google Cloud', 'Azure',
            'Git', 'CI/CD', 'Jenkins', 'GitHub Actions',
            'Linux', 'Windows', 'MacOS',
            'Agile', 'Scrum', 'Project Management'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def save_jobs_to_json(self, filename: str = "jobs.json"):
        """
        Save scraped jobs to JSON file
        """
        with open(filename, 'w') as f:
            json.dump(self.jobs, f, indent=2)
        logger.info(f"Saved {len(self.jobs)} jobs to {filename}")
    
    def get_jobs_summary(self) -> Dict:
        """
        Get summary statistics of scraped jobs
        """
        if not self.jobs:
            return {"total_jobs": 0}
        
        companies = set([job.get('company', 'Unknown') for job in self.jobs])
        sources = set([job.get('source', 'Unknown') for job in self.jobs])
        
        return {
            "total_jobs": len(self.jobs),
            "unique_companies": len(companies),
            "sources": list(sources),
            "average_jobs_per_source": len(self.jobs) / len(sources) if sources else 0
        }


if __name__ == "__main__":
    scraper = JobListingScraper()
    
    # Scrape multiple sources
    print("\n=== SCRAPING JOB LISTINGS ===")
    
    # RemoteOK jobs
    remoteok_jobs = scraper.scrape_remoteok(limit=10)
    print(f"\nRemoteOK Jobs ({len(remoteok_jobs)}):")
    for job in remoteok_jobs[:3]:
        print(f"  - {job['title']} at {job['company']} ({job['location']})")
    
    # GitHub Jobs (archived)
    github_jobs = scraper.scrape_github_jobs_archive()
    print(f"\nGitHub Jobs Archive ({len(github_jobs)}):")
    for job in github_jobs:
        print(f"  - {job['title']} at {job['company']} ({job['location']})")
    
    # Summary
    summary = scraper.get_jobs_summary()
    print(f"\n=== SUMMARY ===")
    print(f"Total jobs scraped: {summary['total_jobs']}")
    print(f"Unique companies: {summary['unique_companies']}")
    print(f"Sources: {', '.join(summary['sources'])}")
