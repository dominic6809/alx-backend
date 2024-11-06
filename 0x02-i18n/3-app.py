#!/usr/bin/env python3
"""
Basic Flask application setup with Babel integration.
This module contains a basic Flask app with Babel setup for language
localization and timezone configuration.
"""

from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    """Configuration class for language and timezone settings."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Determine the best match for supported languages."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """Render the welcome message."""
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
