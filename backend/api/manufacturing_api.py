"""
FastAPI endpoints for Manufacturing Operations Platform
Integrates AI-powered quality planning and machine recommendations
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.quality_standards_trainer import QualityStandardsTrainer, MachineRecommendationEngine
import sqlite3
import json
import uuid

app = FastAPI(
    title="Manufacturing Operations API",
    description="AI-powered quality planning and machine recommendations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI engines
quality_trainer = QualityStandardsTrainer(db_path="database/manufacturing.db")
machine_engine = MachineRecommendationEngine(db_path="database/manufacturing.db")

# Request/Response Models
class CADUploadRequest(BaseModel):
    partName: str
    material: str
    volume: int
    dimensions: Optional[Dict[str, float]] = None
    features: Optional[List[str]] = None
    tolerances: Optional[List[Dict]] = None


class QualityPlanRequest(BaseModel):
    partDescription: str
    material: str
    industry: str
    tolerances: List[Dict]
    annualVolume: int


class MachineRecommendationRequest(BaseModel):
    partDimensions: Dict[str, float]
    material: str
    requiredOperations: List[str]
    annualVolume: int
    tolerance: float


class AnalysisResponse(BaseModel):
    analysisId: str
    status: str
    message: str


class QualityPlanResponse(BaseModel):
    planId: str
    templateUsed: str
    description: str
    relevantStandards: List[Dict]
    inspectionPoints: List[Dict]
    controlMethods: List[str]
    acceptanceCriteria: Dict
    documentationRequirements: List[str]
    aiRecommendations: List[str]
    estimatedInvestment: float


class MachineRecommendation(BaseModel):
    id: int
    name: str
    manufacturer: str
    model: str
    category: str
    price: float
    tolerance: float
    automationLevel: str
    leadTimeWeeks: int
    score: int
    reasons: List[str]
    capabilities: List[str]


# Database helper
def get_db_connection():
    return sqlite3.connect('database/manufacturing.db')


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Manufacturing Operations API",
        "status": "operational",
        "version": "1.0.0"
    }


@app.post("/api/cad/upload", response_model=AnalysisResponse)
async def upload_cad(
    partName: str = Form(...),
    material: str = Form(...),
    volume: int = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Upload CAD files and initiate analysis
    """
    # Generate analysis ID
    analysis_id = str(uuid.uuid4())

    # In production, you would:
    # 1. Save uploaded files
    # 2. Extract features from CAD files (using libraries like pythonOCC, cadquery)
    # 3. Run AI analysis

    # For now, simulate processing
    conn = get_db_connection()
    cursor = conn.cursor()

    # Store analysis record
    cursor.execute("""
        INSERT INTO cad_analyses (analysis_id, part_name, material, annual_volume, status)
        VALUES (?, ?, ?, ?, ?)
    """, (analysis_id, partName, material, volume, 'PROCESSING'))

    conn.commit()
    conn.close()

    return AnalysisResponse(
        analysisId=analysis_id,
        status="PROCESSING",
        message=f"CAD files uploaded successfully. Processing {len(files)} files."
    )


