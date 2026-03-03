from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Transcript(Base):
    __tablename__ = "transcripts"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    company_name = Column(String(200), nullable=True)
    quarter = Column(String(10), nullable=False)
    year = Column(Integer, nullable=False)
    filing_date = Column(String(20), nullable=True)
    content = Column(Text, nullable=False)
    word_count = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Signal(Base):
    __tablename__ = "signals"
    id = Column(Integer, primary_key=True, index=True)
    transcript_id = Column(Integer, nullable=False)
    ticker = Column(String(10), nullable=False, index=True)
    quarter = Column(String(10), nullable=False)
    year = Column(Integer, nullable=False)
    confidence_score = Column(Float, nullable=True)
    hedging_score = Column(Float, nullable=True)
    guidance_score = Column(Float, nullable=True)
    risk_score = Column(Float, nullable=True)
    composite_score = Column(Float, nullable=True)
    signal_label = Column(String(20), nullable=True)
    raw_llm_response = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BacktestResult(Base):
    __tablename__ = "backtest_results"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False)
    quarter = Column(String(10), nullable=False)
    year = Column(Integer, nullable=False)
    composite_score = Column(Float, nullable=True)
    signal_direction = Column(String(10), nullable=True)
    return_1d = Column(Float, nullable=True)
    return_5d = Column(Float, nullable=True)
    actual_direction_1d = Column(String(10), nullable=True)
    actual_direction_5d = Column(String(10), nullable=True)
    correct_1d = Column(Integer, nullable=True)
    correct_5d = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
