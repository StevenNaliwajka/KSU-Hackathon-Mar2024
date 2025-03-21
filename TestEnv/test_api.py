import requests
import json

def test_api():
    # Flask API URL (Replace with your actual server IP or localhost)
    api_url = "http://24.99.20.190:5000/process"

    # Sample JSON payload matching your expected format
    test_payload = {
        "pricingData": {
            "State": "GA",
            "First3LettersOfZip": "301"
        },
        "userData": {
            "google_sub": "103494999324234235234",
            "paypal_customer_id": "cus_JjULafXYZ"
        },
        "lineItems": [
            {
                "ID": 99201,
                "Description": "Focused H/E Straight",
                "Price": 1200
            },
            {
                "ID": 12345,
                "Description": "Example Item",
                "Price": 899.99
            },
            {
                "ID": 99999,
                "Description": "Should Trigger UnderBill",
                "Price": 1
            }
        ]
    }

    # Send POST request
    response = requests.post(api_url, json=test_payload, headers={"Content-Type": "application/json"})

    # Print Response
    if response.status_code == 200:
        print("API Response:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    test_api()
