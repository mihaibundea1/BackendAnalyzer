class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin_password@localhost:3308/myapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False