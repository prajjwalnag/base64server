# Base64 Image Converter

A fast, secure, and professional-grade Flask web application for converting between base64 strings and image files. Built with a dark-mode UI, comprehensive API, and production-ready security features.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/prajjwalnag/base64server.git
cd base64server

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Server

**Development:**
```bash
python app.py
```
The app will start at `http://localhost:5000`

**Production:**
```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

For production on a different port:
```bash
gunicorn app:app --bind 0.0.0.0:8000
```

---

## Features

### Web Interface
- **Decode Base64 → Image**: Paste base64 strings and download as image files
- **Encode Image → Base64**: Upload images and get base64 output
- **Dark Theme UI**: Modern, professional design with responsive layout
- **Real-time Stats**: See file sizes and conversion metrics
- **Copy to Clipboard**: One-click copying of base64 strings and URLs
- **Drag-and-Drop**: Upload images by dragging them into the drop zone

### API
- **RESTful Endpoints**: Full programmatic access
- **Multiple Formats**: Supports PNG, JPEG, GIF, WEBP, BMP
- **Two Decode Modes**: 
  - Binary: Download image directly
  - URL: Save to server and get shareable link
- **Rate Limiting**: Built-in protection against abuse
- **Security Headers**: CSP, XSS protection, clickjacking prevention
- **Auto File Cleanup**: Files older than 24 hours automatically deleted

### Backend
- **Fast Image Detection**: Magic byte verification (not by extension)
- **20 MB File Limit**: Prevents resource exhaustion
- **Rate Limiting**: 30 requests/minute per IP, 50/hour globally, 200/day globally
- **Thread-Safe**: Automatic cleanup thread manages file retention

---

## API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

---

### 1. Decode Base64 to Image

**Endpoint:** `POST /api/v1/decode`

**Default Mode (Binary Download):**

Send base64 data and receive image file directly.

```bash
curl -X POST http://localhost:5000/api/v1/decode \
  -H "Content-Type: application/json" \
  -d '{"data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="}' \
  -o image.png
```

**Request Format:**
```json
{
  "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
}
```

**URL Mode (Save to Server):**

Send `"mode": "url"` to save the image and get a shareable URL.

```bash
curl -X POST http://localhost:5000/api/v1/decode \
  -H "Content-Type: application/json" \
  -d '{"data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==", "mode": "url"}'
```

**Response (URL Mode):**
```json
{
  "url": "http://localhost:5000/api/v1/files/abc123def456.png",
  "mime_type": "image/png",
  "filename": "abc123def456.png"
}
```

**Supports Data URLs:**
You can also send data URLs with the prefix:
```json
{
  "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
}
```

**Error Responses:**
```json
{"error": "No base64 data provided"}                    // 400
{"error": "Invalid base64 data"}                        // 400
{"error": "Decoded data is not a recognized image"}    // 400
{"error": "Rate limit exceeded. Max 30 requests/min."} // 429
```

---

### 2. Encode Image to Base64

**Endpoint:** `POST /api/v1/encode`

Upload an image file and receive base64 encoding.

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/v1/encode \
  -F "file=@/path/to/image.png"
```

**Response:**
```json
{
  "mime_type": "image/png",
  "base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
  "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
}
```

**Error Responses:**
```json
{"error": "No file provided"}                    // 400
{"error": "Uploaded file is not a recognized image"} // 400
{"error": "File too large"}                     // 413
{"error": "Rate limit exceeded"}                // 429
```

---

### 3. Retrieve Saved File

**Endpoint:** `GET /api/v1/files/<filename>`

Download a file previously saved with `mode: "url"`.

**Example:**
```bash
curl http://localhost:5000/api/v1/files/abc123def456.png -o image.png
```

**Error Responses:**
```json
{"error": "File not found"} // 404
```

---

## Code Examples

### Python

```python
import requests

# Upload image → Base64
with open('photo.png', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/v1/encode',
        files={'file': f}
    )
    data = response.json()
    print("Base64:", data['base64'])
    print("Data URL:", data['data_url'])

# Base64 → Download Image
base64_str = data['base64']
response = requests.post(
    'http://localhost:5000/api/v1/decode',
    json={'data': base64_str}
)
with open('decoded.png', 'wb') as f:
    f.write(response.content)

# Base64 → Save on Server (URL Mode)
response = requests.post(
    'http://localhost:5000/api/v1/decode',
    json={'data': base64_str, 'mode': 'url'}
)
data = response.json()
print("File URL:", data['url'])
```

