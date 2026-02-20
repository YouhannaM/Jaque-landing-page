#!/usr/bin/env python3
"""Simple file upload server for logo images."""
import http.server, cgi, os, pathlib

UPLOAD_DIR = pathlib.Path("/home/user/Jaque-landing-page/assets/logos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Upload Logos</title>
<style>
  body{font-family:sans-serif;max-width:600px;margin:60px auto;background:#0a0a0a;color:#fff;padding:0 24px}
  h2{margin-bottom:8px}p{color:#888;margin-bottom:28px;font-size:14px}
  .slot{background:#111;border:1px solid #222;border-radius:12px;padding:20px 24px;margin-bottom:12px;display:flex;align-items:center;gap:16px}
  .slot label{flex:1;cursor:pointer;color:#aaa;font-size:14px}
  .slot input{display:none}
  .slot .name{font-weight:600;min-width:120px}
  .slot .chosen{font-size:12px;color:#6366f1;margin-top:4px}
  button{background:#6366f1;color:#fff;border:none;border-radius:8px;padding:14px 32px;font-size:15px;cursor:pointer;width:100%;margin-top:8px}
  button:hover{background:#4f46e5}
  .ok{color:#22c55e;font-weight:600;margin-top:20px;display:none}
</style>
</head>
<body>
<h2>Upload Logo Images</h2>
<p>Select the logo file for each brand, then click Upload All.</p>
<form method="POST" enctype="multipart/form-data">
  <div class="slot">
    <span class="name">1. Dell</span>
    <label>
      <input type="file" name="dell" accept="image/*" onchange="this.nextElementSibling.textContent=this.files[0]?.name||''">
      <span style="background:#1a1a2e;border:1px dashed #333;border-radius:6px;padding:8px 16px;display:inline-block">Choose file</span>
      <div class="chosen"></div>
    </label>
  </div>
  <div class="slot">
    <span class="name">2. Anthropic</span>
    <label>
      <input type="file" name="anthropic" accept="image/*" onchange="this.nextElementSibling.textContent=this.files[0]?.name||''">
      <span style="background:#1a1a2e;border:1px dashed #333;border-radius:6px;padding:8px 16px;display:inline-block">Choose file</span>
      <div class="chosen"></div>
    </label>
  </div>
  <div class="slot">
    <span class="name">3. U of T</span>
    <label>
      <input type="file" name="uoft" accept="image/*" onchange="this.nextElementSibling.textContent=this.files[0]?.name||''">
      <span style="background:#1a1a2e;border:1px dashed #333;border-radius:6px;padding:8px 16px;display:inline-block">Choose file</span>
      <div class="chosen"></div>
    </label>
  </div>
  <div class="slot">
    <span class="name">4. Cornell</span>
    <label>
      <input type="file" name="cornell" accept="image/*" onchange="this.nextElementSibling.textContent=this.files[0]?.name||''">
      <span style="background:#1a1a2e;border:1px dashed #333;border-radius:6px;padding:8px 16px;display:inline-block">Choose file</span>
      <div class="chosen"></div>
    </label>
  </div>
  <div class="slot">
    <span class="name">5. Tesla</span>
    <label>
      <input type="file" name="tesla" accept="image/*" onchange="this.nextElementSibling.textContent=this.files[0]?.name||''">
      <span style="background:#1a1a2e;border:1px dashed #333;border-radius:6px;padding:8px 16px;display:inline-block">Choose file</span>
      <div class="chosen"></div>
    </label>
  </div>
  <button type="submit">Upload All</button>
</form>
</body>
</html>
"""

SUCCESS = """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Done</title>
<style>body{{font-family:sans-serif;max-width:600px;margin:60px auto;background:#0a0a0a;color:#fff;padding:0 24px}}
.ok{{color:#22c55e;font-size:18px;font-weight:600;margin-bottom:16px}}
ul{{color:#aaa;font-size:14px;line-height:1.8}}
</style></head><body>
<div class="ok">✓ Logos uploaded successfully</div>
<ul>{files}</ul>
<p style="color:#888;font-size:13px;margin-top:24px">You can close this tab. Claude Code will now update the website.</p>
</body></html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                environ={"REQUEST_METHOD": "POST",
                                         "CONTENT_TYPE": self.headers["Content-Type"]})
        saved = []
        for field in ["dell", "anthropic", "uoft", "cornell", "tesla"]:
            item = form[field] if field in form else None
            if item and item.filename:
                ext = os.path.splitext(item.filename)[1].lower() or ".png"
                dest = UPLOAD_DIR / f"{field}{ext}"
                dest.write_bytes(item.file.read())
                saved.append(f"<li>{field}{ext} — saved</li>")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(SUCCESS.format(files="".join(saved) or "<li>No files selected</li>").encode())

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", 3000), Handler)
    print("Upload server running on port 3000", flush=True)
    server.serve_forever()
