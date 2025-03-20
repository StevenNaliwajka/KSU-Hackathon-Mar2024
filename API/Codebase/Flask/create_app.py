from flask import Flask

from API.Codebase.Data.process_request import process_request


def create_app():
    # create
    app = Flask(__name__)

    @app.route("/process", methods=["POST"])
    def process_json():
        return process_request()

    return app


