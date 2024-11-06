# 0x02-i18n
## Flask Internationalization (i18n) Project

## Overview
This project implements a Flask web application that supports multiple languages and timezones. It includes features like user login simulation, language and timezone selection, and displaying the current time based on the user's preferences.

## Key Features
- **Localization**: Supports English and French using Flask-Babel.
- **Timezone Handling**: Automatically adjusts the displayed time based on the user's timezone.
- **User Simulation**: Mock user login using URL parameters, with different locales and timezones.
- **Translation Files**: PO files for English and French translations.
- **Time Display**: Displays current time in the user's timezone.

## Installation
1. Install dependencies:
   ```bash
   pip3 install flask flask_babel pytz

## Set up translations
    pybabel extract -F babel.cfg -o messages.pot .
    pybabel init -i messages.pot -d translations -l en
    pybabel init -i messages.pot -d translations -l fr
    pybabel compile -d translations

## License

### Key Points:
- The README covers the basic functionality of the application.
- It includes setup instructions, usage, and configuration details.
- It summarizes the main objectives (localization, timezone handling, and user simulation) in a concise manner.

