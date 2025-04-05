import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils import generate_all_styles

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "backend/uploads"
OUTPUT_FOLDER = "backend/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 获取服务器 IP 地址
def get_server_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

SERVER_IP = get_server_ip()

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file uploaded"})

    file = request.files["file"]
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in [".wav", ".mp3", ".m4a"]:
        return jsonify({"success": False, "message": "Unsupported file format"})

    filename = str(uuid.uuid4()) + ext
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # 调用utils生成风格图案
    output_files = generate_all_styles(file_path, OUTPUT_FOLDER, filename)

    # 返回所有风格图案的URL
    image_urls = {}
    for style, file_name in output_files.items():
        image_urls[style] = f"http://{SERVER_IP}:5000/image/{file_name}"

    return jsonify({"success": True, "images": image_urls})

@app.route("/image/<filename>")
def get_image(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
