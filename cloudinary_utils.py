import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

def upload_qr_image(file_path, public_id):
    result = cloudinary.uploader.upload(
        file_path,
        folder="dynamic_qrs",
        public_id=public_id,
        overwrite=True
    )
    return result["secure_url"]
