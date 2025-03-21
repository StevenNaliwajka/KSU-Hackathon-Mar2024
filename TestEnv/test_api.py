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
                "ID": "0417T",
                "Description": "HC PROGRAMMING DEVICE EVALUATION CARDIAC MODULATION SYSTEM",
                "Price": 300
            },
            {
                "ID": "34010067",
                "Description": "HC I-131 SERUM ALBUMIN DX PER 5 UCI DOSE",
                "Price": 355.8
            },
            {
                "ID": "20010042",
                "Description": "HC CLOSED TX NASAL BONE FX W/MNPJ W/O STABILIZATION",
                "Price": 22000.40
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
