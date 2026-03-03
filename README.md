# Earnings Signal Extractor

An alternative data pipeline that uses LLMs to extract sentiment signals from SEC earnings call transcripts, then backtests whether those signals predict short-term post-earnings stock returns.

## What It Does

1. Transcript Ingestion - Pulls earnings call transcripts from SEC EDGAR
2. LLM Signal Extraction - Scores management tone on Confidence, Hedging, Guidance, and Risk
3. Alpha Signal Generation - Combines scores into a composite signal per ticker
4. Backtesting Engine - Tests signal predictive power against post-earnings returns
5. Analytics Dashboard - Visualizes Sharpe ratio, hit rate, and signal distribution

## Tech Stack

Python / FastAPI / React / SQLite / Anthropic API / OpenAI API / SEC EDGAR / Docker / GitHub Actions

## Quick Start

    git clone https://github.com/sahasra-yikuntam/earnings-signal-extractor.git
    cd earnings-signal-extractor
    cp .env.example .env
    cd backend && pip install -r requirements.txt
    uvicorn app.main:app --reload

In another terminal:

    cd frontend && npm install && npm run dev

Built by Sahasra Yikuntam - Ohio State University - NSF Imageomics Institute
