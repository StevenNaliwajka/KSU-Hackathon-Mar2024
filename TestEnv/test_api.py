import requests
import json

def test_api():
    # Flask API URL (Replace with your actual server IP)
    API_URL = "http://24.99.20.190:5000/process"

    # Sample JSON payload
    test_payload = {
        "pricingData": {"currency": "USD", "tax": 5.5},
        "userData": {"name": "John Doe", "email": "john@example.com"},
        "lineItems": [
            {"item": "Product A", "Price": 100},
            {"item": "Product B", "Price": 50.75},
            {"item": "Product C", "Price": "invalid"},  # Should be ignored
        ]
    }

    # Send POST request
    response = requests.post(API_URL, json=test_payload, headers={"Content-Type": "application/json"})

    # Print Response
    if response.status_code == 200:
        print("API Response:", json.dumps(response.json(), indent=4))
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    test_api()