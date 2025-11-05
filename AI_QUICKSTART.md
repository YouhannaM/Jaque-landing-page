# 🤖 AI-Powered Manufacturing Platform - Quick Start

## What's New

Your Manufacturing Operations Platform now includes:

✅ **Real Machine Database** - Actual CNC machines (Haas, DMG MORI, Mazak) with specs and pricing
✅ **Quality Standards AI** - Trained on ISO 9001, AS9100, ASME Y14.5, IATF 16949, ISO 13485
✅ **Smart Quality Planning** - AI generates quality control plans based on your requirements
✅ **Machine Recommendations** - AI recommends best equipment for your parts

## Setup (5 minutes)

### 1. Install Backend Dependencies

```bash
cd backend
chmod +x setup_ai_system.sh
./setup_ai_system.sh
```

This will:
- Create Python virtual environment
- Install AI/ML libraries (sentence-transformers, scikit-learn, etc.)
- Initialize database with 4 CNC machines and 6 quality standards
- Train AI models

### 2. Start the AI-Powered API

```bash
./start_api.sh
```

Or manually:
```bash
source venv/bin/activate
cd api
python3 manufacturing_api.py
```

The API will start on **http://localhost:8000**

### 3. View API Documentation

Open your browser to:
```
http://localhost:8000/docs
```

You'll see interactive documentation for all AI endpoints.

## What's in the Database

### Machines

| Machine | Type | Price | Tolerance | Use Case |
|---------|------|-------|-----------|----------|
| Haas ST-30 | CNC Lathe | $185K | ±0.005mm | Production turning |
| Haas VF-3 | 3-Axis Mill | $145K | ±0.008mm | General milling |
| DMG MORI NLX 2500 | Advanced Lathe | $285K | ±0.003mm | High-precision turning |
| Mazak Variaxis i-600 | 5-Axis Mill | $495K | ±0.005mm | Complex parts |

Plus quality tools:
- Zeiss CMM ($125K)
- Mitutoyo CMM ($95K)
- Keyence Optical CMM ($75K)

### Quality Standards

- **ISO 9001:2015** - Quality Management Systems
- **AS9100D** - Aerospace Quality Requirements
- **ASME Y14.5-2018** - GD&T Standard
- **ISO 1101:2017** - Geometric Tolerancing
- **IATF 16949:2016** - Automotive Quality
- **ISO 13485:2016** - Medical Device Quality

Each standard includes full text for AI training.

## Using the AI Features

### 1. Generate Quality Plans

```bash
curl -X POST http://localhost:8000/api/quality/plan \
  -H "Content-Type: application/json" \
  -d '{
    "partDescription": "Precision shaft with concentricity requirements",
    "material": "Aluminum 6061-T6",
    "industry": "aerospace",
    "tolerances": [
      {"feature": "diameter", "tolerance": 0.005},
      {"feature": "concentricity", "tolerance": 0.01}
    ],
    "annualVolume": 10000
  }'
```

**AI will generate:**
- Relevant quality standards (ranked by relevance)
- Inspection points and frequencies
- Control methods (SPC, FAI, etc.)
- Acceptance criteria
- Documentation requirements
- Smart recommendations based on your specific requirements

### 2. Get Machine Recommendations

```bash
curl -X POST http://localhost:8000/api/machines/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "partDimensions": {"x": 150, "y": 50, "z": 50},
    "material": "Aluminum 6061-T6",
    "requiredOperations": ["TURNING", "DRILLING"],
    "annualVolume": 10000,
    "tolerance": 0.005
  }'
```

**AI will score machines based on:**
- Size compatibility
- Tolerance capability
- Automation level for your volume
- Operation capabilities
- Cycle time efficiency

### 3. Search Quality Standards

```bash
curl "http://localhost:8000/api/quality/standards/search?query=aerospace%20tight%20tolerances%20traceability&industry=aerospace"
```

**AI uses semantic search** to find the most relevant standards for your needs.

## Connecting Frontend to AI Backend

Update `manufacturing/assets/js/app.js`:

