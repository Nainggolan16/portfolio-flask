import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        # SQLAlchemy menggunakan driver pymysql
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace(
            "mysql://",
            "mysql+pymysql://",
            1
        )
    else:
        raise RuntimeError("DATABASE_URL belum diatur.")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # Resend
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")