@app.get("/api/cad/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Get CAD analysis results
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT analysis_id, part_name, material, annual_volume, complexity_score,
               recommended_machines, estimated_cycle_time, status
        FROM cad_analyses
        WHERE analysis_id = ?
    """, (analysis_id,))

    result = cursor.fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")

    # Simulate completion (in production, check actual processing status)
    return {
        "analysisId": result[0],
        "partName": result[1],
        "material": result[2],
        "annualVolume": result[3],
        "status": "COMPLETED",
        "complexityScore": result[4] or 75.0,
        "recommendedMachines": json.loads(result[5]) if result[5] else [],
        "estimatedCycleTime": result[6] or 30.0
    }


@app.post("/api/quality/plan", response_model=QualityPlanResponse)
async def generate_quality_plan(request: QualityPlanRequest):
    """
    Generate AI-powered quality control plan
    """
    # Use AI to generate quality plan
    quality_plan = quality_trainer.generate_quality_plan_recommendations(
        part_description=request.partDescription,
        material=request.material,
        industry=request.industry,
        tolerances=request.tolerances
    )

    if 'error' in quality_plan:
        raise HTTPException(status_code=400, detail=quality_plan['error'])

    # Calculate estimated investment
    # Get recommended machines and quality tools
    machine_recommendations = machine_engine.recommend_machines(
        part_dimensions={'x': 200, 'y': 100, 'z': 100},  # Would come from CAD analysis
        material=request.material,
        required_operations=['TURNING', 'MILLING'],  # Would be determined by part features
        annual_volume=request.annualVolume,
        tolerance=min([t.get('tolerance', 0.1) for t in request.tolerances])
    )

    # Sum up investment
    total_investment = 0
    if machine_recommendations:
        # Primary and secondary machines
        total_investment = sum(m['price'] for m in machine_recommendations[:2])

    # Add quality inspection equipment (CMM)
    total_investment += 125000  # Typical CMM cost

    # Generate plan ID
    plan_id = str(uuid.uuid4())

    return QualityPlanResponse(
        planId=plan_id,
        templateUsed=quality_plan['template_used'],
        description=quality_plan['description'],
        relevantStandards=quality_plan['relevant_standards'],
        inspectionPoints=quality_plan['inspection_points'],
        controlMethods=quality_plan['control_methods'],
        acceptanceCriteria=quality_plan['acceptance_criteria'],
        documentationRequirements=quality_plan['documentation_requirements'],
        aiRecommendations=quality_plan['ai_recommendations'],
        estimatedInvestment=total_investment
    )


@app.post("/api/machines/recommend")
async def recommend_machines(request: MachineRecommendationRequest):
    """
    Get AI-powered machine recommendations
    """
    recommendations = machine_engine.recommend_machines(
        part_dimensions=request.partDimensions,
        material=request.material,
        required_operations=request.requiredOperations,
        annual_volume=request.annualVolume,
        tolerance=request.tolerance
    )

    return {
        "recommendations": recommendations,
        "totalRecommendations": len(recommendations)
    }


@app.get("/api/machines")
async def list_machines(
    category: Optional[str] = None,
    material: Optional[str] = None,
    max_price: Optional[float] = None
):
    """
    List available machines with optional filters
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, name, manufacturer, model, category, price, tolerance,
               automation_level, lead_time_weeks, description
        FROM machines
        WHERE is_available = 1
    """
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if max_price:
        query += " AND price <= ?"
        params.append(max_price)

    cursor.execute(query, params)
    machines = cursor.fetchall()
    conn.close()

    return {
        "machines": [
            {
                "id": m[0],
                "name": m[1],
                "manufacturer": m[2],
                "model": m[3],
                "category": m[4],
                "price": m[5],
                "tolerance": m[6],
                "automationLevel": m[7],
                "leadTimeWeeks": m[8],
                "description": m[9]
            }
            for m in machines
        ]
    }


@app.get("/api/quality/standards")
async def list_quality_standards(
    industry: Optional[str] = None,
    category: Optional[str] = None
):
    """
    List quality standards with optional filters
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT standard_id, title, organization, category, summary FROM quality_standards"
    params = []
    conditions = []

    if category:
        conditions.append("category = ?")
        params.append(category)

    if industry:
        conditions.append("json_extract(industry, '$') LIKE ?")
        params.append(f'%"{industry}"%')

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    standards = cursor.fetchall()
    conn.close()

    return {
        "standards": [
            {
                "standardId": s[0],
                "title": s[1],
                "organization": s[2],
                "category": s[3],
                "summary": s[4]
            }
            for s in standards
        ]
    }


@app.get("/api/quality/standards/search")
async def search_quality_standards(query: str, industry: Optional[str] = None):
    """
    AI-powered search for relevant quality standards
    """
    relevant_standards = quality_trainer.find_relevant_standards(
        query=query,
        industry=industry,
        top_k=10
    )

    return {
        "query": query,
        "results": relevant_standards
    }


@app.post("/api/production/quality-data")
async def log_quality_data(data: Dict):
    """
    Log quality measurement data
    """
    # In production, this would store to database and trigger SPC analysis
    data_id = str(uuid.uuid4())

    # Simulate storing data
    return {
        "dataId": data_id,
        "status": "recorded",
        "timestamp": datetime.utcnow().isoformat(),
        "alerts": []  # Would contain any out-of-spec alerts
    }


@app.get("/api/production/metrics")
async def get_production_metrics():
    """
    Get real-time production metrics
    """
    # In production, this would query actual production data
    import random

    return {
        "oee": round(85 + random.uniform(-5, 10), 1),
        "partsToday": 142 + random.randint(-10, 20),
        "hoursToMaintenance": 23,
        "currentCpk": 1.45,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/analytics/spc")
async def get_spc_data(
    feature: str = "boreDiameter",
    limit: int = 100
):
    """
    Get SPC chart data
    """
    # In production, query actual measurement data
    import numpy as np

    target = 25.000
    measurements = []
    for i in range(limit):
        value = target + np.random.normal(0, 0.002)
        measurements.append({
            "timestamp": datetime.utcnow().isoformat(),
            "value": round(value, 4),
            "operator": ["John Smith", "Maria Garcia", "David Chen"][i % 3]
        })

    return {
        "feature": feature,
        "measurements": measurements,
        "controlLimits": {
            "ucl": 25.005,
            "lcl": 24.995,
            "target": 25.000
        },
        "cpk": 1.45
    }


@app.get("/api/analytics/insights")
async def get_ai_insights():
    """
    Get AI-powered production insights
    """
    return {
        "insights": [
            {
                "type": "trend",
                "severity": "warning",
                "message": "Bore diameter showing slight upward drift over last 50 parts",
                "recommendation": "Schedule tool replacement within 20 parts",
                "timestamp": datetime.utcnow().isoformat()
            },
            {
                "type": "root_cause",
                "severity": "info",
                "message": "Increased variation in overall length during Shift B",
                "recommendation": "Investigate coolant system on VF-3",
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    }


@app.post("/api/ai/train")
async def train_models():
    """
    Trigger AI model training on quality standards
    """
    try:
        quality_trainer.train_on_quality_standards()
        return {
            "status": "success",
            "message": "Quality standards model training completed",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Startup Event
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("\n" + "="*60)
    print("🚀 Manufacturing Operations API Starting...")
    print("="*60)

    # Initialize AI model
    quality_trainer.initialize_model()

    print("\n✅ API Ready!")
    print("📊 Endpoints available at: http://localhost:8000/docs")
    print("="*60 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
