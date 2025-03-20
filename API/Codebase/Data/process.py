def process(data):
    try:
        # get data from json
        pricing_data = data.get("pricingData", {})
        user_data = data.get("userData", {})
        line_items = data.get("lineItems", [])

        # Calc total price
        total_price = sum(item.get("Price", 0) for item in line_items if isinstance(item.get("Price"), (int, float)))

        # generate a structured response
        processed_result = {
            "message": "Received",
            "pricingData": pricing_data,
            "userData": user_data,
            "lineItems": line_items,
            "summary": {
                "total_items": len(line_items),
                "total_price": total_price
            }
        }

        return processed_result

    except Exception as e:
        return {"error": str(e)}