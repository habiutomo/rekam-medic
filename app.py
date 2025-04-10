import os
import logging
from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Define base model class
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Template filter for formatting dates
@app.template_filter('format_date')
def format_date(value, format='%Y-%m-%d'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

# Home page route
@app.route("/")
def index():
    return render_template("index.html")

# Handle errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error='Internal server error'), 500

with app.app_context():
    # Import models to ensure they are registered with SQLAlchemy
    import models

    # Create database tables
    db.create_all()
    
    # Import and register blueprints
    from routes.auth import auth
    from routes.patients import patients
    from routes.appointments import appointments
    from routes.clinical import clinical
    from routes.prescriptions import prescriptions
    from routes.laboratory import laboratory
    from routes.billing import billing
    from routes.reports import reports
    from routes.documents import documents
    
    app.register_blueprint(auth)
    app.register_blueprint(patients)
    app.register_blueprint(appointments)
    app.register_blueprint(clinical)
    app.register_blueprint(prescriptions)
    app.register_blueprint(laboratory)
    app.register_blueprint(billing)
    app.register_blueprint(reports)
    app.register_blueprint(documents)

    # Configure login manager
    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
