from flask import request, jsonify

from API.Codebase.Data.process import process

def process_request():
    try:
        print("\n--- Incoming Request ---")
        print(f"Headers: {dict(request.headers)}")
        print(f"Raw Data: {request.data}")
        print(f"JSON: {request.get_json(silent=True)}")  # Avoids exception if JSON is invalid
        print("------------------------\n")

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        # Call process()
        processed_data = process(data)
        return jsonify(processed_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
