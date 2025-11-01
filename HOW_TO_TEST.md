# 🎯 How to Test Your Backend - Simple Guide

## The TWO Main Ways to Test:

---

## ⭐ METHOD 1: Web Browser (EASIEST - NO TYPING!)

### Step 1: Open your web browser
- Chrome, Firefox, Safari, Edge, or any browser

### Step 2: Copy and paste this URL in the address bar:
```
http://localhost:8000/docs
```

### Step 3: You'll see a beautiful interface!
- Click on any green/blue bar to expand an endpoint
- Click the "Try it out" button
- Fill in the example data
- Click "Execute"
- See the results!

### What you can do:
- ✅ Test demo request submission
- ✅ Upload CAD files
- ✅ View all requests
- ✅ Check health status
- **All with just mouse clicks - no command typing needed!**

---

## 💻 METHOD 2: Terminal/Command Line

### Step 1: Open your terminal
**Where is the terminal?**
- **Mac:** Applications → Utilities → Terminal
- **Windows:** Search for "Command Prompt" or "PowerShell"
- **Linux:** Ctrl+Alt+T
- **VS Code:** View → Terminal (or Ctrl+`)

### Step 2: Navigate to the project folder
```bash
cd /home/user/Jaque-landing-page
```

### Step 3: Run the test script
```bash
./quick_test.sh
```

That's it! The script will automatically test everything.

---

## 🎨 What Each Method Does:

### Web Browser Method:
```
YOU:    Open browser → Go to http://localhost:8000/docs
RESULT: Interactive page where you click buttons to test
```

### Terminal Method:
```
YOU:    Type ./quick_test.sh in terminal
RESULT: Automatic tests run and show results
```

---

## 🚀 Quick Commands You Can Try (in Terminal):

### Check if backend is healthy:
```bash
curl http://localhost:8000/health
```

### View all demo requests:
```bash
curl http://localhost:8000/api/demo/requests
```

### View uploaded CAD files:
```bash
curl http://localhost:8000/api/cad/uploads
```

---

## ❓ "I don't know what terminal means"

**No problem!** Just use the **Web Browser** method:

1. Open Chrome (or any browser)
2. Type in the URL bar: `http://localhost:8000/docs`
3. Press Enter
4. Click around and test!

**You don't need to use the terminal at all!** 🎉

---

## 📱 Screenshot of What You'll See:

When you open `http://localhost:8000/docs` in your browser, you'll see:

```
┌─────────────────────────────────────────────────┐
│  Jaque.ai API                                   │
│  Backend API for Jaque.ai - AI for Manufacturing│
│                                                  │
│  ▼ demo - Demo request endpoints                │
│     POST /api/demo/request                      │
│     GET  /api/demo/requests                     │
│                                                  │
│  ▼ cad - CAD file processing                    │
│     POST /api/cad/upload                        │
│     GET  /api/cad/uploads                       │
│                                                  │
│  ▼ default                                      │
│     GET  /                                      │
│     GET  /health                                │
└─────────────────────────────────────────────────┘
```

Click on any line to expand and test it!

---

## ✅ Recommended: Start with Web Browser

**The web browser method is:**
- ✅ Easier to use
- ✅ Visual and interactive
- ✅ No commands to remember
- ✅ Perfect for beginners

**Just open: http://localhost:8000/docs**

---

## 🆘 Having Trouble?

### "localhost:8000 doesn't work"
→ Make sure the backend is running. You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### "I see a blank page"
→ Wait a few seconds and refresh

### "Connection refused"
→ Backend might not be running. Start it with:
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🎉 That's It!

**Start with the web browser method - it's the easiest!**

Just open: **http://localhost:8000/docs**

Happy testing! 🚀
