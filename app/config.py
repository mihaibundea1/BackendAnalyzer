import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin_password@localhost:3308/myapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Blackblaze S3
    APPLICATION_KEY_ID = os.getenv("B2_APPLICATION_KEY_ID")
    APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY")
    BUCKET_NAME = 'medical-images'
