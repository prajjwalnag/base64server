import base64
import binascii
import io
import uuid

from flask import Flask, jsonify, request, send_file, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
)
app.config["RATELIMIT_STORAGE_URL"] = "memory://"

SIGNATURES = {
    b"\xff\xd8\xff": ("image/jpeg", "jpg"),
    b"\x89PNG\r\n\x1a\n": ("image/png", "png"),
    b"GIF87a": ("image/gif", "gif"),
    b"GIF89a": ("image/gif", "gif"),
    b"RIFF": ("image/webp", "webp"),
    b"BM": ("image/bmp", "bmp"),
}


def detect_image_type(data: bytes):
    for signature, info in SIGNATURES.items():
        if data.startswith(signature):
            return info
    return None, None


def strip_data_url_prefix(raw: str) -> str:
    if raw.strip().startswith("data:") and ";base64," in raw:
        return raw.split(";base64,", 1)[1]
    return raw


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/v1/decode", methods=["POST"])
@limiter.limit("30 per minute")
def decode():
    payload = request.get_json(silent=True) or {}
    b64_data = payload.get("data") or request.form.get("data")

    if not b64_data:
        return jsonify({"error": "No base64 data provided"}), 400

    b64_data = strip_data_url_prefix(b64_data)

    try:
        image_bytes = base64.b64decode(b64_data, validate=True)
    except (binascii.Error, ValueError):
        return jsonify({"error": "Invalid base64 data"}), 400

    mime_type, extension = detect_image_type(image_bytes)
    if mime_type is None:
        return jsonify({"error": "Decoded data is not a recognized image format"}), 400

    filename = f"{uuid.uuid4().hex}.{extension}"
    return send_file(
        io.BytesIO(image_bytes),
        mimetype=mime_type,
        as_attachment=True,
        download_name=filename,
    )


@app.route("/api/v1/encode", methods=["POST"])
@limiter.limit("30 per minute")
def encode():
    uploaded = request.files.get("file")
    if uploaded is None or uploaded.filename == "":
        return jsonify({"error": "No file provided"}), 400

    image_bytes = uploaded.read()
    mime_type, _extension = detect_image_type(image_bytes)
    if mime_type is None:
        return jsonify({"error": "Uploaded file is not a recognized image format"}), 400

    encoded = base64.b64encode(image_bytes).decode("ascii")
    return jsonify({
        "mime_type": mime_type,
        "base64": encoded,
        "data_url": f"data:{mime_type};base64,{encoded}",
    })


# Backwards-compatible alias for the unversioned route.
app.add_url_rule("/api/decode", view_func=decode, methods=["POST"])


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "File too large"}), 413


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Rate limit exceeded. Max 30 requests per minute."}), 429


if __name__ == "__main__":
    app.run(debug=True)
