import os
import sys

from API.Codebase.Flask.create_app import create_app

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)