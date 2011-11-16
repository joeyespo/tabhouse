"""\
Helper.py

Helper functions for the current Flask web application.
"""

import os
from flask import url_for, current_app


def static_for(filename, endpoint='.static'):
    """Provides the 'static' function that also appends the file's timestamp to the URL, usable in a template."""
    return url_for(endpoint, filename=filename) + '?' + str(int(os.path.getmtime(os.path.join(current_app.static_folder, filename))))
