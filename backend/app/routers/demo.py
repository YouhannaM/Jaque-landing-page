from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import DemoRequest
from ..schemas import DemoRequestCreate, DemoRequestResponse, MessageResponse

router = APIRouter(
    prefix="/api/demo",
    tags=["demo"]
)


@router.post("/request", response_model=MessageResponse, status_code=201)
async def create_demo_request(
    demo_request: DemoRequestCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new demo request from the landing page
    """
    try:
        # Create new demo request
        db_demo = DemoRequest(
            name=demo_request.name,
            email=demo_request.email,
            company=demo_request.company,
            role=demo_request.role,
            message=demo_request.message,
            status="new",
            contacted=False
        )

        db.add(db_demo)
        db.commit()
        db.refresh(db_demo)

        return MessageResponse(
            message="Demo request submitted successfully! We'll be in touch within 24 hours.",
            success=True
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create demo request: {str(e)}"
        )


@router.get("/requests", response_model=List[DemoRequestResponse])
async def get_demo_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all demo requests (admin endpoint)
    """
    requests = db.query(DemoRequest).offset(skip).limit(limit).all()
    return requests


@router.get("/requests/{request_id}", response_model=DemoRequestResponse)
async def get_demo_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific demo request by ID
    """
    request = db.query(DemoRequest).filter(DemoRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Demo request not found")
    return request


@router.patch("/requests/{request_id}/status")
async def update_demo_request_status(
    request_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """
    Update the status of a demo request
    """
    request = db.query(DemoRequest).filter(DemoRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Demo request not found")

    request.status = status
    if status in ["contacted", "scheduled"]:
        request.contacted = True

    db.commit()
    db.refresh(request)

    return MessageResponse(
        message=f"Demo request status updated to: {status}",
        success=True
    )
