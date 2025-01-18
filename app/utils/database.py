from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseManager(metaclass=SingletonMeta):
    def __init__(self):
        self.engine = None
        self.SessionLocal = None

    def init_app(self, app):
        try:
            self.engine = create_engine(
                app.config['SQLALCHEMY_DATABASE_URI'],
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30
            )
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        except SQLAlchemyError as e:
            print(f"Error initializing database: {e}")
            raise

    def execute_query(self, query, params=None):
        with self.SessionLocal() as session:
            try:
                if isinstance(query, str):
                    query = text(query)
                result = session.execute(query, params or {})
                if query.text.strip().upper().startswith('SELECT'):
                    return [dict(row._mapping) for row in result]
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                raise