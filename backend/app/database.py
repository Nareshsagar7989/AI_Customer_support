import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# .env file nundi variables load cheyadaniki
load_dotenv()

# Variables thechukuntunnam
DB_USER = os.getenv("DB_USER")
import urllib.parse
DB_PASSWORD = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Database URL create chesthunnam
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Database tho matladadaniki Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Mana models anni deeni nundi inherit avthayi
Base = declarative_base()

# Database connect ayyi work aypoyaka close chese function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
