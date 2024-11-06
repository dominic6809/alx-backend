#!/usr/bin/env python3
"""
Flask application module with Babel configuration.
This module sets up a Flask web application with internationalization
support using Flask-Babel.
"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext
from typing import Any, Union


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


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best matching language based on client's preferred languages.
    First checks for locale parameter in URL, then falls back to request headers.
    Returns:
        str: Best matching language code from the supported languages
    """
    # Check if locale parameter is in URL
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    
    # Fall back to default behavior (accept_languages header)
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> Any:
    """
    Handle the root route of the application.
    Returns:
        str: Rendered HTML template with welcome message
    """
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
