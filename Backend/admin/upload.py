import cloudinary
import cloudinary.uploader


def init_cloudinary(app):
    """
    Inisialisasi Cloudinary.
    Dipanggil sekali saat aplikasi dijalankan.
    """

    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"],
        secure=True
    )


def upload_image(file, folder="portfolio"):
    """
    Upload file ke Cloudinary.
    Mengembalikan URL gambar.
    """

    if file is None:
        return None

    result = cloudinary.uploader.upload(
        file,
        folder=folder
    )

    return result["secure_url"]