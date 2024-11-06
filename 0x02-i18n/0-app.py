#!/usr/bin/env python3
"""
Basic Flask application module.
This module sets up a simple Flask web application with a single route
that renders a template displaying a welcome message.
"""
from flask import Flask, render_template
from typing import Any

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> Any:
    """
    Handle the root route of the application.
    Returns:
        str: Rendered HTML template with welcome message
    """
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