```javascript
async analyzeCAD() {
    // ... file upload code ...

    // Call AI backend for quality plan
    const response = await fetch('http://localhost:8000/api/quality/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            partDescription: document.getElementById('partName').value,
            material: document.getElementById('materialType').value,
            industry: 'aerospace',  // Add industry selector to form
            tolerances: [
                { feature: 'diameter', tolerance: 0.005 },
                { feature: 'length', tolerance: 0.1 }
            ],
            annualVolume: parseInt(document.getElementById('volume').value)
        })
    });

    const qualityPlan = await response.json();

    // Display AI-generated plan
    console.log('Quality Standards:', qualityPlan.relevantStandards);
    console.log('AI Recommendations:', qualityPlan.aiRecommendations);

    // Update Step 2 with real data from AI
    this.displayQualityPlan(qualityPlan);
}
```

## Example AI Insights

The AI generates contextual recommendations like:

> "Identified 3 critical dimensions with tolerances < ±0.01mm. Recommend CMM inspection with SPC monitoring."

> "Based on AS9100D, require First Article Inspection (FAI) and maintain complete traceability."

> "Titanium material requires specialized tooling and cutting parameters. Monitor tool wear closely and validate process capability."

## Testing the AI

### Test Quality Plan Generation

```bash
cd backend
source venv/bin/activate
cd ai
python3 quality_standards_trainer.py
```

This will:
- Train AI on all quality standards
- Generate a sample quality plan for aerospace part
- Recommend machines

### Test via API

```bash
# Health check
curl http://localhost:8000/

# List all machines
curl http://localhost:8000/api/machines

# Search for aerospace standards
curl "http://localhost:8000/api/quality/standards/search?query=aerospace"
```

## Architecture

```
Manufacturing Platform
│
├── Frontend (manufacturing/)
│   ├── HTML/CSS/JS
│   └── Calls API endpoints
│
└── Backend (backend/)
    ├── Database (SQLite)
    │   ├── Machines catalog
    │   ├── Quality standards
    │   └── Templates
    │
    ├── AI Engine
    │   ├── Sentence transformers
    │   ├── Quality plan generator
    │   └── Machine recommender
    │
    └── FastAPI Server
        └── REST endpoints
```

## Adding Your Own Data

### Add Custom Machines

Edit `backend/database/seed_data.py` and add your machines:

```python
Machine(
    name="Your Machine",
    manufacturer="Manufacturer",
    model="Model",
    category="CNC_LATHE",
    price=200000,
    max_part_size_x=500,
    tolerance=0.005,
    # ... other specs
)
```

Then re-seed:
```bash
cd backend/database
python3 seed_data.py
```

### Add Custom Quality Standards

Add your company's internal standards or additional industry standards:

```python
QualityStandard(
    standard_id="INTERNAL-QC-001",
    title="Your Company Quality Standard",
    full_text="Full text for AI training...",
    # ... other fields
)
```

Then retrain AI:
```bash
curl -X POST http://localhost:8000/api/ai/train
```

## Production Deployment

### Option 1: Docker

```bash
cd backend
docker build -t manufacturing-ai-api .
docker run -p 8000:8000 manufacturing-ai-api
```

### Option 2: Cloud (AWS/GCP/Azure)

1. Deploy API to cloud service
2. Update frontend API endpoint
3. Use managed database (PostgreSQL)
4. Enable CORS for your domain

## Troubleshooting

### "ModuleNotFoundError: No module named 'sentence_transformers'"

```bash
cd backend
source venv/bin/activate
pip install sentence-transformers
```

### "Database not found"

```bash
cd backend/database
python3 seed_data.py
```

### CORS Errors in Frontend

Update `backend/api/manufacturing_api.py`:
```python
allow_origins=["http://localhost:8000", "http://localhost:3000"]
```

## Next Steps

1. ✅ **Integrate with Frontend** - Connect the manufacturing UI to AI endpoints
2. ✅ **Add CAD Parser** - Extract features from actual CAD files
3. ✅ **Expand Database** - Add more machines and standards
4. ✅ **Custom Training** - Train on your company's quality documents
5. ✅ **Deploy** - Move to production environment

## Resources

- **Full Documentation**: `backend/AI_SYSTEM_README.md`
- **API Docs**: http://localhost:8000/docs (when running)
- **Database Schema**: `backend/database/models.py`
- **AI Code**: `backend/ai/quality_standards_trainer.py`

## Support

Questions? Check:
- `backend/AI_SYSTEM_README.md` for detailed documentation
- API docs at `/docs` endpoint
- GitHub issues

---

**Ready to revolutionize manufacturing quality planning! 🚀**
