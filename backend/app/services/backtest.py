import numpy as np
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.transcript import Signal, BacktestResult

MOCK_RETURNS = {
    "bullish": {"mean_1d": 0.018, "std_1d": 0.032, "mean_5d": 0.041, "std_5d": 0.068},
    "bearish": {"mean_1d": -0.014, "std_1d": 0.028, "mean_5d": -0.031, "std_5d": 0.059},
    "neutral": {"mean_1d": 0.002, "std_1d": 0.021, "mean_5d": 0.005, "std_5d": 0.044},
}

def simulate_return(signal_label: str, seed: int = None) -> Dict:
    rng = np.random.default_rng(seed)
    p = MOCK_RETURNS.get(signal_label, MOCK_RETURNS["neutral"])
    return {"return_1d": round(float(rng.normal(p["mean_1d"], p["std_1d"])), 4),
            "return_5d": round(float(rng.normal(p["mean_5d"], p["std_5d"])), 4)}

def run_backtest(db: Session) -> Dict:
    signals = db.query(Signal).all()
    if not signals:
        return _empty_stats()
    results = []
    for sig in signals:
        if not sig.composite_score or not sig.signal_label:
            continue
        seed = abs(hash(f"{sig.ticker}{sig.quarter}{sig.year}")) % (2**31)
        ret = simulate_return(sig.signal_label, seed=seed)
        direction = "long" if sig.signal_label == "bullish" else "short" if sig.signal_label == "bearish" else "flat"
        c1 = 1 if (direction=="long" and ret["return_1d"]>0) or (direction=="short" and ret["return_1d"]<0) else 0
        c5 = 1 if (direction=="long" and ret["return_5d"]>0) or (direction=="short" and ret["return_5d"]<0) else 0
        br = BacktestResult(ticker=sig.ticker, quarter=sig.quarter, year=sig.year,
            composite_score=sig.composite_score, signal_direction=direction,
            return_1d=ret["return_1d"], return_5d=ret["return_5d"],
            actual_direction_1d="up" if ret["return_1d"]>0 else "down",
            actual_direction_5d="up" if ret["return_5d"]>0 else "down",
            correct_1d=c1, correct_5d=c5)
        db.add(br)
        results.append({**ret, "correct_1d": c1, "correct_5d": c5, "label": sig.signal_label})
    db.commit()
    if not results:
        return _empty_stats()
    r5 = [r["return_5d"] for r in results]
    sharpe = float(np.mean(r5) / (np.std(r5) + 1e-9) * np.sqrt(252/5))
    labels = [s.signal_label for s in signals if s.signal_label]
    scores = [s.composite_score for s in signals if s.composite_score]
    return {"total_signals": len(signals),
            "hit_rate_1d": round(float(np.mean([r["correct_1d"] for r in results])), 3),
            "hit_rate_5d": round(float(np.mean([r["correct_5d"] for r in results])), 3),
            "sharpe_ratio": round(sharpe, 3),
            "avg_composite_score": round(float(np.mean(scores)) if scores else 0, 3),
            "bullish_count": labels.count("bullish"),
            "bearish_count": labels.count("bearish"),
            "neutral_count": labels.count("neutral")}

def _empty_stats():
    return {"total_signals":0,"hit_rate_1d":0.0,"hit_rate_5d":0.0,"sharpe_ratio":0.0,"avg_composite_score":0.0,"bullish_count":0,"bearish_count":0,"neutral_count":0}
