# Kana design for quickly transport.
import os
import sys
import socket
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename
import time
import uuid

if getattr(sys, "frozen", False):
    bundle_dir = sys._MEIPASS
    current_dir = os.path.dirname(sys.executable)
    template_path = os.path.join(bundle_dir, "templates")
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "templates")

app = Flask(__name__, template_folder=template_path)

BASE_UPLOAD_FOLDER = os.path.join(current_dir, "upload")
app.config["UPLOAD_FOLDER"] = BASE_UPLOAD_FOLDER


FILE_EXTENSIONS = {
    "🗂️ 文件": [
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
        ".md",
    ],
    "🖼️ 圖片": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "🎬 影音": [".mp4", ".mkv", ".avi", ".mp3", ".wav", ".flac"],
    "📦 压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
}


EXT_TO_CATEGORY = {
    ext: category for category, exts in FILE_EXTENSIONS.items() for ext in exts
}


def get_file_category(filename):
    _, ext = os.path.splitext(filename.lower())
    return EXT_TO_CATEGORY.get(ext, "📝 其他")


def init_folders():
    if not os.path.exists(BASE_UPLOAD_FOLDER):
        os.makedirs(BASE_UPLOAD_FOLDER)
    for category in FILE_EXTENSIONS.keys():
        cat_path = os.path.join(BASE_UPLOAD_FOLDER, category)
        if not os.path.exists(cat_path):
            os.makedirs(cat_path)
    other_path = os.path.join(BASE_UPLOAD_FOLDER, "📝 其他")
    if not os.path.exists(other_path):
        os.makedirs(other_path)


init_folders()


@app.route("/")
def index():
    file_structure = {}

    current_ip = get_lan_ip()
    port = 5000
    lan_url = f"http://{current_ip}:{port}"

    if os.path.exists(BASE_UPLOAD_FOLDER):
        for category in os.listdir(BASE_UPLOAD_FOLDER):
            cat_path = os.path.join(BASE_UPLOAD_FOLDER, category)
            if os.path.isdir(cat_path):
                file_structure[category] = []
                for filename in os.listdir(cat_path):
                    if not filename.startswith("."):
                        file_structure[category].append(filename)

    return render_template("index.html", file_structure=file_structure, lan_url=lan_url)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "沒有选择档案", 400

    f = request.files["file"]
    if f.filename == "":
        return "档名为空", 400

    if f:
        original_filename = os.path.basename(f.filename)
        name, ext = os.path.splitext(original_filename)
        timestamp = int(time.time())
        safe_filename = f"{name}_{timestamp}{ext}"
        category = get_file_category(original_filename)
        save_dir = os.path.join(app.config["UPLOAD_FOLDER"], category)
        f.save(os.path.join(save_dir, safe_filename))
        return redirect(url_for("index"))


@app.route("/download/<category>/<path:filename>")
def download_file(category, filename):
    target_dir = os.path.join(app.config["UPLOAD_FOLDER"], category)
    return send_from_directory(target_dir, filename, as_attachment=True)


@app.route("/delete/<category>/<path:filename>", methods=["POST"])
def delete_file(category, filename):
    target_dir = os.path.join(app.config["UPLOAD_FOLDER"], category)
    file_path = os.path.join(target_dir, filename)

    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            print(f"🗑️ 档案已删除: {file_path}")
        else:
            print(f"⚠️ 找不到准备删除档案: {file_path}")
    except Exception as e:
        print(f"❌ 删除档案时出错: {str(e)}")
        return f"刪除失败 {str(e)}", 500

    return redirect(url_for("index"))


def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 5000
    lan_ip = get_lan_ip()

    print("\n" + "=" * 50)
    print("🚀 档案共享中心已将开启！")
    print(f"💻 访问请打开：http://localhost:{PORT}")
    print("=" * 50 + "\n")

    app.run(host=HOST, port=PORT, debug=False)
