from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

class Database:
    def __init__(self):
        db_url = "mysql+pymysql://root:pass123@localhost/flask_db"

        self.engine = create_engine(db_url)
        self.Base = declarative_base()
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.SessionLocal()

    def close_session(self, session):
        session.close()
