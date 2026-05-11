# app.py
import warnings;
from flask import Flask, render_template;
from config import Config;
from helpers import log_request;
from urllib3.exceptions import NotOpenSSLWarning;

# Create a Flask application instance and configure it using the Config class
warnings.filterwarnings("ignore", category=NotOpenSSLWarning);
app = Flask(__name__);
app.config.from_object(Config);
app.json.sort_keys = app.config.get("JSON_SORT_KEYS");
app.json.ensure_ascii = app.config.get("JSON_AS_ASCII");
app.secret_key = app.config.get("SECRET_KEY");


# Import and register the views blueprint
from routes import views_bp, api_bp;
from language import lang_bp;

# Register the blueprint with the Flask application
app.register_blueprint(lang_bp);
app.register_blueprint(views_bp);
app.register_blueprint(api_bp);

# Request Interceptor & Logging Middleware
@app.before_request
def start_logging():
    log_request();
    
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(
        host="0.0.0.0",
        port = app.config.get("PORT"),
        debug = app.config.get("DEBUG")
    );