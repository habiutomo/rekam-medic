"""
Main module for Electronic Medical Records (EMR) system.
Import app from app module to ensure Flask app is configured correctly.
"""
from app import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")