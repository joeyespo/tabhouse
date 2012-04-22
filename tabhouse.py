#!/usr/bin/env python
"""\
Tabhouse

A site to find quality guitar tabs.
"""

from logging import error, info
from logging.config import dictConfig
from urllib import urlencode
from flask import Flask, request, render_template, redirect, url_for, jsonify
from search import search_song
from helper import try_parse_int, add_jinja_helpers, email_errors

__version__ = '0.1'


# Flask application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('default_config')
app.config.from_pyfile('local_config.py', silent=True)
app.config.from_envvar('SETTINGS_MODULE', silent=True)
if __name__ == '__main__':
    app.config.from_pyfile('dev_config.py', silent=True)
add_jinja_helpers(app)
if 'LOGGING' in app.config:
    dictConfig(app.config['LOGGING'])
email_errors(app)


# Views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    q = request.args.get('q')
    if not q:
        return redirect(url_for('index'))
    depth = try_parse_int(request.args.get('depth'))
    show_source = bool(request.args.get('source'))
    return render_template('search.html', depth=depth, source=show_source, query=q.title(), raw_query=q, encoded_query=urlencode({'q': q + ' guitar tab'}))


@app.route('/search.json')
def search_json():
    q = request.args.get('q', '')
    depth = try_parse_int(request.args.get('depth'))
    show_source = bool(request.args.get('source'))
    info('  > %s', q)
    song_url, song_text, song_source = search_song(q, depth, show_source)
    if not song_url:
        info('  - No song found for: %s', q)
    info('')
    return jsonify(song_url=song_url, song_text=song_text, song_source=song_source)


# Error handlers
@app.errorhandler(404)
def page_not_found(exception=None):
    error('\n***ERROR*** 404: %s\n  -> (referrer): %s\n', request.url, request.referrer)
    return render_template('error404.html'), 404


@app.errorhandler(500)
def internal_error(exception=None):
    error('\n***ERROR*** 500: %s: %s\n  -> (referrer): %s\n', type(exception).__name__, exception, request.referrer)
    return render_template('error500.html'), 500


# Run development server
if __name__ == '__main__':
    app.run(app.config['HOST'], app.config['PORT'], app.debug != False)