### JavaScript

```javascript
// Upload image → Base64
const fileInput = document.querySelector('input[type="file"]');
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:5000/api/v1/encode', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log('Base64:', data.base64);
console.log('MIME:', data.mime_type);

// Base64 → Image URL
const decodeResponse = await fetch('http://localhost:5000/api/v1/decode', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ data: data.base64 })
});

const blob = await decodeResponse.blob();
const imageUrl = URL.createObjectURL(blob);
document.querySelector('img').src = imageUrl;
```

### Node.js / TypeScript

```typescript
import axios from 'axios';
import fs from 'fs';

const API = 'http://localhost:5000/api/v1';

// Encode
async function encodeImage(filePath: string) {
  const file = fs.readFileSync(filePath);
  const formData = new FormData();
  formData.append('file', new Blob([file]));

  const response = await axios.post(`${API}/encode`, formData);
  return response.data;
}

// Decode
async function decodeImage(base64: string) {
  const response = await axios.post(`${API}/decode`, { data: base64 }, {
    responseType: 'arraybuffer'
  });
  return response.data;
}
```

---

## Configuration

### Environment Variables

Set these for production deployments:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### Adjust Rate Limits

Edit `app.py` to customize rate limiting:

```python
# Per-endpoint limit (line ~80)
@app.route("/api/v1/decode", methods=["POST"])
@limiter.limit("50 per minute")  # Change to higher/lower as needed
def decode():
    ...

# Global limits (line ~44)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["300 per day", "100 per hour"],  # Adjust defaults
)
```

### Enable CORS (For Cross-Domain Requests)

If your frontend runs on a different domain, add CORS:

```python
# Add to app.py
from flask_cors import CORS
CORS(app)
```

Then install: `pip install flask-cors`

---

## Deployment

### Local/Development
```bash
python app.py
```

### Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

**Build & Run:**
```bash
docker build -t base64server .
docker run -p 5000:5000 base64server
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Production Checklist
- [ ] Use Gunicorn or uWSGI (not Flask dev server)
- [ ] Deploy behind Nginx/Apache reverse proxy
- [ ] Enable HTTPS/SSL
- [ ] Set `FLASK_ENV=production`
- [ ] Use Redis for rate limiting across multiple instances
- [ ] Monitor disk space (files expire after 24 hours)
- [ ] Set up log rotation
- [ ] Use environment variables for configuration

---

## Troubleshooting

### Port 5000 already in use
```bash
# Use a different port
python -c "from app import app; app.run(port=5001)"

# Or find and kill the process using port 5000
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

### Rate limit errors during testing
Temporarily increase limits in `app.py`:
```python
@limiter.limit("1000 per minute")  # Lenient for testing
def decode():
    ...
```

### Files not being deleted
The cleanup thread runs every 10 minutes. Check file modification times:
```bash
ls -la base64server/files/
```

### Memory issues with large files
The app accepts up to 20 MB per file. To adjust:
```python
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB in app.py
```

---

## Security

- **Content Security Policy**: Restricts script execution and resource loading
- **Magic Byte Validation**: Verifies images by content, not extension
- **Rate Limiting**: Prevents brute force and resource exhaustion
- **XSS Protection**: Safe DOM manipulation, no innerHTML with user input
- **Clickjacking Prevention**: X-Frame-Options headers
- **File Cleanup**: Automatic deletion of old files prevents disk exhaustion

---

## File Structure

```
base64server/
├── app.py                    # Flask app & API endpoints
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── templates/
│   └── index.html           # Web UI (dark theme)
├── files/                   # Temporary image storage (auto-cleaned)
└── .gitignore               # Git ignore rules
```

---

## Support & Contact

Built by **Prajjwal Nag** - AI Automation Expert & Software Engineer

- **GitHub**: [prajjwalnag](https://github.com/prajjwalnag)
- **Facebook**: [mwragency](https://www.facebook.com/mwragency)
- **Instagram**: [@mwragency](https://www.instagram.com/mwragency/)
- **LinkedIn**: [prajjwalnag](https://www.linkedin.com/in/prajjwalnag/)

---

## License

MIT License - Free to use for personal and commercial projects.

Feel free to fork, modify, and distribute. See LICENSE file for details.

---

## Contributing

Found a bug? Have a feature request? Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Made with ❤️ by Prajjwal Nag**
