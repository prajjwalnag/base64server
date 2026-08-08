# Base64 Image Converter

A modern, high-performance Flask web application for converting between base64 strings and image files. Features a stunning, production-grade UI with advanced animations and a robust API with rate limiting.

## Features

### 🎨 UI
- **Dual-mode interface**: Decode base64 to images and encode images to base64
- **Visually stunning design** with animated gradients, glassmorphism effects, and smooth micro-interactions
- **Responsive layout** works seamlessly on desktop, tablet, and mobile
- **Real-time file stats**: View original size, base64 size, and size increase percentage
- **Loading states** with elegant animations
- **Copy to clipboard** functionality with success feedback
- **Drag-and-drop** support for image uploads

### 🔒 Rate Limiting
- **30 requests per minute** per IP address for each endpoint
- **200 requests per day** global limit per IP
- **50 requests per hour** global limit per IP
- Graceful rate limit error messages

### 🛠️ API
- **RESTful endpoints** for programmatic access
- **JSON responses** with detailed error handling
- **File size limit**: 20 MB max
- **Supported formats**: PNG, JPEG, GIF, WEBP, BMP

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
cd base64server

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

For production, use a production-grade server like Gunicorn:
```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

## API Documentation

### Endpoints

#### 1. Decode Base64 → Image
**POST** `/api/v1/decode`

Convert a base64 string to an image file.

**Request:**
```json
{
  "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
}
```

Supports optional `data:image/...;base64,` prefix:
```json
{
  "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
}
```

By default the decoded image is returned as a binary file. Pass `"mode": "url"` to instead have the server save the file to disk and return a URL to it:
```json
{
  "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
  "mode": "url"
}
```

**Response (`mode: "binary"`, default):**
- Returns image file as binary with correct MIME type
- Supported formats: PNG, JPEG, GIF, WEBP, BMP

**Response (`mode: "url"`):**
```json
{
  "url": "http://localhost:5000/api/v1/files/56a6f648ac7245f9ab042f68e04c34c5.png",
  "mime_type": "image/png",
  "filename": "56a6f648ac7245f9ab042f68e04c34c5.png"
}
```

The file is saved under `base64server/files/`. A background thread inside the app automatically deletes files older than 24 hours, sweeping every 10 minutes — no external cron job needed.

**Error Responses:**
```json
{"error": "No base64 data provided"}                          // 400
{"error": "Invalid base64 data"}                              // 400
{"error": "Decoded data is not a recognized image format"}    // 400
{"error": "Rate limit exceeded. Max 30 requests per minute."} // 429
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/v1/decode \
  -H "Content-Type: application/json" \
  -d '{"data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="}' \
  -o image.png
```

---

#### 2. Encode Image → Base64
**POST** `/api/v1/encode`

Convert an image file to a base64 string.

**Request (multipart form-data):**
```bash
curl -X POST http://localhost:5000/api/v1/encode \
  -F "file=@path/to/image.png"
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
{"error": "No file provided"}                                 // 400
{"error": "Uploaded file is not a recognized image format"}   // 400
{"error": "File too large"}                                   // 413
{"error": "Rate limit exceeded. Max 30 requests per minute."} // 429
```

**Python Example:**
```python
import requests

# Encode image to base64
with open('image.png', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/api/v1/encode', files=files)
    data = response.json()
    print(data['base64'])
    print(data['data_url'])

# Decode base64 to image
response = requests.post('http://localhost:5000/api/v1/decode',
    json={'data': data['base64']})
with open('decoded.png', 'wb') as f:
    f.write(response.content)
```

**JavaScript/Fetch Example:**
```javascript
// Encode
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://localhost:5000/api/v1/encode', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.base64);      // base64 string
console.log(data.data_url);    // data URL
console.log(data.mime_type);   // image/png

// Decode
const decodeResponse = await fetch('http://localhost:5000/api/v1/decode', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ data: data.base64 })
});

