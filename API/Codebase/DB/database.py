'''
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.create_tables()

        self.Base = declarative_base()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def add_user(self, name, age):
        session = self.SessionLocal()
        try:
            new_user = User(name=name, age=age)
            session.add(new_user)
            session.commit()
            print(f"User {name} added successfully!")
        except Exception as e:
            session.rollback()
            print(f"Error adding user: {e}")
        finally:
            session.close()

    def get_users(self):
        """Retrieve all users from the database."""
        session = self.SessionLocal()
        try:
            users = session.query(User).all()
            return [{"id": user.id, "name": user.name, "age": user.age} for user in users]
        finally:
            session.close()
'''