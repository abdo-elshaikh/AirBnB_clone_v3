#!/usr/bin/python3
"""Main module for the AirBnB clone API."""
from flask import Flask, jsonify
from flask_cors import CORS
from os import environ
from models import storage
from api.v1.views import app_views


# Create a Flask application instance
app = Flask(__name__)

# Create CORS instance and allow /* for 0.0.0.0
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register blueprint app_views to the Flask app instance
app.register_blueprint(app_views)

# Enable strict_slashes=False
app.url_map.strict_slashes = False


# Define a method to handle teardown_appcontext
@app.teardown_appcontext
def close_storage(exception):
    """Close the current SQLAlchemy session."""
    storage.close()


#  create a handler for 404 errors
@app.errorhandler(404)
def nop(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404


# Run the Flask application
if __name__ == "__main__":
    # Set the host and port for the Flask server
    host = environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(environ.get("HBNB_API_PORT", 5000))

    # Run the Flask application
    app.run(host=host, port=port, threaded=True)
