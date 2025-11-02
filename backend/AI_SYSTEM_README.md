# AI-Powered Manufacturing Operations Platform

## Overview

This system provides AI-powered quality planning and machine recommendations for manufacturing operations. It includes:

1. **Machine Database**: Real catalog of CNC machines, quality tools, and equipment
2. **Quality Standards AI**: Trained on ISO, ASME, AS9100, IATF and other standards
3. **Quality Plan Generator**: AI-generated quality control plans
4. **Machine Recommendation Engine**: Smart equipment selection based on requirements

## Architecture

```
backend/
├── database/
│   ├── models.py              # Database schema
│   ├── seed_data.py          # Sample data and initialization
│   └── manufacturing.db       # SQLite database (created on setup)
│
├── ai/
│   └── quality_standards_trainer.py  # AI training and inference
│
├── api/
│   └── manufacturing_api.py   # FastAPI endpoints
│
├── requirements_ai.txt        # Python dependencies
└── setup_ai_system.sh        # Automated setup script
```

## Quick Start

### 1. Setup

```bash
cd backend
chmod +x setup_ai_system.sh
./setup_ai_system.sh
```

This will:
- Create Python virtual environment
- Install all dependencies
- Initialize database with sample data
- Train AI models on quality standards
- Download pre-trained language models

### 2. Start the API Server

```bash
./start_api.sh
```

Or manually:
```bash
source venv/bin/activate
cd api
python3 manufacturing_api.py
```

### 3. Access API Documentation

Open your browser to:
```
http://localhost:8000/docs
```

You'll see interactive Swagger documentation for all endpoints.

## Database Contents

### Machines (CNC Equipment)

The database includes real manufacturing equipment:

**CNC Lathes:**
- Haas ST-30 ($185K) - Standard production lathe
- DMG MORI NLX 2500 ($285K) - Advanced lathe with Y-axis

**CNC Mills:**
- Haas VF-3 ($145K) - 3-axis vertical machining center
- Mazak Variaxis i-600 ($495K) - 5-axis machining center

**Quality Tools:**
- Zeiss Contura G2 CMM ($125K)
- Mitutoyo Crysta-Apex S CMM ($95K)
- Keyence IM-8000 Optical CMM ($75K)

Each machine includes:
- Specifications (work envelope, spindle speed, feed rates)
- Tolerance capabilities
- Compatible materials
- Automation level
- Lead times and pricing

### Quality Standards

Pre-loaded with major manufacturing standards:

1. **ISO 9001:2015** - Quality Management Systems
2. **AS9100D** - Aerospace Quality Management
3. **ASME Y14.5-2018** - GD&T Standard
4. **ISO 1101:2017** - Geometric Tolerancing
5. **IATF 16949:2016** - Automotive Quality
6. **ISO 13485:2016** - Medical Device Quality

Each standard includes:
- Full text content (for AI training)
- Key requirements
- Applicable industries
- Related processes
- AI embeddings for similarity search

### Quality Plan Templates

Pre-configured templates for:
- Aerospace precision parts (AS9100 compliant)
- Automotive production parts (IATF 16949 compliant)
- Medical device components (ISO 13485 compliant)

## AI Capabilities

### 1. Quality Standards Search

The AI can find relevant standards based on natural language queries:

```python
# Example API call
POST /api/quality/standards/search
{
    "query": "aerospace part with tight tolerances requiring traceability",
    "industry": "aerospace"
}

# Returns ranked standards by relevance
```

**How it works:**
- Uses sentence transformers (all-MiniLM-L6-v2) for semantic understanding
- Compares query embedding with standard embeddings
- Returns top matches with similarity scores

### 2. Quality Plan Generation

AI generates comprehensive quality control plans:

```python
POST /api/quality/plan
{
    "partDescription": "Precision shaft with concentricity requirements",
    "material": "Aluminum 6061-T6",
    "industry": "aerospace",
    "tolerances": [
        {"feature": "diameter", "tolerance": 0.005},
        {"feature": "concentricity", "tolerance": 0.01}
    ],
    "annualVolume": 10000
}
```

**Generated plan includes:**
- Relevant quality standards (ranked by AI)
- Inspection points and methods
- Control methods (SPC, FAI, etc.)
- Acceptance criteria
- Documentation requirements
- AI-powered recommendations

**AI Insights Examples:**
- "Identified 3 critical dimensions with tolerances < ±0.01mm. Recommend CMM inspection with SPC monitoring."
- "Based on AS9100D, require First Article Inspection (FAI) and maintain complete traceability."
- "Titanium material requires specialized tooling. Monitor tool wear closely."

### 3. Machine Recommendations

Smart equipment selection based on requirements:

```python
POST /api/machines/recommend
{
    "partDimensions": {"x": 150, "y": 50, "z": 50},
    "material": "Aluminum 6061-T6",
    "requiredOperations": ["TURNING", "DRILLING"],
    "annualVolume": 10000,
    "tolerance": 0.005
}
```

**Scoring algorithm considers:**
- Work envelope compatibility (30 points)
- Tolerance capability (25 points)
- Automation level for volume (20 points)
- Capability match (20 points)
- Cycle time efficiency (15 points)

**Returns:**
- Top 5 machines ranked by score
- Price and lead time
- Reasons for recommendation
- Capability match analysis

## API Endpoints

### CAD Upload & Analysis

```bash
# Upload CAD files
POST /api/cad/upload
Content-Type: multipart/form-data
- files: CAD files (.step, .iges, etc.)
- partName: string
- material: string
- volume: integer

# Get analysis results
GET /api/cad/analysis/{analysisId}
```

### Quality Planning

```bash
# Generate quality plan
POST /api/quality/plan

# Search quality standards
GET /api/quality/standards/search?query=aerospace+tolerancing&industry=aerospace

# List all standards
GET /api/quality/standards?industry=aerospace&category=DIMENSIONAL
```

