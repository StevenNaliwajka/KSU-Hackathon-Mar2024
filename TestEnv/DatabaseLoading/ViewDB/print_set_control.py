import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from API.Codebase.DB.database import Database
from sqlalchemy.sql import text


def print_set_control():
    db = Database()
    session = db.get_session()

    try:
        result = session.execute(text("SELECT * FROM set_control")).fetchall()

        if not result:
            print("'set_control' table is empty or does not exist.")
            return

        print("\nContents of 'set_control':")
        for row in result:
            print(row)

    except Exception as e:
        print(f"Error retrieving 'set_control': {e}")

    finally:
        db.close_session(session)


if __name__ == "__main__":
    print_set_control()
