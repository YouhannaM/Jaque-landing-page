# 🚀 How to Run This Code from GitHub

There are several ways to run this code from GitHub. Choose the one that fits your needs:

---

## 📋 **Quick Answer: What Do You Want?**

1. **Someone else wants to run your code?** → See [Clone and Run Locally](#1-clone-and-run-locally)
2. **Deploy to the internet (live website)?** → See [Deploy to Cloud](#2-deploy-to-cloud)
3. **Just the frontend (landing page)?** → See [GitHub Pages](#3-github-pages-frontend-only)

---

## 1. Clone and Run Locally

**For someone who wants to run your code on their computer:**

### Step 1: Clone the Repository
```bash
git clone https://github.com/YouhannaM/Jaque-landing-page.git
cd Jaque-landing-page
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment
```bash
cp .env.example .env
# Edit .env with your settings if needed
```

### Step 4: Run the Backend
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 5: Access the API
Open browser to: `http://localhost:8000/docs`

---

## 2. Deploy to Cloud (Make it Live on Internet)

### Option A: Deploy to Render.com (FREE & EASY!) ⭐

**Perfect for beginners - No credit card needed!**

#### Step 1: Go to Render.com
- Visit: https://render.com
- Sign up with your GitHub account

#### Step 2: Create New Web Service
- Click **"New +"** → **"Web Service"**
- Connect your GitHub repository
- Select: `YouhannaM/Jaque-landing-page`

#### Step 3: Configure Settings
```
Name: jaque-backend
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

#### Step 4: Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**:
- `DATABASE_URL` = `sqlite:///./jaque.db`
- `ALLOWED_ORIGINS` = `*`
- `DEBUG` = `True`

#### Step 5: Deploy!
- Click **"Create Web Service"**
- Wait 2-3 minutes
- Your API will be live at: `https://jaque-backend.onrender.com`

**Access your API at:**
```
https://jaque-backend.onrender.com/docs
```

---

### Option B: Deploy to Railway.app (Also FREE!)

#### Step 1: Go to Railway
- Visit: https://railway.app
- Sign in with GitHub

#### Step 2: New Project
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**
- Choose `YouhannaM/Jaque-landing-page`

#### Step 3: Configure
Railway auto-detects Python. Just add these environment variables:
- `DATABASE_URL` = `sqlite:///./jaque.db`
- `PORT` = `8000`

#### Step 4: Deploy
- Railway automatically builds and deploys
- Get your URL from the dashboard

---

### Option C: Deploy to Heroku

#### Step 1: Install Heroku CLI
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh
```

#### Step 2: Login and Create App
```bash
heroku login
heroku create jaque-backend
```

#### Step 3: Add Procfile
Create `Procfile` in your project root:
```
web: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

#### Step 4: Deploy
```bash
git push heroku main
```

Your app will be at: `https://jaque-backend.herokuapp.com`

---

## 3. GitHub Pages (Frontend Only)

**Deploy just the landing page (index.html) - No backend**

### Step 1: Go to Repository Settings
- Go to your GitHub repo
- Click **"Settings"** tab
- Click **"Pages"** in sidebar

### Step 2: Configure Source
- Source: **Deploy from a branch**
- Branch: **main** (or your branch name)
- Folder: **/ (root)**

### Step 3: Save
- Click **"Save"**
- Wait 1-2 minutes

### Step 4: Access
Your site will be live at:
```
https://youhannam.github.io/Jaque-landing-page/
```

**Note:** This only works for the HTML page, NOT the backend API!

---

## 4. Docker Deployment (Advanced)

**If you have Docker installed:**

### Step 1: Build Docker Image
```bash
docker-compose up -d
```

This starts:
- Backend (port 8000)
- PostgreSQL database
- Redis cache
- Nginx web server

### Step 2: Access
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🎯 **Recommended Setup for Beginners**

**I recommend using Render.com because:**
✅ Completely FREE
✅ No credit card required
✅ Auto-deploys from GitHub
✅ Provides HTTPS automatically
✅ Easy to set up

---

## 📝 **What Each Deployment Includes**

| Method | Frontend | Backend | Database | Cost |
|--------|----------|---------|----------|------|
| **Local** | ✅ | ✅ | SQLite | Free |
| **Render.com** | ❌ | ✅ | SQLite | Free |
| **Railway** | ❌ | ✅ | PostgreSQL | Free tier |
| **GitHub Pages** | ✅ | ❌ | ❌ | Free |
| **Docker (Local)** | ✅ | ✅ | PostgreSQL | Free |

---

## 🔧 Files Needed for Deployment

Your repository already has these files ready:

✅ `requirements.txt` - Python dependencies
✅ `Dockerfile` - Docker configuration
✅ `docker-compose.yml` - Multi-container setup
✅ `.env.example` - Environment template
✅ `backend/` - All backend code
✅ `index.html` - Frontend landing page

---

## 🆘 **Common Issues**

### "Module not found"
→ Run: `pip install -r requirements.txt`

### "Port already in use"
→ Change port: `uvicorn backend.app.main:app --port 8001`

### "Database not found"
→ The app creates it automatically on first run

### "CORS errors in browser"
→ Update `ALLOWED_ORIGINS` in `.env`

---

## 📚 **Next Steps After Deployment**

Once deployed, update your frontend (`index.html`) to point to your live backend:

```javascript
// Change this line in index.html
const API_URL = 'https://your-app.onrender.com';  // Your deployed URL
```

---

## 🎉 **Quick Start Commands**

### Run Locally:
```bash
git clone https://github.com/YouhannaM/Jaque-landing-page.git
cd Jaque-landing-page
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

### Deploy to Render:
1. Go to render.com
2. Connect GitHub
3. Deploy!

---

Need help? Check the main README.md or ask questions!
