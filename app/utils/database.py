from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from ..config import Config  # Importăm configurările

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class LocalMySQL(metaclass=SingletonMeta):
    def __init__(self):
        # Preluăm configurările din Config
        self.host = Config.SQLALCHEMY_DATABASE_URI.split('@')[1].split(':')[0]
        self.port = int(Config.SQLALCHEMY_DATABASE_URI.split(':')[2].split('/')[0])
        self.user = Config.SQLALCHEMY_DATABASE_URI.split('//')[1].split(':')[0]
        self.password = Config.SQLALCHEMY_DATABASE_URI.split(':')[1].split('@')[0][2:]
        self.database = Config.SQLALCHEMY_DATABASE_URI.split('/')[-1]
        self.engine = None
        self.create_engine()

    def create_engine(self):
        try:
            self.engine = create_engine(
                f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}',
                pool_pre_ping=True
            )
            print("SQLAlchemy engine created")
        except SQLAlchemyError as e:
            print(f"Error creating SQLAlchemy engine: {e}")
            raise

    def execute_query(self, query, params=None):
        try:
            with self.engine.connect() as connection:
                if isinstance(query, str):
                    query = text(query)
                result = connection.execute(query, params or {})
                if query.text.strip().upper().startswith('SELECT'):
                    return [dict(row._mapping) for row in result]
                else:
                    connection.commit()
                    return True
        except SQLAlchemyError as e:
            print(f"Error executing query: {e}")
            raise

    def close(self):
        if self.engine:
            self.engine.dispose()
