def check_novelty(user_price, match_dict):

    print("NOVELTY FOUND!!!!!")
    if not match_dict:
        return {
            "Status": "DNF",
            "CorrectPrice": 0
        }

    prices = list(match_dict.values())
    avg_price = sum(prices) / len(prices)

    print (f"avg_price = {avg_price}")
    try:
        user_price = float(user_price)
    except (ValueError, TypeError):
        # Invalid user price
        return None

    if user_price > avg_price:
        return {
            "Status": "OverBill",
            "CorrectPrice": round(avg_price, 2)
        }
    elif user_price < avg_price:
        return {
            "Status": "UnderBill",
            "CorrectPrice": round(avg_price, 2)
        }
    else:
        # EXACT MATCH
        return None
