import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# .env file nundi variables load cheyadaniki
load_dotenv()

import urllib.parse

# Support both individual variables and cloud-provided DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
connect_args = {}

if DATABASE_URL:
    if DATABASE_URL.startswith("mysql://"):
        DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
    if "aivencloud.com" in DATABASE_URL or "ssl-mode=" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.split("?")[0]
        connect_args = {"ssl": {"check_hostname": False}}
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = urllib.parse.quote_plus(os.getenv("DB_PASSWORD") or "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "restaurant_db")
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

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
