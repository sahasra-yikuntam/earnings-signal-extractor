from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AnalyzeRequest(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    content: str = Field(..., min_length=100)
    quarter: str = Field(default="Q1")
    year: int = Field(default=2024)

class SignalOut(BaseModel):
    id: int
    ticker: str
    quarter: str
    year: int
    confidence_score: Optional[float]
    hedging_score: Optional[float]
    guidance_score: Optional[float]
    risk_score: Optional[float]
    composite_score: Optional[float]
    signal_label: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class TranscriptOut(BaseModel):
    id: int
    ticker: str
    company_name: Optional[str]
    quarter: str
    year: int
    word_count: Optional[int]
    created_at: datetime
    class Config:
        from_attributes = True

class BacktestResultOut(BaseModel):
    id: int
    ticker: str
    quarter: str
    year: int
    composite_score: Optional[float]
    signal_direction: Optional[str]
    return_1d: Optional[float]
    return_5d: Optional[float]
    correct_1d: Optional[int]
    correct_5d: Optional[int]
    class Config:
        from_attributes = True
