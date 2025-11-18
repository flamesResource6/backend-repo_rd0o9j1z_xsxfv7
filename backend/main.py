from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Lead, ClickLog

app = FastAPI(title="Decoding The Unseen API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
    ,allow_headers=["*"]
)


class LeadIn(BaseModel):
    email: EmailStr
    source: Optional[str] = "website"


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.get("/test")
async def test_db():
    # verify we can query the db
    docs = await get_documents("lead", {}, limit=1)
    return {"ok": True, "count_sample": len(docs)}


@app.post("/leads")
async def create_lead(payload: LeadIn):
    data = payload.model_dump()
    data["created_at"] = datetime.utcnow()
    try:
        doc_id = await create_document("lead", data)
        return {"ok": True, "id": str(doc_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ClickLogIn(BaseModel):
    product: str
    ref: Optional[str] = None


@app.post("/clicks")
async def log_click(payload: ClickLogIn):
    data = payload.model_dump()
    data["created_at"] = datetime.utcnow()
    try:
        _id = await create_document("clicklog", data)
        return {"ok": True, "id": str(_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
