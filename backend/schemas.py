from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Lead schema (emails captured)
class Lead(BaseModel):
    email: EmailStr
    source: Optional[str] = Field(default="website")
    created_at: Optional[datetime] = None

# Product purchase intent / click logs (optional)
class ClickLog(BaseModel):
    product: str
    ref: Optional[str] = None
    created_at: Optional[datetime] = None
