from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.api.signals import router as signals_router

app = FastAPI(title="Earnings Signal Extractor", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000","http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(signals_router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok", "service": "earnings-signal-extractor"}
