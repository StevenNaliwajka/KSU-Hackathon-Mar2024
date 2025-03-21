from API.Codebase.DB.database import Database
from sqlalchemy.sql import text

def get_set_list(zip_3_dig):
    db = Database()
    session = db.get_session()

    try:
        query = text("SELECT set_id, zip FROM set_control")
        result = session.execute(query).fetchall()

        matching_set_ids = []
        for row in result:
            zip_code = str(row.zip).strip()
            if zip_code.startswith(zip_3_dig):
                matching_set_ids.append(row.set_id)

        return matching_set_ids

    except Exception as e:
        print(f"Error querying set_control: {e}")
        return []

    finally:
        db.close_session(session)
