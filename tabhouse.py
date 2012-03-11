#!/usr/bin/env python
"""\
Tabhouse

A site to find quality guitar tabs.
"""

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
    print
    print '  >', q
    song_url, song_text, song_source = search_song(q, depth, show_source)
    if not song_url:
        print '  - No song found'
    print
    return jsonify(song_url=song_url, song_text=song_text, song_source=song_source)


# Error handlers
@app.errorhandler(404)
def page_not_found(error=None):
    # TODO: Log broken link
    print
    print '***ERROR*** 404:', request.url
    print '  -> (referrer):', request.referrer
    print
    return render_template('error404.html'), 404


@app.errorhandler(500)
def internal_error(error=None):
    # TODO: Log the error
    print
    print '***ERROR*** 500:', error
    print
    return render_template('error500.html'), 500


# Run development server
if __name__ == '__main__':
    app.run(app.config['HOST'], app.config['PORT'], app.debug != False)
