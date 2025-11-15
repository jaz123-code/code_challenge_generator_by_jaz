from sqlalchemy import Column, Integer, String, ForeignKey,DateTime,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine=create_engine('sqlite:///example.db', echo=True)
Base = declarative_base()
class Challenge(Base):
    __tablename__ = 'challenges'
    
    id = Column(Integer, primary_key=True)
    difficulty = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=False)
    title= Column(String, nullable=False)
    options= Column(String, nullable=False)  # Comma-separated options
    correct_answer_id= Column(Integer, nullable=False)
    explanation= Column(String, nullable=True)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChallengeQuota(Base):
    __tablename__ = 'challenge_quotas'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, unique=True)
    quota_remaining = Column(Integer, nullable=False, default=50)
    last_reset_date = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

