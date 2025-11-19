import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

from database import db, create_document
from schemas import Lead, ClickLog

app = FastAPI(title="Decoding The Unseen API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/leads")
def capture_lead(lead: Lead):
    try:
        inserted_id = create_document("lead", lead)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clicks")
def log_click(click: ClickLog):
    try:
        inserted_id = create_document("clicklog", click)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_db():
    resp = {
        "db": "connected" if db is not None else "not_configured",
        "has_env": bool(os.getenv("DATABASE_URL")) and bool(os.getenv("DATABASE_NAME"))
    }
    return resp

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
