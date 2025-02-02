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

    # JWT 
    JWT_SECRET_KEY = "wHqoz5_UPWcLAf6ywL3A4TOfUs6hl7j7Pik0u9ekNZfyHsoQUD-P3g-RP03lBokeT-FR2qgqAmivDTJlTJw5e-BZqYVw5pL7-k_1HU8wqJOp5NYWTVj_KgT-1qLya925ddVh6-K6_wFbohrlCE-_WqJU1Zgpjli0V3vr6HhbOD4"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
