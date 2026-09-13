import os
from typing import Optional
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL Setup
class PostgreSQLSetup:
    """
    PostgreSQL database setup for career guidance platform
    """
    
    @staticmethod
    def get_connection_string() -> str:
        """
        Get PostgreSQL connection string from environment variables
        """
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', 'password')
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        database = os.getenv('DB_NAME', 'career_guidance')
        
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    @staticmethod
    def get_create_tables_sql() -> str:
        """
        SQL to create all necessary tables
        """
        return """
        -- Occupations table (O*NET data)
        CREATE TABLE IF NOT EXISTS occupations (
            id SERIAL PRIMARY KEY,
            onet_code VARCHAR(10) UNIQUE NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            salary_min DECIMAL(10, 2),
            salary_max DECIMAL(10, 2),
            job_outlook VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Skills table
        CREATE TABLE IF NOT EXISTS skills (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            category VARCHAR(100),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Occupation-Skill relationship
        CREATE TABLE IF NOT EXISTS occupation_skills (
            occupation_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            importance_level VARCHAR(50),
            PRIMARY KEY (occupation_id, skill_id),
            FOREIGN KEY (occupation_id) REFERENCES occupations(id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
        );

        -- Job listings table
        CREATE TABLE IF NOT EXISTS job_listings (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            company VARCHAR(255),
            location VARCHAR(255),
            description TEXT,
            url VARCHAR(2000),
            source VARCHAR(100),
            salary_min DECIMAL(10, 2),
            salary_max DECIMAL(10, 2),
            job_type VARCHAR(50),
            posted_at TIMESTAMP,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT true
        );

        -- Job-Skill relationship
        CREATE TABLE IF NOT EXISTS job_skills (
            job_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            PRIMARY KEY (job_id, skill_id),
            FOREIGN KEY (job_id) REFERENCES job_listings(id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
        );

        -- User profiles
        CREATE TABLE IF NOT EXISTS user_profiles (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(255),
            experience_years INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- User skills
        CREATE TABLE IF NOT EXISTS user_skills (
            user_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            proficiency_level VARCHAR(50),
            PRIMARY KEY (user_id, skill_id),
            FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
        );

        -- Career recommendations
        CREATE TABLE IF NOT EXISTS career_recommendations (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            occupation_id INTEGER NOT NULL,
            match_score DECIMAL(3, 1),
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE CASCADE,
            FOREIGN KEY (occupation_id) REFERENCES occupations(id) ON DELETE CASCADE
        );

        -- Create indexes for performance
        CREATE INDEX IF NOT EXISTS idx_occupations_title ON occupations(title);
        CREATE INDEX IF NOT EXISTS idx_job_listings_company ON job_listings(company);
        CREATE INDEX IF NOT EXISTS idx_job_listings_location ON job_listings(location);
        CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email);
        """
    
    @staticmethod
    def create_sample_data_sql() -> str:
        """
        SQL to insert sample data
        """
        return """
        -- Insert sample skills
        INSERT INTO skills (name, category, description) VALUES
        ('Python', 'Technical', 'Python programming language'),
        ('JavaScript', 'Technical', 'JavaScript programming language'),
        ('React', 'Technical', 'React JavaScript library'),
        ('Project Management', 'Management', 'Ability to manage projects'),
        ('Communication', 'Soft Skills', 'Ability to communicate effectively'),
        ('Leadership', 'Soft Skills', 'Ability to lead teams'),
        ('Data Analysis', 'Technical', 'Analyzing and interpreting data'),
        ('SQL', 'Technical', 'SQL database language')
        ON CONFLICT (name) DO NOTHING;

        -- Insert sample occupations
        INSERT INTO occupations (onet_code, title, description, salary_min, salary_max, job_outlook) VALUES
        ('15-1132.00', 'Software Developers', 'Develop and maintain software applications', 80000, 160000, 'Grow 17%'),
        ('11-1011.00', 'Chief Executives', 'Determine and formulate organizational policies', 100000, 250000, 'Grow 8%'),
        ('13-1111.00', 'Management Analysts', 'Conduct organizational studies and design systems', 60000, 130000, 'Grow 11%'),
        ('29-1141.00', 'Registered Nurses', 'Provide patient healthcare and support', 50000, 90000, 'Grow 6%')
        ON CONFLICT (onet_code) DO NOTHING;
        """


# MongoDB Setup (Alternative)
class MongoDBSetup:
    """
    MongoDB setup for career guidance platform (NoSQL alternative)
    """
    
    @staticmethod
    def get_connection_string() -> str:
        """
        Get MongoDB connection string from environment variables
        """
        user = os.getenv('MONGO_USER', 'user')
        password = os.getenv('MONGO_PASSWORD', 'password')
        host = os.getenv('MONGO_HOST', 'localhost')
        port = os.getenv('MONGO_PORT', '27017')
        database = os.getenv('MONGO_DB', 'career_guidance')
        
        if user and password:
            return f"mongodb+srv://{user}:{password}@{host}/{database}"
        else:
            return f"mongodb://{host}:{port}/{database}"
    
    @staticmethod
    def get_collections_schema() -> dict:
        """
        MongoDB collections and their schema
        """
        return {
            "occupations": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["onet_code", "title"],
                        "properties": {
                            "onet_code": {"bsonType": "string"},
                            "title": {"bsonType": "string"},
                            "description": {"bsonType": "string"},
                            "salary_min": {"bsonType": "double"},
                            "salary_max": {"bsonType": "double"},
                            "job_outlook": {"bsonType": "string"},
                            "skills": {"bsonType": "array"},
                            "created_at": {"bsonType": "date"}
                        }
                    }
                }
            },
            "job_listings": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["title", "company"],
                        "properties": {
                            "title": {"bsonType": "string"},
                            "company": {"bsonType": "string"},
                            "location": {"bsonType": "string"},
                            "description": {"bsonType": "string"},
                            "url": {"bsonType": "string"},
                            "source": {"bsonType": "string"},
                            "salary_min": {"bsonType": "double"},
                            "salary_max": {"bsonType": "double"},
                            "skills": {"bsonType": "array"},
                            "scraped_at": {"bsonType": "date"}
                        }
                    }
                }
            },
            "user_profiles": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["email"],
                        "properties": {
                            "email": {"bsonType": "string"},
                            "name": {"bsonType": "string"},
                            "skills": {"bsonType": "array"},
                            "experience_years": {"bsonType": "int"},
                            "created_at": {"bsonType": "date"}
                        }
                    }
                }
            }
        }


# Database initialization
def init_database():
    """
    Initialize database based on DB_TYPE environment variable
    """
    db_type = os.getenv('DB_TYPE', 'postgresql').lower()
    
    if db_type == 'postgresql':
        logger.info("Using PostgreSQL")
        connection_string = PostgreSQLSetup.get_connection_string()
        logger.info(f"Connection string: {connection_string}")
        logger.info("\nSQL to create tables:")
        print(PostgreSQLSetup.get_create_tables_sql())
        
    elif db_type == 'mongodb':
        logger.info("Using MongoDB")
        connection_string = MongoDBSetup.get_connection_string()
        logger.info(f"Connection string: {connection_string}")
        logger.info("\nMongoDB schema:")
        print(json.dumps(MongoDBSetup.get_collections_schema(), indent=2))
    
    else:
        logger.error(f"Unknown database type: {db_type}")


if __name__ == "__main__":
    init_database()
