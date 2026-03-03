import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.models.transcript import Signal, Transcript

TEST_DATABASE_URL = "sqlite:///./test_earnings.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)

def test_health(client):
    assert client.get("/health").status_code == 200

def test_list_signals_empty(client):
    assert client.get("/api/signals/").json() == []

def test_analyze_transcript(client):
    r = client.post("/api/signals/analyze", json={
        "ticker": "AAPL", "quarter": "Q1", "year": 2024,
        "content": "We are extremely pleased with our record results this quarter. Revenue exceeded expectations and we are raising guidance significantly. Management feels very confident about the pipeline ahead and sees strong demand continuing into next year. We expect momentum to accelerate substantially."
    })
    assert r.status_code == 201
    data = r.json()
    assert data["ticker"] == "AAPL"
    assert data["signal_label"] in ("bullish", "bearish", "neutral")

def test_fetch_known_ticker(client):
    r = client.get("/api/signals/fetch/NVDA?quarter=Q1&year=2024")
    assert r.status_code == 201
    assert r.json()["ticker"] == "NVDA"

def test_delete_signal(client):
    db = TestingSessionLocal()
    t = Transcript(ticker="TSLA", quarter="Q2", year=2024, content="test content here for the transcript entry minimum length", word_count=10)
    db.add(t); db.commit(); db.refresh(t)
    sig = Signal(transcript_id=t.id, ticker="TSLA", quarter="Q2", year=2024, composite_score=0.6, signal_label="bullish")
    db.add(sig); db.commit(); db.refresh(sig)
    sid = sig.id
    db.close()
    assert client.delete(f"/api/signals/{sid}").status_code == 204

def test_backtest_empty(client):
    r = client.get("/api/signals/backtest/run")
    assert r.status_code == 200
    assert r.json()["total_signals"] == 0

def test_signal_not_found(client):
    assert client.delete("/api/signals/999").status_code == 404
