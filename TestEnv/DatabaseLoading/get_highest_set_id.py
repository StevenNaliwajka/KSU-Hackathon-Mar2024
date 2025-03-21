from API.Codebase.DB.connect_to_db import connect_to_db


def get_highest_set_id():
    # gets highest set from set ctrl tble
    db = connect_to_db()
    session = db.get_session()
    try:
        result = session.execute("SELECT MAX(set_ID) FROM set_control").fetchone()
        highest_id = result[0] if result[0] is not None else 0
        return highest_id
    except Exception as e:
        print(f"Error querying set_control: {e}")
        return 0
    finally:
        db.close_session(session)