# 🎯 How to Open Backend in VS Code

## Method 1: VS Code Simple Browser (Built-in) ⭐ EASIEST!

### Step 1: Open Command Palette
Press: **Ctrl+Shift+P** (Windows/Linux) or **Cmd+Shift+P** (Mac)

### Step 2: Type and Select
Type: `Simple Browser`
Select: **"Simple Browser: Show"**

### Step 3: Enter URL
When prompted, paste this URL:
```
http://localhost:8000/docs
```

### Step 4: Press Enter
You'll see the API documentation in VS Code's built-in browser!

---

## Method 2: VS Code Port Forwarding (If Remote)

If you're connected to a remote server via SSH:

### Step 1: Open Ports Panel
1. Click on **"PORTS"** tab at the bottom of VS Code
2. (Next to TERMINAL, PROBLEMS, etc.)

### Step 2: Forward Port 8000
1. Click the **"+"** button (Forward a Port)
2. Type: **8000**
3. Press Enter

### Step 3: Open in Browser
1. Right-click on the forwarded port (8000)
2. Click **"Open in Browser"**
3. Add `/docs` to the URL

---

## Method 3: Open External Browser from VS Code

### Step 1: Open Terminal in VS Code
Press: **Ctrl+`** (backtick) or go to **Terminal → New Terminal**

### Step 2: Click the URL
You'll see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Hold Ctrl and Click
**Ctrl+Click** (or **Cmd+Click** on Mac) on the URL `http://0.0.0.0:8000`

### Step 4: Add /docs
In your browser, add `/docs` to the end of the URL:
```
http://localhost:8000/docs
```

---

## 🎨 Visual Guide for VS Code Simple Browser:

```
┌─────────────────────────────────────────────┐
│  VS Code                                    │
├─────────────────────────────────────────────┤
│                                             │
│  1. Press Ctrl+Shift+P                     │
│  2. Type: "Simple Browser"                 │
│  3. Enter URL: http://localhost:8000/docs  │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  Simple Browser                       │ │
│  │  ─────────────────────────────────── │ │
│  │                                       │ │
│  │  Jaque.ai API Documentation          │ │
│  │  [Interactive API Interface]         │ │
│  │                                       │ │
│  └───────────────────────────────────────┘ │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🚀 Quick Steps (Summary):

### Fastest Way:
1. **Ctrl+Shift+P** (Command Palette)
2. Type **"Simple Browser"**
3. Enter **http://localhost:8000/docs**
4. Done! ✅

---

## ✅ What You'll See:

Once opened, you'll see:
- **Jaque.ai API** title
- List of all endpoints (demo, cad, health)
- **"Try it out"** buttons
- Interactive testing interface

---

## 🔧 Troubleshooting:

### "Simple Browser not found"
→ You might have an older version of VS Code
→ Alternative: Use Method 3 (Open in external browser)

### "Connection refused"
→ Make sure backend is running
→ Check terminal shows: `Uvicorn running on http://0.0.0.0:8000`

### Port forwarding not working
→ Make sure you're using VS Code Remote SSH
→ Check PORTS tab is visible

---

## 💡 Pro Tip:

You can split your VS Code screen:
- **Left side:** Your code
- **Right side:** Simple Browser with API docs
- Test your changes in real-time!

To split:
1. Open Simple Browser
2. Drag the tab to the right side
3. Now you can see code + browser together!

---

Happy Testing in VS Code! 🎉
