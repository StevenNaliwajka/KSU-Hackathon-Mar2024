from flask import request, jsonify

from API.Codebase.Data.process import process


def process_request():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        # Call process()
        processed_data = process(data)

        return jsonify(processed_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500