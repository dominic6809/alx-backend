#!/usr/bin/env python3
"""
Flask application module with Babel configuration and user handling.
This module sets up a Flask web application with internationalization
support using Flask-Babel and mock user authentication.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext
from typing import Any, Union, Dict


class Config:
    """
    Configuration class for Flask application.
    Defines language and timezone settings for the application.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


def get_user() -> Union[Dict, None]:
    """
    Get user dictionary based on login_as URL parameter.
    Returns:
        Union[Dict, None]: User dictionary if found, None otherwise
    """
    login_id = request.args.get('login_as')
    if login_id:
        try:
            return users.get(int(login_id))
        except ValueError:
            return None
    return None


@app.before_request
def before_request() -> None:
    """
    Execute before all other functions.
    Sets the logged in user (if any) in flask.g.user
    """
    g.user = get_user()


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
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
