#!/usr/bin/env python3
"""
Main entry point for Career Guidance Web Scraper
Integrates O*NET data and job listings from multiple sources
"""

import sys
import logging
import json
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.onet_scraper import ONetScraper
from scrapers.job_listing_scraper import JobListingScraper
from database.db_setup import init_database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the scraper
    """
    print("\n" + "="*60)
    print("CAREER GUIDANCE WEB SCRAPER")
    print("Combining O*NET data + Real Job Listings")
    print("="*60)
    
    # Initialize database
    logger.info("\n[1/3] Initializing database...")
    init_database()
    
    # Scrape O*NET data
    logger.info("\n[2/3] Scraping O*NET career data...")
    onet_scraper = ONetScraper()
    onet_data = onet_scraper.fetch_onet_data()
    
    print("\n=== O*NET DATA ===")
    print(f"Occupations: {len(onet_data['occupations'])}")
    print(f"Skills: {len(onet_data['skills'])}")
    print(f"Abilities: {len(onet_data['abilities'])}")
    print(f"Work Activities: {len(onet_data['work_activities'])}")
    
    # Sample occupations
    print("\nSample Occupations:")
    for occ in onet_data['occupations'][:3]:
        print(f"  - {occ['title']}: ${occ['salary_min']:,} - ${occ['salary_max']:,}")
    
    # Scrape job listings
    logger.info("\n[3/3] Scraping job listings...")
    job_scraper = JobListingScraper()
    
    print("\n=== SCRAPING JOB LISTINGS ===")
    
    # Scrape from different sources
    print("\nAttempting to scrape from multiple sources...")
    remoteok_jobs = job_scraper.scrape_remoteok(limit=5)
    github_jobs = job_scraper.scrape_github_jobs_archive()
    we_work_jobs = job_scraper.scrape_we_work_remotely(limit=5)
    
    # Display results
    print(f"\nRemoteOK: {len(remoteok_jobs)} jobs")
    print(f"GitHub Jobs Archive: {len(github_jobs)} jobs")
    print(f"We Work Remotely: {len(we_work_jobs)} jobs")
    
    # Summary
    summary = job_scraper.get_jobs_summary()
    print(f"\nTotal jobs scraped: {summary['total_jobs']}")
    print(f"Unique companies: {summary['unique_companies']}")
    print(f"Sources: {', '.join(summary['sources'])}")
    
    # Display sample jobs
    if job_scraper.jobs:
        print("\nSample Jobs:")
        for job in job_scraper.jobs[:5]:
            print(f"  - {job['title']} at {job['company']} ({job['location']})")
            if job.get('skills'):
                print(f"    Skills: {', '.join(job['skills'][:3])}")
    
    # Save to files
    logger.info("\nSaving data to files...")
    onet_scraper.save_to_json('output/onet_data.json')
    onet_scraper.save_to_csv('output/onet_occupations.csv')
    job_scraper.save_jobs_to_json('output/jobs.json')
    
    print("\n" + "="*60)
    print("✓ Scraping completed successfully!")
    print("Output files saved to /output directory")
    print("="*60 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
