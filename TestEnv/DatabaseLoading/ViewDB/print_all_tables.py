import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from API.Codebase.DB.database import Database
from sqlalchemy import inspect

def print_all_tables():
    db = Database()
    inspector = inspect(db.engine)

    try:
        tables = inspector.get_table_names()

        if not tables:
            print("No tables found in the database.")
            return

        print("\nList of all tables in the database:")
        for table in tables:
            print(f"- {table}")

    except Exception as e:
        print(f"Error retrieving tables: {e}")

if __name__ == "__main__":
    print_all_tables()
