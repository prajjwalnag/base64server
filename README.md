# 🖼️ Base64 Server

A production-ready Base64 image conversion service built with Flask. Convert between base64 strings and image files via a modern web UI or REST API.

---

## 📁 Project Structure

```
base64/
├── base64server/              # Main Flask application
│   ├── app.py                 # API endpoints & server logic
│   ├── templates/index.html   # Dark-mode web UI
│   ├── requirements.txt       # Python dependencies
│   ├── .gitignore             # Git ignore rules
│   └── README.md              # Full setup & API documentation
└── README.md                  # This file
```

---

## 🚀 Quick Start

### 1️⃣ Get the Code
```bash
git clone https://github.com/prajjwalnag/base64server.git
cd base64server
```

### 2️⃣ Install & Run
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

✨ **The app is ready at** `http://localhost:5000`

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎨 **Web Interface** | Dark-mode UI for encoding/decoding images |
| 🔌 **REST API** | Programmatic access with rate limiting |
| 💾 **Two Modes** | Download binary or save to server with URL |
| 🔒 **Security** | Content Security Policy, XSS/clickjacking protection |
| 🧹 **Auto-Cleanup** | Temporary files deleted after 24 hours |
| ⚡ **Rate Limiting** | 30 requests/min per IP to prevent abuse |
| 🖼️ **Format Support** | PNG, JPEG, GIF, WEBP, BMP |

---

## 📚 Documentation

For complete setup, deployment, API documentation, and code examples, see:

### 👉 **[base64server/README.md](base64server/README.md)** ← Full Documentation

**Quick Sections:**
- 🔧 Installation & configuration
- 🔌 API endpoints with examples
- 💻 Python, JavaScript, Node.js code samples
- 🐳 Docker & Nginx deployment
- 🆘 Troubleshooting & security info

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/decode` | `POST` | Convert base64 → image |
| `/api/v1/encode` | `POST` | Convert image → base64 |
| `/api/v1/files/<filename>` | `GET` | Download saved file |

**Base URL:** `http://localhost:5000/api/v1`

### ⚡ Quick Example

```bash
# 📤 Encode image to base64
curl -X POST http://localhost:5000/api/v1/encode \
  -F "file=@image.png"

# 📥 Decode base64 to image
curl -X POST http://localhost:5000/api/v1/decode \
  -H "Content-Type: application/json" \
  -d '{"data": "iVBORw0KGgo..."}' \
  -o output.png
```

---

## 🛠️ Development

### 📋 Requirements
- **Python 3.8+** (3.9, 3.10, 3.11, 3.12 supported)
- pip

### ✅ Python Version Support

| Version | Status | Notes |
|---------|--------|-------|
| Python 3.8 | ✅ Supported | Minimum version |
| Python 3.9 | ✅ Supported | Recommended |
| Python 3.10 | ✅ Supported | Fully tested |
| Python 3.11 | ✅ Supported | Fully tested |
| Python 3.12 | ✅ Supported | Latest stable |

### 🔧 Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r base64server/requirements.txt
cd base64server
python app.py
```

### 🚀 Production Deployment
```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

📖 See [base64server/README.md#deployment](base64server/README.md#deployment) for Docker, Nginx, and cloud deployment guides.

---

## 🔒 Security Features

- 🛡️ **Content Security Policy** — Restricts script execution
- ✅ **Magic Byte Validation** — Verifies files by content, not extension
- 🚫 **Rate Limiting** — Protects against brute force & DoS
- 🔐 **XSS Protection** — Safe DOM manipulation
- 🔒 **Clickjacking Prevention** — X-Frame-Options headers
- 🧹 **Auto Cleanup** — Deletes old files automatically

---

## 📊 Stats

- **Lines of Code**: ~800 (backend) + ~400 (frontend)
- **Max File Size**: 20 MB
- **File Retention**: 24 hours
- **Rate Limit**: 30 req/min per IP
- **Supported Formats**: 5 (PNG, JPEG, GIF, WEBP, BMP)

---

## 📄 License

MIT License — Free to use for personal and commercial projects. ✅

---

## 👤 Creator

Built by **Prajjwal Nag** 
*AI Automation Expert | Software Engineer | Entrepreneur*

### 🔗 Connect

[![GitHub](https://img.shields.io/badge/GitHub-prajjwalnag-black?style=flat&logo=github)](https://github.com/prajjwalnag)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-prajjwalnag-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/prajjwalnag/)
[![Instagram](https://img.shields.io/badge/Instagram-@mwragency-E4405F?style=flat&logo=instagram)](https://www.instagram.com/mwragency/)
[![Facebook](https://img.shields.io/badge/Facebook-mwragency-1877F2?style=flat&logo=facebook)](https://www.facebook.com/mwragency)

---

## 🤝 Contributing

Found a bug? Have an idea? 
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/prajjwalnag/base64server/issues)
- 💡 **Pull Requests**: All contributions welcome!

---

## ⭐ Show Your Support

If this project helped you, please consider:
- ⭐ **Star** this repository
- 📢 **Share** with others
- 💬 **Give feedback** on GitHub

---

**Made with ❤️ by Prajjwal Nag**

*Last Updated: August 2026*
