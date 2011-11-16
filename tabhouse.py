#!/usr/bin/env python
"""\
Tabhouse

A site to find quality guitar tabs.
"""

from urllib import urlencode
from flask import Flask, render_template, request, redirect, url_for
from search import search_song
from helper import static_for

__version__ = '0.1'


# Flask application
app = Flask(__name__, instance_relative_config=True)
app.jinja_env.globals.update(static_for=static_for)
app.config.from_object('default_config')
app.config.from_pyfile('local_config.py', silent=True)


# Views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    q = request.args.get('q')
    depth = int(request.args.get('depth', 10))
    show_source = bool(request.args.get('source'))
    if not q:
        return redirect(url_for('index'))
    print
    print '>', q
    raw_query = urlencode({'q': q + ' guitar tab'})
    song_url, song_text, song_source = search_song(q, depth, show_source)
    return render_template('search.html', song_url=song_url, query=q.title(), raw_query=raw_query, song_text=song_text, song_source=song_source)


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
