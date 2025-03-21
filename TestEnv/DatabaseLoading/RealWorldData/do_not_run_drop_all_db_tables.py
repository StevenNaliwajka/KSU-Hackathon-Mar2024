import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from API.Codebase.DB.database import Database
from sqlalchemy import MetaData

def drop_all_tables():
    db = Database()
    metadata = MetaData()

    try:
        metadata.reflect(bind=db.engine)
        metadata.drop_all(bind=db.engine)
        print("All tables dropped successfully!")

    except Exception as e:
        print(f"Error dropping tables: {e}")

if __name__ == "__main__":
    confirm = input("This will delete ALL TABLES in the database. Type 'YES' to confirm: ")
    if confirm == "YES":
        drop_all_tables()
    else:
        print("Operation cancelled.")
