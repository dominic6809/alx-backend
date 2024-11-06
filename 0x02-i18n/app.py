#!/usr/bin/env python3
"""
Flask application module with Babel configuration and user handling.
This module sets up a Flask web application with internationalization
and timezone support using Flask-Babel and pytz.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext, format_datetime
from typing import Any, Union, Dict
import pytz
from datetime import datetime


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
    Determine the best matching language based on priority:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request header
    4. Default locale
    Returns:
        str: Best matching language code from the supported languages
    """
    # 1. Check if locale parameter is in URL
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # 2. Check user settings
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']

    # 3. Check request header
    header_locale = request.accept_languages.best_match(
    app.config['LANGUAGES']
)
    if header_locale:
        return header_locale

    # 4. Default locale
    return app.config['BABEL_DEFAULT_LOCALE']


def validate_timezone(timezone: str) -> Union[str, None]:
    """
    Validate that a timezone string is valid.
    Args:
        timezone: String representing the timezone
    Returns:
        str: Validated timezone string or None if invalid
    """
    try:
        pytz.timezone(timezone)
        return timezone
    except pytz.exceptions.UnknownTimeZoneError:
        return None


@babel.timezoneselector
def get_timezone() -> str:
    """
    Determine the appropriate timezone based on priority:
    1. Timezone from URL parameters
    2. Timezone from user settings
    3. Default to UTC
    Returns:
        str: Valid timezone string
    """
    # 1. Find timezone parameter in URL parameters
    timezone = request.args.get('timezone')
    if timezone:
        validated_timezone = validate_timezone(timezone)
        if validated_timezone:
            return validated_timezone

    # 2. Find timezone from user settings
    if g.user and g.user.get('timezone'):
        validated_timezone = validate_timezone(g.user['timezone'])
        if validated_timezone:
            return validated_timezone

    # 3. Default to UTC
    return "UTC"


@app.route('/', strict_slashes=False)
def index() -> Any:
    """
    Handle the root route of the application.
    Returns:
        str: Rendered HTML template with welcome message
    """
    # Get the timezone
    timezone = get_timezone()
    # Get current time in the user's timezone
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    # Format the time based on the locale
    formatted_time = format_datetime(current_time)

    return render_template('index.html', current_time=formatted_time)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
