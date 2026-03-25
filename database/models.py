from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

os.makedirs("database", exist_ok=True)

engine = create_engine("sqlite:///database/analysis.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    original_name = Column(String(255))
    file_type = Column(String(50))
    row_count = Column(Integer)
    col_count = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer)
    role = Column(String(20))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer)
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(engine)