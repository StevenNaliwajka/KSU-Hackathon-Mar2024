from API.Codebase.DB.database import Database
from sqlalchemy.sql import text


def print_named_set(table_name):
    db = Database()
    session = db.get_session()

    try:
        result = session.execute(text(f"SELECT * FROM {table_name}")).fetchall()

        if not result:
            print(f"Table '{table_name}' is empty or does not exist.")
            return

        print(f"\nContents of '{table_name}':")
        for row in result:
            print(row)

    except Exception as e:
        print(f"Error retrieving '{table_name}': {e}")

    finally:
        db.close_session(session)


if __name__ == "__main__":
    table_to_print = "set3"
    print_named_set(table_to_print)
