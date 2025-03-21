import csv
import os
import re
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from sqlalchemy import Column, Integer, String, Float, Table, MetaData, inspect
from sqlalchemy.sql import text
from API.Codebase.DB.database import Database
from TestEnv.DatabaseLoading.get_highest_set_id import get_highest_set_id


def load_wellstar_pricing_data(csv_file):
    db = Database()

    # Read CSV File
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Extract Metadata (Second Row Contains Hospital Information)
    # Second row has hospital metadata
    metadata_row = rows[1]
    # "hospital_name"
    hospital_name = metadata_row[0]
    # "last_updated_on"
    date_of_set = metadata_row[1]
    # "hospital_address"
    address = metadata_row[4]

    match = re.search(r'\b\d{5}\b$', address.strip())
    zip_code = match.group() if match else None
    print(zip_code)

    # Get latest set_id
    latest_set = get_highest_set_id()
    new_set_id = latest_set + 1
    new_table_name = f"set_{new_set_id}"

    session = db.get_session()
    try:
        session.execute(
            text(
                "INSERT INTO set_control (hospital_name, address, zip, date_of_set, set_id) VALUES (:hospital_name, :address, :zip, :date_of_set, :set_id)"),
            {
                "hospital_name": hospital_name,
                "address": address,
                "zip": zip_code,
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
            print("'set_control' table does not exist. Creating it...")

            metadata = MetaData()
            Table(
                "set_control", metadata,
                Column("set_id", Integer, primary_key=True),
                Column("hospital_name", String(255)),
                Column("address", String(255)),
                Column("zip", Integer),
                Column("date_of_set", String(100))
            )
            metadata.create_all(db.engine)
            print("'set_control' table created successfully.")

            # Retry insertion
            try:
                session.execute(
                    text(
                        "INSERT INTO set_control (hospital_name, address, zip, date_of_set, set_id) VALUES (:hospital_name, :address, :zip, :date_of_set, :set_id)"),
                    {
                        "hospital_name": hospital_name,
                        "address": address,
                        "zip": zip_code,
                        "date_of_set": date_of_set,
                        "set_id": new_set_id
                    }
                )
                session.commit()
                print(f"Retried and successfully inserted into set_control for Set ID {new_set_id}")

            except Exception as inner_e:
                session.rollback()
                print(f"Retry failed: {inner_e}")
                return

        else:
            print("'set_control' table exists. The error may be due to another issue.")
            return

    finally:
        db.close_session(session)

    metadata = MetaData()
    pricing_table = Table(
        new_table_name, metadata,
        Column("item_id", Integer, primary_key=True, autoincrement=True),
        Column("description", String(255)),
        Column("price", Float),
        Column("code1", String(50)),
        Column("code1_type", String(50)),
        Column("code2", String(50)),
        Column("code2_type", String(50)),
        Column("code3", String(50)),
        Column("code3_type", String(50))
    )

    metadata.create_all(db.engine)
    print(f"Created new table: {new_table_name}")

    session = db.get_session()
    try:
        # The third row contains headers, and data starts from the fourth row (index 3)
        # Column names
        headers = rows[2]
        # Actual pricing data
        data_rows = rows[3:]

        # Map CSV column indexes to known fields
        description_idx = headers.index("description")
        price_idx = headers.index("standard_charge|gross") if "standard_charge|gross" in headers else None
        code1_idx = headers.index("code|1") if "code|1" in headers else None
        code1_type_idx = headers.index("code|1|type") if "code|1|type" in headers else None
        code2_idx = headers.index("code|2") if "code|2" in headers else None
        code2_type_idx = headers.index("code|2|type") if "code|2|type" in headers else None
        code3_idx = headers.index("code|3") if "code|3" in headers else None
        code3_type_idx = headers.index("code|3|type") if "code|3|type" in headers else None

        for row in data_rows:
            session.execute(
                text(f"INSERT INTO {new_table_name} (description, price, code1, code1_type, code2, code2_type, code3, code3_type) VALUES (:description, :price, :code1, :code1_type, :code2, :code2_type, :code3, :code3_type)"),
                {
                    "description": row[description_idx] if description_idx is not None else "",
                    "price": float(row[price_idx]) if price_idx is not None and row[price_idx] else None,
                    "code1": row[code1_idx] if code1_idx is not None else "",
                    "code1_type": row[code1_type_idx] if code1_type_idx is not None else "",
                    "code2": row[code2_idx] if code2_idx is not None else "",
                    "code2_type": row[code2_type_idx] if code2_type_idx is not None else "",
                    "code3": row[code3_idx] if code3_idx is not None else "",
                    "code3_type": row[code3_type_idx] if code3_type_idx is not None else ""
                }
            )
        session.commit()
        print(f"Inserted {len(data_rows)} items into {new_table_name}")

    except Exception as e:
        session.rollback()
        print(f"Error inserting pricing data: {e}")

    finally:
        db.close_session(session)


# Run the script
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_path = os.path.join(script_dir, "real_data")
    csv_file_path = os.path.join(temp_path, "58-0968382_wellstar-cobb-hospital_standardcharges.csv")
    load_wellstar_pricing_data(csv_file_path)
