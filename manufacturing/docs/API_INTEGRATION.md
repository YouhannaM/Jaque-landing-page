# API Integration Guide

This guide explains how to integrate the Manufacturing Operations Platform with a backend API.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Authentication](#authentication)
4. [API Endpoints](#api-endpoints)
5. [Integration Steps](#integration-steps)
6. [Error Handling](#error-handling)
7. [WebSocket Integration](#websocket-integration)
8. [Examples](#examples)

## Overview

The Manufacturing Operations Platform is currently a frontend-only application. This guide shows how to integrate it with a backend API for production use.

## Architecture

### Recommended Stack

**Backend:**
- FastAPI (Python) - Already implemented in `/backend`
- Node.js + Express
- Django REST Framework
- ASP.NET Core

**Database:**
- PostgreSQL (relational data)
- MongoDB (document storage for CAD metadata)
- Redis (caching and real-time data)

**Real-time:**
- WebSocket (Socket.io or native WebSocket)
- Server-Sent Events (SSE)
- GraphQL Subscriptions

## Authentication

### JWT Authentication

1. **Login Endpoint:**
```javascript
async login(username, password) {
    const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    localStorage.setItem('token', data.token);
    return data;
}
```

2. **Add to API Service:**
```javascript
class ApiService {
    constructor() {
        this.baseUrl = '/api';
        this.token = localStorage.getItem('token');
    }

    async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            ...options,
            headers
        });

        if (response.status === 401) {
            // Token expired, redirect to login
            window.location.href = '/login';
            return;
        }

        return response.json();
    }
}
```

## API Endpoints

### CAD Upload & Analysis

**POST /api/cad/upload**
```javascript
Request:
{
    "files": [File objects],
    "partName": "string",
    "material": "string",
    "volume": number
}

Response:
{
    "analysisId": "uuid",
    "status": "processing",
    "estimatedTime": 120 // seconds
}
```

**GET /api/cad/analysis/{analysisId}**
```javascript
Response:
{
    "status": "completed",
    "criticalDimensions": [
        {
            "feature": "Bore Diameter",
            "specification": "Ø25.000 ±0.005mm",
            "method": "CMM"
        }
    ],
    "qualityPlan": { ... },
    "recommendations": { ... }
}
```

### Quality Control Plan

**POST /api/quality/plan**
```javascript
Request:
{
    "analysisId": "uuid",
    "controlPoints": [...],
    "inspectionFrequency": {...}
}

Response:
{
    "planId": "uuid",
    "status": "approved",
    "createdAt": "ISO-8601 timestamp"
}
```

**GET /api/quality/plan/{planId}**
```javascript
Response:
{
    "planId": "uuid",
    "features": [...],
    "controlPlan": [...],
    "strategy": {...}
}
```

### Production Monitoring

**GET /api/production/metrics**
```javascript
Response:
{
    "oee": 87.5,
    "partsToday": 142,
    "hoursToMaintenance": 23,
    "currentCpk": 1.45,
    "timestamp": "ISO-8601"
}
```

**POST /api/production/quality-data**
```javascript
Request:
{
    "operator": "string",
    "serialNumber": "string",
    "measurements": {
        "boreDiameter": 25.002,
        "overallLength": 149.98
    },
    "timestamp": "ISO-8601"
}

Response:
{
    "dataId": "uuid",
    "status": "recorded",
    "alerts": []
}
```

### Analytics

**GET /api/analytics/spc**
```javascript
Query Parameters:
- feature: "boreDiameter"
- startDate: "ISO-8601"
- endDate: "ISO-8601"
- limit: 100

Response:
{
    "feature": "boreDiameter",
    "measurements": [
        {
            "timestamp": "ISO-8601",
            "value": 25.002,
            "operator": "John Smith"
        }
    ],
    "controlLimits": {
        "ucl": 25.005,
        "lcl": 24.995,
        "target": 25.000
    },
    "cpk": 1.45
}
```

**GET /api/analytics/insights**
```javascript
Response:
{
    "insights": [
        {
            "type": "trend",
            "severity": "warning",
            "message": "Bore diameter showing upward drift",
            "recommendation": "Schedule tool replacement"
        }
    ],
    "timestamp": "ISO-8601"
}
```

## Integration Steps

### Step 1: Create API Service

Add to `assets/js/api-service.js`:

```javascript
class ApiService {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
        this.token = localStorage.getItem('authToken');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('authToken', token);
    }

    async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                ...options,
                headers
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // CAD Upload
    async uploadCAD(formData) {
        return this.request('/cad/upload', {
            method: 'POST',
            body: formData,
            headers: {} // Let browser set Content-Type for FormData
        });
    }

    async getAnalysis(analysisId) {
        return this.request(`/cad/analysis/${analysisId}`);
    }

    // Quality Plan
    async createQualityPlan(planData) {
        return this.request('/quality/plan', {
            method: 'POST',
            body: JSON.stringify(planData)
        });
    }

    async getQualityPlan(planId) {
        return this.request(`/quality/plan/${planId}`);
    }

    // Production
    async getProductionMetrics() {
        return this.request('/production/metrics');
    }

    async logQualityData(data) {
        return this.request('/production/quality-data', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // Analytics
    async getSPCData(feature, startDate, endDate) {
        const params = new URLSearchParams({
            feature,
            startDate: startDate.toISOString(),
            endDate: endDate.toISOString()
        });
        return this.request(`/analytics/spc?${params}`);
    }

    async getInsights() {
        return this.request('/analytics/insights');
    }
}

export default ApiService;
```

### Step 2: Update ManufacturingApp

Modify `assets/js/app.js`:

```javascript
import ApiService from './api-service.js';

class ManufacturingApp {
    constructor() {
        this.api = new ApiService();
        // ... rest of constructor
    }

    async analyzeCAD() {
        if (this.uploadedFiles.length === 0) {
            this.showError('Please upload CAD files');
            return;
        }

        this.showLoading(true);

        try {
            const formData = new FormData();
            this.uploadedFiles.forEach(file => {
                formData.append('files', file);
            });
            formData.append('partName', document.getElementById('partName').value);
            formData.append('material', document.getElementById('materialType').value);
            formData.append('volume', document.getElementById('volume').value);

            const result = await this.api.uploadCAD(formData);

            // Poll for analysis completion
            await this.pollAnalysis(result.analysisId);

            this.currentStep = 2;
            this.showStep(2);
        } catch (error) {
            this.showError('Analysis failed: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async pollAnalysis(analysisId) {
        return new Promise((resolve, reject) => {
            const interval = setInterval(async () => {
                try {
                    const result = await this.api.getAnalysis(analysisId);

                    if (result.status === 'completed') {
                        clearInterval(interval);
                        this.analysisData = result;
                        resolve(result);
                    } else if (result.status === 'failed') {
                        clearInterval(interval);
                        reject(new Error('Analysis failed'));
                    }
                } catch (error) {
                    clearInterval(interval);
                    reject(error);
                }
            }, 2000);
        });
    }

    async logQualityData() {
        const data = {
            operator: document.getElementById('operator').value,
            serialNumber: document.getElementById('serialNumber').value,
            measurements: {
                boreDiameter: parseFloat(document.getElementById('boreDiameter').value),
                overallLength: parseFloat(document.getElementById('overallLength').value)
            },
            timestamp: new Date().toISOString()
        };

        try {
            const result = await this.api.logQualityData(data);
            this.showNotification('Data logged successfully', 'success');

            // Clear form
            document.getElementById('serialNumber').value = '';
            document.getElementById('boreDiameter').value = '';
            document.getElementById('overallLength').value = '';

            // Enable analytics
            this.currentStep = Math.max(this.currentStep, 5);
        } catch (error) {
            this.showError('Failed to log data: ' + error.message);
        }
    }
}
```

### Step 3: Update HTML

Modify `index.html` to use modules:

```html
<script type="module" src="assets/js/app.js"></script>
```

## Error Handling

### Global Error Handler

```javascript
class ErrorHandler {
    static handle(error, context = '') {
        console.error(`Error in ${context}:`, error);

        // Log to error tracking service
        if (window.Sentry) {
            Sentry.captureException(error);
        }

        // Display user-friendly message
        const message = this.getUserMessage(error);
        this.showNotification(message, 'error');
    }

    static getUserMessage(error) {
        if (error.response) {
            switch (error.response.status) {
                case 400:
                    return 'Invalid request. Please check your input.';
                case 401:
                    return 'Please log in to continue.';
                case 403:
                    return 'You do not have permission to perform this action.';
                case 404:
                    return 'Resource not found.';
                case 500:
                    return 'Server error. Please try again later.';
                default:
                    return 'An error occurred. Please try again.';
            }
        }
        return error.message || 'An unexpected error occurred.';
    }

    static showNotification(message, type) {
        // Implement notification UI
        alert(message);
    }
}
```

## WebSocket Integration

### Real-time Production Monitoring

```javascript
class WebSocketService {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.ws.onclose = () => {
            console.log('WebSocket closed');
            this.reconnect();
        };
    }

    handleMessage(data) {
        switch (data.type) {
            case 'metrics_update':
                this.updateMetrics(data.payload);
                break;
            case 'alert':
                this.showAlert(data.payload);
                break;
            case 'quality_data':
                this.updateQualityData(data.payload);
                break;
        }
    }

    reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => {
                console.log(`Reconnecting... (${this.reconnectAttempts})`);
                this.connect();
            }, 1000 * this.reconnectAttempts);
        }
    }

    send(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Usage
const wsService = new WebSocketService('wss://api.example.com/ws');
wsService.connect();
```

## Examples

### Complete Integration Example

See `/backend` directory for a working FastAPI implementation that includes:
- CAD file upload endpoints
- Quality plan management
- Production monitoring APIs
- WebSocket support for real-time updates
- Database models and migrations
- Authentication and authorization

### Testing

```javascript
// Mock API for testing
class MockApiService extends ApiService {
    async uploadCAD(formData) {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve({
                    analysisId: 'mock-uuid',
                    status: 'processing'
                });
            }, 1000);
        });
    }

    async getAnalysis(analysisId) {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve({
                    status: 'completed',
                    criticalDimensions: [/* mock data */]
                });
            }, 2000);
        });
    }
}
```

## Best Practices

1. **Use environment variables** for API URLs
2. **Implement retry logic** for failed requests
3. **Add request timeouts**
4. **Cache responses** where appropriate
5. **Validate data** before sending to API
6. **Handle network errors** gracefully
7. **Use HTTPS** in production
8. **Implement rate limiting**
9. **Log API calls** for debugging
10. **Monitor API performance**

## Support

For API integration questions:
- Check the backend README at `/backend/README.md`
- Open an issue on GitHub
- Contact: api-support@jaque.ai

---

**Last Updated:** November 2025
**Version:** 1.0.0