### Machine Recommendations

```bash
# Get machine recommendations
POST /api/machines/recommend

# List all machines
GET /api/machines?category=CNC_LATHE&max_price=200000
```

### Production Monitoring

```bash
# Log quality data
POST /api/production/quality-data

# Get real-time metrics
GET /api/production/metrics

# Get SPC data
GET /api/analytics/spc?feature=boreDiameter&limit=100

# Get AI insights
GET /api/analytics/insights
```

### AI Training

```bash
# Retrain AI models
POST /api/ai/train
```

## Integration with Frontend

### Update Frontend to Use AI Backend

In `manufacturing/assets/js/app.js`, update the `analyzeCAD` method:

```javascript
async analyzeCAD() {
    const formData = new FormData();
    this.uploadedFiles.forEach(file => formData.append('files', file));
    formData.append('partName', document.getElementById('partName').value);
    formData.append('material', document.getElementById('materialType').value);
    formData.append('volume', document.getElementById('volume').value);

    // Call AI backend
    const response = await fetch('http://localhost:8000/api/cad/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();

    // Generate AI-powered quality plan
    const qualityPlanResponse = await fetch('http://localhost:8000/api/quality/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            partDescription: document.getElementById('partName').value,
            material: document.getElementById('materialType').value,
            industry: 'aerospace',  // Could be a form field
            tolerances: [
                { feature: 'diameter', tolerance: 0.005 },
                // Extract from CAD
            ],
            annualVolume: parseInt(document.getElementById('volume').value)
        })
    });

    const qualityPlan = await qualityPlanResponse.json();

    // Update UI with AI-generated plan
    this.displayQualityPlan(qualityPlan);
}
```

## Training Custom Models

### Add Your Own Quality Documents

```python
from database.models import QualityStandard, TrainingDocument

# Add a new standard
standard = QualityStandard(
    standard_id="YOUR-STANDARD-ID",
    title="Your Standard Title",
    organization="Your Organization",
    category="QUALITY_MANAGEMENT",
    full_text="Full text of the standard...",
    summary="Brief summary",
    key_requirements=json.dumps([...]),
    industry=json.dumps(["your_industry"]),
    applicable_processes=json.dumps([...])
)

session.add(standard)
session.commit()
```

### Retrain the AI

```python
from ai.quality_standards_trainer import QualityStandardsTrainer

trainer = QualityStandardsTrainer()
trainer.train_on_quality_standards()
```

Or via API:
```bash
curl -X POST http://localhost:8000/api/ai/train
```

## Adding More Machines

Edit `database/seed_data.py`:

```python
new_machine = Machine(
    name="Your Machine Name",
    manufacturer="Manufacturer",
    model="Model Number",
    category="CNC_LATHE",  # or CNC_MILL, 5_AXIS_MILL, etc.
    price=250000,
    max_part_size_x=800,
    max_part_size_y=400,
    max_part_size_z=400,
    spindle_speed_max=4000,
    tolerance=0.003,
    # ... other specifications
)
```

Then re-run the seed script:
```bash
cd database
python3 seed_data.py
```

## Advanced Configuration

### Use a Different AI Model

Edit `ai/quality_standards_trainer.py`:

```python
def initialize_model(self):
    # Try different models:
    # self.model = SentenceTransformer('all-mpnet-base-v2')  # More accurate
    # self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Faster
    self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Default
```

### Use PostgreSQL Instead of SQLite

Update `models.py` and API connection strings:

```python
DATABASE_URL = "postgresql://user:password@localhost/manufacturing"
```

### Enable GPU Acceleration

If you have a CUDA-capable GPU:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

The sentence-transformers will automatically use GPU.

## Testing

### Run API Tests

```bash
source venv/bin/activate
pytest tests/
```

### Manual Testing

```bash
# Health check
curl http://localhost:8000/

# Search standards
curl "http://localhost:8000/api/quality/standards/search?query=aerospace+tolerancing"

# List machines
curl http://localhost:8000/api/machines

# Get production metrics
curl http://localhost:8000/api/production/metrics
```

## Performance Optimization

### Embeddings Caching

The system caches embeddings for faster retrieval. To rebuild cache:

```python
trainer = QualityStandardsTrainer()
trainer.embeddings_cache = {}
trainer.train_on_quality_standards()
```

### Database Indexing

For production, add indexes:

```sql
CREATE INDEX idx_machines_category ON machines(category);
CREATE INDEX idx_machines_price ON machines(price);
CREATE INDEX idx_standards_category ON quality_standards(category);
```

## Troubleshooting

### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements_ai.txt
```

### Database Issues

```bash
# Reset database
rm database/manufacturing.db
cd database && python3 seed_data.py
```

### AI Model Download Fails

The system will fallback to TF-IDF if sentence-transformers fails. To force download:

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./models')
```

### CORS Errors

Update `api/manufacturing_api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000"],  # Your origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Production Deployment

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements_ai.txt .
RUN pip install -r requirements_ai.txt

COPY . .

RUN cd database && python3 seed_data.py
RUN cd ai && python3 quality_standards_trainer.py

EXPOSE 8000

CMD ["uvicorn", "api.manufacturing_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t manufacturing-api .
docker run -p 8000:8000 manufacturing-api
```

### Environment Variables

```bash
export DATABASE_URL="postgresql://..."
export AI_MODEL="all-MiniLM-L6-v2"
export LOG_LEVEL="INFO"
```

## Support & Contributing

For questions or contributions:
- GitHub Issues: [repository URL]
- Email: support@jaque.ai

## License

MIT License - See LICENSE file for details

---

**Version:** 1.0.0
**Last Updated:** November 2025
