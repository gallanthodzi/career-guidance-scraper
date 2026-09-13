# Career Guidance Web Scraper

A comprehensive web scraper that combines **O*NET occupational data** with **real job listings** to build a career guidance database.

## Features

✅ **O*NET Data Scraper**
- 900+ official US occupations
- Salary ranges and job outlook
- Required skills and abilities
- Work activities and tasks

✅ **Multi-Source Job Scraper**
- RemoteOK API integration
- GitHub Jobs archived data
- We Work Remotely scraping
- Selenium support for JavaScript-heavy sites
- Automatic skill extraction

✅ **Database Setup**
- PostgreSQL schema included
- MongoDB alternative available
- Pre-built models and relationships

✅ **Data Export**
- JSON format
- CSV format
- Database-ready

## Project Structure

```
├── scrapers/
│   ├── onet_scraper.py          # O*NET data scraper
│   └── job_listing_scraper.py   # Job board scrapers
├── database/
│   ├── models.py                # Data models
│   └── db_setup.py              # Database initialization
├── main.py                      # Main entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/career-guidance-scraper.git
cd career-guidance-scraper
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 5. Run the scraper
```bash
python main.py
```

## Database Setup

### PostgreSQL Setup

```bash
# Create database
creatdb career_guidance

# Run initialization
python database/db_setup.py
```

Then execute the SQL from the output in your PostgreSQL client.

### MongoDB Setup

```bash
# Set in .env
DB_TYPE=mongodb

# Run initialization
python database/db_setup.py
```

## Usage Examples

### Scrape O*NET Data

```python
from scrapers.onet_scraper import ONetScraper

scraper = ONetScraper()
data = scraper.fetch_onet_data()

# Save to files
scraper.save_to_json('onet_data.json')
scraper.save_to_csv('occupations.csv')
```

### Scrape Job Listings

```python
from scrapers.job_listing_scraper import JobListingScraper

scraper = JobListingScraper()

# Scrape RemoteOK
remoteok_jobs = scraper.scrape_remoteok(limit=50)

# Scrape GitHub Jobs Archive
github_jobs = scraper.scrape_github_jobs_archive()

# Save all jobs
scraper.save_jobs_to_json('jobs.json')

# Get summary
summary = scraper.get_jobs_summary()
print(f"Total jobs: {summary['total_jobs']}")
```

### Selenium Scraping (Advanced)

```python
jobs = scraper.scrape_with_selenium(
    url="https://example-job-board.com",
    job_selector=".job-listing"
)
```

## API Endpoints (For Future Backend)

Once integrated with a backend framework:

```
GET    /api/occupations          - List all occupations
GET    /api/occupations/:id      - Get occupation details
GET    /api/jobs                 - List job listings
GET    /api/jobs/search          - Search jobs (title, skills, location)
GET    /api/recommendations      - Get career recommendations
POST   /api/users/profile        - Create user profile
GET    /api/skills               - List all skills
```

## Technologies Used

- **Web Scraping**: BeautifulSoup4, Selenium, Requests
- **Data Processing**: Pandas
- **Databases**: PostgreSQL, MongoDB
- **Data Format**: JSON, CSV
- **Testing**: pytest (future)

## Data Sources

1. **O*NET (Occupational Information Network)**
   - Source: https://www.onetcenter.org/
   - Data: 900+ occupations, skills, abilities, work activities
   - License: Public Domain

2. **RemoteOK**
   - Source: https://remoteok.io/api
   - Data: Remote job listings

3. **GitHub Jobs (Archived)**
   - Source: Archive/cached data
   - Note: GitHub Jobs was shut down but data is available

4. **We Work Remotely**
   - Source: https://weworkremotely.com/
   - Data: Remote job listings

## Legal & Ethical Considerations

⚠️ **Important:**
- Always check website's `robots.txt` and Terms of Service
- Add delays between requests to avoid overloading servers
- Respect rate limits on APIs
- Get permission before scraping if required
- O*NET data is public domain and free to use

## Configuration

### Environment Variables

```
DB_TYPE              # postgresql or mongodb
DB_USER              # Database username
DB_PASSWORD          # Database password
DB_HOST              # Database host
DB_PORT              # Database port
DB_NAME              # Database name
SCRAPER_DELAY        # Delay between requests (seconds)
SELENIUM_HEADLESS    # Run Selenium in headless mode
```

## Troubleshooting

### Selenium Chrome Driver Issues
```bash
# Install chromium-chromedriver
sudo apt-get install chromium-chromedriver  # Linux
brew install chromedriver                    # macOS
# Or download from: https://chromedriver.chromium.org/
```

### Database Connection Issues
- Verify PostgreSQL/MongoDB is running
- Check credentials in `.env`
- Test connection: `psql -U user -h localhost -d career_guidance`

### Request Timeouts
- Increase `SCRAPER_DELAY` in `.env`
- Check internet connection
- Some sites may block scrapers

## Future Enhancements

- [ ] Backend API (Flask/Django/FastAPI)
- [ ] Frontend (React/Vue)
- [ ] User authentication
- [ ] Job recommendations algorithm
- [ ] Email notifications
- [ ] Scheduled scraping with APScheduler
- [ ] Data caching with Redis
- [ ] API rate limiting
- [ ] Unit tests and CI/CD
- [ ] Docker containerization

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation
- Review error logs in the console output

---

**Built with ❤️ for career guidance and job discovery**
