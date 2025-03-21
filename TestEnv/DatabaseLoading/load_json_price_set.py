import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from sqlalchemy import Column, Integer, String, Float, Table, MetaData, inspect
from API.Codebase.DB.database import Database
from TestEnv.DatabaseLoading.get_highest_set_id import get_highest_set_id


def load_json_price_set(json_file):
    db = Database()

    with open(json_file, "r") as f:
        schema = json.load(f)

    price_set = schema["price_set"]
    hospital_name = price_set["Hospital_Name"]
    address = price_set["Address"]
    date_of_set = price_set["date_of_release"]

    latest_set = get_highest_set_id()
    new_set_id = latest_set + 1
    new_table_name = f"set_{new_set_id}"

    session = db.get_session()
    try:
        session.execute(
            f"INSERT INTO set_control (hospital_name, address, date_of_set, set_id) VALUES (:hospital_name, :address, :date_of_set, :set_id)",
            {
                "hospital_name": hospital_name,
                "address": address,
                "date_of_set": date_of_set,
                "set_id": new_set_id
            }
        )
        session.commit()
        print(f"Added set_control entry for Set ID {new_set_id}")


    except Exception as e:
        session.rollback()
        inspector = inspect(db.engine)

        if not inspector.has_table("set_control"):
            metadata = MetaData()
            Table(
                "set_control", metadata,
                Column("set_id", Integer, primary_key=True),
                Column("hospital_name", String(255)),
                Column("address", String(255)),
                Column("date_of_set", String(100))
            )
            metadata.create_all(db.engine)
            try:
                session.execute(
                    f"INSERT INTO set_control (hospital_name, address, date_of_set, set_id) VALUES (:hospital_name, :address, :date_of_set, :set_id)",
                    {
                        "hospital_name": hospital_name,
                        "address": address,
                        "date_of_set": date_of_set,
                        "set_id": new_set_id
                    }
                )
                session.commit()

            except Exception as inner_e:
                session.rollback()
                print(f"Retry failed: {inner_e}")
                return
        else:
            print("'set_control' table exists. Error still.")
            return

    finally:
        db.close_session(session)

    metadata = MetaData()
    items_table = Table(
        new_table_name, metadata,
        Column("item_id", Integer, primary_key=True),
        Column("description", String(255)),
        Column("price", Float)
    )

    metadata.create_all(db.engine)
    print(f"Created new table: {new_table_name}")

    session = db.get_session()
    try:
        items = schema["items"]
        for item in items:
            session.execute(
                f"INSERT INTO {new_table_name} (item_id, description, price) VALUES (:item_id, :description, :price)",
                {
                    "item_id": item["itemID"],
                    "description": item["description"],
                    "price": item["price"]
                }
            )
        session.commit()
        print(f"Inserted {len(items)} items into {new_table_name}")

    except Exception as e:
        session.rollback()
        print(f"Error inserting items: {e}")

    finally:
        db.close_session(session)


# Run the script
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, "medical1.json")
    load_json_price_set(json_file_path)
