from API.Codebase.Billing.check_billing import check_billing
from API.Codebase.Data.check_novelty import check_novelty
from API.Codebase.Data.get_set_list import get_set_list
from API.Codebase.DB.database import Database
from sqlalchemy.sql import text

def process(data):
    try:

        # Parse metadata
        pricing_data = data.get("pricingData", {})

        state = pricing_data.get("State", "")
        zip_prefix = pricing_data.get("First3LettersOfZip", "")

        # Parse user info
        user_data = data.get("userData", {})
        google_sub = user_data.get("google_sub", "")
        paypal_id = user_data.get("paypal_customer_id", "")

        # Check billing
        pricing_status = check_billing(paypal_id)
        if pricing_status == "Bad":
            return {
                "pricingStatus": pricing_status,
                "lineItems": None
            }

        # Parse line items
        line_items_raw = data.get("lineItems", [])

        print("line_items_raw", line_items_raw)

        set_list = get_set_list(zip_prefix)
        # print(f"set_list for zip prefix {zip_prefix}: {set_list}")
        db = Database()
        session = db.get_session()

        notible_line_items = []
        for item in line_items_raw:
            item_id = str(item.get("ID"))

            set_match_list = {}
            for set_id in set_list:
                table_name = f"set_{set_id}"

                try:
                    # SQL to check for ID match in code1/code2/code3
                    query = text(f"""
                        SELECT price FROM {table_name}
                        WHERE code1 = :item_id OR code2 = :item_id OR code3 = :item_id
                        LIMIT 1
                    """)
                    result = session.execute(query, {"item_id": item_id}).fetchone()

                    if result:
                        # Match found: store set_id and price
                        set_match_list[set_id] = result.price

                except Exception as inner_e:
                    print(f"Error querying {table_name}: {inner_e}")

            result = check_novelty(item.get("Price"), set_match_list)

            if result:
                notible_line_items.append({
                    "ID": item.get("ID"),
                    "Description": item.get("Description", ""),
                    "Status": result["Status"],
                    "CorrectPrice": result["CorrectPrice"]
                })


            #print(f"\nProcessing item: {item}")
            #print(f"Collected price matches: {set_match_list}")
            #print(f"User Price: {item.get('Price')} | Match Result: {result}")

        session.close()

        return {
            "pricingStatus": pricing_status,
            "lineItems": notible_line_items
        }

    except Exception as e:
        return {"error": str(e)}
