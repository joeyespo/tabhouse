#!/usr/bin/env python
"""\
TabHouse

A site to find quality guitar tabs.
"""

from flask import Flask, render_template

__version__ = '0.1'


# Flask application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('default_config')
app.config.from_pyfile('local_config.py', silent=True)


# Views
@app.route('/')
def index():
    return render_template('index.html')


# Run development server
if __name__ == '__main__':
    app.run(app.config['HOST'], app.config['PORT'], app.debug != False)