const imageBlob = await decodeResponse.blob();
const imageUrl = URL.createObjectURL(imageBlob);
```

---

#### 3. Fetch a Saved File
**GET** `/api/v1/files/<filename>`

Downloads a file previously saved via `/api/v1/decode` with `"mode": "url"`.

**Error Responses:**
```json
{"error": "File not found"} // 404
```

---

### Legacy Endpoint
`/api/decode` is an alias for `/api/v1/decode` for backwards compatibility.

---

## Rate Limiting

The API implements strict rate limiting to prevent abuse:

| Limit | Value |
|-------|-------|
| Per minute (per endpoint) | 30 requests |
| Per hour (global) | 50 requests |
| Per day (global) | 200 requests |

**Rate Limit Response:**
```
HTTP 429 Too Many Requests
{
  "error": "Rate limit exceeded. Max 30 requests per minute."
}
```

The UI automatically handles rate limit errors and displays user-friendly messages.

---

## Configuration

### Environment Variables
None required for basic setup. For production:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### Modifying Rate Limits

Edit `app.py` to adjust limits:

```python
# Change per-endpoint limit
@app.route("/api/v1/decode", methods=["POST"])
@limiter.limit("50 per minute")  # Change this value
def decode():
    ...

# Change global limits
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["300 per day", "100 per hour"],  # Edit these
)
```

---

## File Structure

```
base64server/
├── app.py                 # Flask application with API endpoints
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend UI (HTML/CSS/JS)
├── files/                 # Decoded images saved when mode="url" (gitignored, auto-cleaned after 24h)
└── README.md             # This file
```

---

## Dependencies

- **Flask 3.0.3**: Web framework
- **Flask-Limiter 3.5.0**: Rate limiting

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## Design & UX

### Frontend Highlights
- **Custom Typography**: Sora (modern sans-serif) + Courier Prime (monospace code)
- **Animated Gradients**: Multi-layered animated background with floating orbs
- **Glassmorphism**: Frosted glass effect with backdrop blur
- **Micro-interactions**: Smooth transitions, hover effects, physics-based animations
- **Data Visualization**: File size stats with visual hierarchy
- **Accessibility**: Semantic HTML, clear error messages, keyboard-friendly

### Performance
- Minimal dependencies
- Efficient image format detection via magic bytes
- In-memory rate limiting (suitable for single-instance deployments)
- Optimized CSS animations (GPU-accelerated)

---

## API Best Practices

### When to Use Each Endpoint

**Decode** (`/api/v1/decode`):
- Convert stored base64 strings to downloadable images
- Render base64 data URLs in web/mobile apps
- Convert clipboard base64 to image files

**Encode** (`/api/v1/encode`):
- Upload images for storage or transmission as base64
- Convert user-selected images to data URLs
- Prepare images for APIs that accept base64

### Error Handling

Always check the HTTP status code:

```javascript
const response = await fetch('http://localhost:5000/api/v1/encode', {
  method: 'POST',
  body: formData
});

if (!response.ok) {
  const error = await response.json();
  console.error(`Error: ${error.error}`);
  return;
}

const data = await response.json();
```

### Handling Rate Limits

Implement exponential backoff for client-side retries:

```python
import time
import requests

def request_with_retry(url, method='GET', max_retries=3, **kwargs):
    for attempt in range(max_retries):
        response = requests.request(method, url, **kwargs)
        if response.status_code == 429:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
            continue
        return response
    raise Exception("Max retries exceeded")
```

---

## Troubleshooting

### "Address already in use"
The default port 5000 is already in use. Specify a different port:
```bash
python -c "from app import app; app.run(port=5001)"
```

### Rate limit errors in development
Adjust limits in `app.py`:
```python
@limiter.limit("1000 per minute")  # More lenient for testing
def decode():
```

### CORS issues
If accessing from a different domain, add CORS headers:
```python
from flask_cors import CORS
CORS(app)
```

---

## Deployment

### Heroku
```bash
pip install gunicorn
echo "web: gunicorn app:app" > Procfile
git push heroku main
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

### Production Recommendations
- Use Gunicorn or uWSGI instead of Flask's development server
- Deploy behind Nginx or Apache
- Use Redis for distributed rate limiting across multiple instances
- Enable HTTPS/SSL
- Set `FLASK_ENV=production`
- Use environment variables for secrets

---

## Credits & Attribution

### Leadership & Vision
- **Claude Ford** - Project Lead at [Rigmi](https://rigmi.com)

### Development
- **MWR Agency** - Product Design & Implementation
- **AI-Assisted Development** - Built with Claude Code

### Special Thanks
This project was developed under the leadership and vision of Claude Ford at Rigmi, with design and implementation by MWR Agency, leveraging advanced AI development tools.

---

## License

MIT License - feel free to use for personal and commercial projects.

---

## Contributing

Found a bug or have a feature request? Feel free to open an issue or submit a PR!

---

**Made with** ✨ **by MWR Agency**
