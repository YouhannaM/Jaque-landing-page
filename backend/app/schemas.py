from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class DemoRequestCreate(BaseModel):
    """Schema for creating a demo request"""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    company: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., min_length=1, max_length=100)
    message: Optional[str] = None


class DemoRequestResponse(BaseModel):
    """Schema for demo request response"""
    id: int
    name: str
    email: str
    company: str
    role: str
    message: Optional[str]
    status: str
    contacted: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
