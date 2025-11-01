# 🧪 Jaque.ai Backend Testing Guide

Your backend is running at: **http://localhost:8000**

## Method 1: Swagger UI - Interactive API Docs (RECOMMENDED) ⭐

**Open in your browser:**
```
http://localhost:8000/docs
```

**What you'll see:**
- Beautiful interactive interface
- All your API endpoints listed
- "Try it out" buttons to test each endpoint
- Real-time request/response examples

**How to test:**
1. Click on any endpoint (e.g., "POST /api/demo/request")
2. Click "Try it out"
3. Fill in the example data
4. Click "Execute"
5. See the response immediately!

**Try these endpoints:**
- `GET /health` - Check if backend is healthy
- `POST /api/demo/request` - Submit a demo request
- `GET /api/demo/requests` - See all demo requests
- `POST /api/cad/upload` - Upload a CAD file
- `GET /api/cad/uploads` - List uploaded CAD files

---

## Method 2: Command Line Testing (Quick & Easy)

### Test 1: Health Check
```bash
curl http://localhost:8000/health | python3 -m json.tool
```

**Expected Output:**
```json
{
    "status": "healthy",
    "version": "1.0.0",
    "timestamp": "2025-11-01T05:00:00.000000"
}
```

### Test 2: Submit Demo Request
```bash
curl -X POST http://localhost:8000/api/demo/request \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "company": "Acme Manufacturing",
    "role": "Operations Manager",
    "message": "Interested in quality prediction"
  }' | python3 -m json.tool
```

### Test 3: Upload CAD File
```bash
curl -X POST http://localhost:8000/api/cad/upload \
  -F "file=@test_simple_part.dxf" | python3 -m json.tool
```

### Test 4: View All Demo Requests
```bash
curl http://localhost:8000/api/demo/requests | python3 -m json.tool
```

### Test 5: View Uploaded CAD Files
```bash
curl http://localhost:8000/api/cad/uploads | python3 -m json.tool
```

---

## Method 3: Automated Test Script

Run the complete end-to-end test:

```bash
./test_complete_workflow.sh
```

This tests:
1. ✅ Demo request submission
2. ✅ CAD file upload
3. ✅ Database verification
4. ✅ File tracking

---

## Method 4: Frontend Testing (HTML Form)

### Option A: Using Python's Built-in Server

1. **Start a simple HTTP server:**
```bash
cd /home/user/Jaque-landing-page
python3 -m http.server 3000
```

2. **Open in browser:**
```
http://localhost:3000
```

3. **Test the form:**
   - Click "Request Demo" button
   - Fill in your details
   - (Optional) Upload a CAD file
   - Click "Send"
   - See the success message!

### Option B: Using Node.js (if available)

```bash
npx serve . -p 3000
```

Then open: http://localhost:3000

---

## Method 5: Python Script Testing

Create a test script:

```python
import requests

# Test 1: Health check
response = requests.get('http://localhost:8000/health')
print("Health Check:", response.json())

# Test 2: Submit demo request
demo_data = {
    "name": "Test User",
    "email": "test@example.com",
    "company": "Test Corp",
    "role": "Quality Manager",
    "message": "Testing the API"
}
response = requests.post('http://localhost:8000/api/demo/request', json=demo_data)
print("Demo Request:", response.json())

# Test 3: Upload CAD file
with open('test_simple_part.dxf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/cad/upload', files=files)
    print("CAD Upload:", response.json())
```

---

## 📊 What to Look For

### ✅ Successful Responses:

**Health Check:**
- Status: "healthy"
- Returns current timestamp

**Demo Request:**
- Success: true
- Message: "Demo request submitted successfully!"

**CAD Upload:**
- Success: true
- Analysis data with entity counts, layers, etc.

### ❌ Common Issues:

**Backend not running:**
```
Connection refused
```
**Solution:** Make sure backend is running:
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

**CORS errors (in browser):**
- Check that ALLOWED_ORIGINS includes your domain
- Should see "Access-Control-Allow-Origin" in response headers

---

## 🎯 Quick Test Checklist

Run these commands to verify everything works:

```bash
# 1. Check health
curl http://localhost:8000/health

# 2. View API docs (open in browser)
echo "Open: http://localhost:8000/docs"

# 3. Run complete test
./test_complete_workflow.sh

# 4. Check database
curl http://localhost:8000/api/demo/requests | python3 -m json.tool

# 5. Check uploaded files
curl http://localhost:8000/api/cad/uploads | python3 -m json.tool
```

---

## 📝 Sample Test Data

### Demo Request JSON:
```json
{
  "name": "John Smith",
  "email": "john.smith@manufacturing.com",
  "company": "Advanced Manufacturing Inc",
  "role": "Quality Manager",
  "message": "We need help with predictive quality control"
}
```

### CAD File:
Use the included `test_simple_part.dxf` file

---

## 🔍 Monitoring Logs

Watch the backend logs in real-time:

```bash
# Backend shows all API requests with:
# - Request method and path
# - Response status code
# - SQL queries (in debug mode)
# - Timestamps
```

Look for lines like:
```
INFO:     127.0.0.1:12345 - "POST /api/demo/request HTTP/1.1" 201 Created
INFO:     127.0.0.1:12345 - "POST /api/cad/upload HTTP/1.1" 200 OK
```

---

## 🚀 Next Steps

After testing:
1. Try uploading different CAD file formats (DXF, STL, etc.)
2. Explore the Swagger UI to see all available endpoints
3. Check the database to see stored data
4. Update request statuses using the PATCH endpoint

Happy Testing! 🎉
