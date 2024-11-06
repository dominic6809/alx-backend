#!/usr/bin/env python3
"""
Flask application module with Babel configuration.
This module sets up a Flask web application with internationalization
support using Flask-Babel.
"""
from flask import Flask, render_template
from flask_babel import Babel
from typing import Any


class Config:
    """
    Configuration class for Flask application.
    Defines language and timezone settings for the application.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/', strict_slashes=False)
def index() -> Any:
    """
    Handle the root route of the application.
    Returns:
        str: Rendered HTML template with welcome message
    """
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
