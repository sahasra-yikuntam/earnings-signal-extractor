from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.transcript import Transcript, Signal, BacktestResult
from app.models.schemas import SignalOut, TranscriptOut, AnalyzeRequest, BacktestResultOut
from app.services.llm_extractor import extract_signal
from app.services.backtest import run_backtest
from app.services.edgar import fetch_transcript, get_company_name

router = APIRouter(prefix="/api/signals", tags=["signals"])

@router.post("/analyze", response_model=SignalOut, status_code=201)
async def analyze_transcript(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    t = Transcript(ticker=payload.ticker.upper(), quarter=payload.quarter, year=payload.year,
        content=payload.content, word_count=len(payload.content.split()),
        company_name=get_company_name(payload.ticker))
    db.add(t); db.commit(); db.refresh(t)
    scores = await extract_signal(payload.content, payload.ticker)
    sig = Signal(transcript_id=t.id, ticker=payload.ticker.upper(),
        quarter=payload.quarter, year=payload.year,
        confidence_score=scores.get("confidence_score"),
        hedging_score=scores.get("hedging_score"),
        guidance_score=scores.get("guidance_score"),
        risk_score=scores.get("risk_score"),
        composite_score=scores.get("composite_score"),
        signal_label=scores.get("signal_label"),
        raw_llm_response=scores)
    db.add(sig); db.commit(); db.refresh(sig)
    return sig

@router.get("/fetch/{ticker}", response_model=SignalOut, status_code=201)
async def fetch_and_analyze(ticker: str, quarter: str = "Q1", year: int = 2024, db: Session = Depends(get_db)):
    content = fetch_transcript(ticker.upper(), quarter, year)
    if not content:
        raise HTTPException(status_code=404, detail=f"No transcript found for {ticker}")
    t = Transcript(ticker=ticker.upper(), quarter=quarter, year=year,
        content=content, word_count=len(content.split()),
        company_name=get_company_name(ticker))
    db.add(t); db.commit(); db.refresh(t)
    scores = await extract_signal(content, ticker)
    sig = Signal(transcript_id=t.id, ticker=ticker.upper(), quarter=quarter, year=year,
        confidence_score=scores.get("confidence_score"),
        hedging_score=scores.get("hedging_score"),
        guidance_score=scores.get("guidance_score"),
        risk_score=scores.get("risk_score"),
        composite_score=scores.get("composite_score"),
        signal_label=scores.get("signal_label"),
        raw_llm_response=scores)
    db.add(sig); db.commit(); db.refresh(sig)
    return sig

@router.get("/", response_model=List[SignalOut])
def list_signals(db: Session = Depends(get_db)):
    return db.query(Signal).order_by(Signal.created_at.desc()).all()

@router.get("/transcripts", response_model=List[TranscriptOut])
def list_transcripts(db: Session = Depends(get_db)):
    return db.query(Transcript).order_by(Transcript.created_at.desc()).all()

@router.get("/backtest/run")
def run_backtest_endpoint(db: Session = Depends(get_db)):
    return run_backtest(db)

@router.get("/backtest/results", response_model=List[BacktestResultOut])
def get_backtest_results(db: Session = Depends(get_db)):
    return db.query(BacktestResult).order_by(BacktestResult.created_at.desc()).all()

@router.delete("/{signal_id}", status_code=204)
def delete_signal(signal_id: int, db: Session = Depends(get_db)):
    sig = db.query(Signal).filter(Signal.id == signal_id).first()
    if not sig:
        raise HTTPException(status_code=404, detail="Signal not found")
    db.delete(sig); db.commit()
