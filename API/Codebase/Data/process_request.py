import traceback
from flask import request, jsonify
from API.Codebase.Data.process import process

def process_request():
    try:
        print("\n--- Incoming Request ---")
        print(f"Headers: {dict(request.headers)}")
        print(f"Raw Data: {request.data}")
        print(f"JSON (silent): {request.get_json(silent=True)}")
        print("------------------------\n")

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        processed_data = process(data)
        return jsonify(processed_data), 200

    except Exception as e:
        print("\n--- Exception Occurred ---")
        traceback.print_exc()  # <---- logs the actual error with file, line, and message
        print("---------------------------\n")
        return jsonify({"error": str(e)}), 500
