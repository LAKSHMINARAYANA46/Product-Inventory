from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
url = "postgresql+psycopg2://postgres:lux810@localhost:5432/postgres"
engine = create_engine(url)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def create_tables():
    Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()