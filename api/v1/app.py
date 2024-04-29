#!/usr/bin/python3
""" Endpoint returns the status of the API"""

from flask import Flask
app = Flask(__name__)

from models import storage
from api.v1.views import app_views
import os

# registering the blueprint
app.register_blueprint(app_views)

# defining the teardown_appcontext function
@app.teardown_appcontext
def close_storage(exception=None):
    """Closes the storage connection when the app context is torn down."""
    storage.close()


if __name__ == "__main__":
    app.run(
        host = os.environ.get("HBNB_API_HOST", "0.0.0.0"),
        port = int(os.environ.get("HBNB_API_PORT", 5000)),
        threaded = True
    )
