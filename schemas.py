"""
Database Schemas for Decoding The Unseen

Each Pydantic model = one MongoDB collection (lowercased class name).
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

class Lead(BaseModel):
    email: EmailStr = Field(..., description="Subscriber email")
    source: Optional[str] = Field(None, description="Where the lead came from (e.g., hero, products, footer)")

class ClickLog(BaseModel):
    url: str = Field(..., description="Destination URL that was clicked")
    label: Optional[str] = Field(None, description="Human label for the click (e.g., Buy Now - Money Wizard)")
    source: Optional[str] = Field(None, description="UI source location (e.g., hero, products)")
    context: Optional[Dict[str, Any]] = Field(None, description="Extra context such as price, product id, etc.")
