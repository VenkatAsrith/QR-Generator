from flask import Flask, request, jsonify, redirect, send_file
from flask_cors import CORS
import uuid
import os
import tempfile
from dotenv import load_dotenv

from db import qr_collection
from qr_utils import generate_qr_image
from cloudinary_utils import upload_qr_image
from pdf_utils import generate_pdf

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/api/qr/generate", methods=["POST"])
def generate_qr():
    data = request.json
    qr_name = data.get("name")
    target_url = data.get("link")

    if not qr_name or not target_url:
        return jsonify({"error": "Missing fields"}), 400

    qr_id = str(uuid.uuid4())
    redirect_url = f"{os.getenv('BACKEND_URL')}/q/{qr_id}"

    temp_dir = tempfile.gettempdir()
    png_path = os.path.join(temp_dir, f"{qr_id}.png")
    # pdf_path is not used here, removing it to avoid confusion or adding it later if needed

    # Generate QR (Static: points directly to target_url)
    generate_qr_image(target_url, png_path)

    # Upload to Cloudinary
    qr_image_url = upload_qr_image(png_path, qr_id)

    # Save in MongoDB
    qr_collection.insert_one({
        "qr_id": qr_id,
        "name": qr_name,
        "target_url": target_url,
        "qr_image": qr_image_url,
        "type": "static"  # Mark as static for clarity
    })

    return jsonify({
        "qr_id": qr_id,
        "qr_image": qr_image_url
    })


@app.route("/q/<qr_id>")
def redirect_qr(qr_id):
    # This route is no longer used for new static QRs but kept for backward compatibility
    qr = qr_collection.find_one({"qr_id": qr_id})
    if not qr:
        return "QR not found", 404
    return redirect(qr["target_url"])


@app.route("/api/qr/download/pdf/<qr_id>")
def download_pdf(qr_id):
    qr = qr_collection.find_one({"qr_id": qr_id})
    if not qr:
        return "QR not found", 404

    temp_dir = tempfile.gettempdir()
    png_path = os.path.join(temp_dir, f"{qr_id}.png")
    pdf_path = os.path.join(temp_dir, f"{qr_id}.pdf")

    # Regenerate QR with target_url (Static)
    generate_qr_image(qr["target_url"], png_path)
    generate_pdf(png_path, qr["name"], pdf_path)

    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
