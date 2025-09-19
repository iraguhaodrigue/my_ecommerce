from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLAlCHAMY_DATABASE_URL='sqlite:///./Blog.db'

engine = create_engine (SQLAlCHAMY_DATABASE_URL, connect_args={"check_same_thread": False})

sessionLOcal = sessionmaker(bind=engine,autocommit=False, autoflush=False,)

Base= declarative_base()

