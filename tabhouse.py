#!/usr/bin/env python
"""\
Tabhouse

A site to find quality guitar tabs.
"""

from flask import Flask, render_template, request

__version__ = '0.1'


# Flask application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('default_config')
app.config.from_pyfile('local_config.py', silent=True)


# Views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    query_string = request.args.get('q')
    # TODO: implement
    url = ''
    song_text = ''
    song_source = ''
    return render_template('search.html', query_string=query_string, url=url, song_text=song_text, song_source=song_source)


# Error handlers
@app.errorhandler(404)
def page_not_found(error=None):
    # TODO: Log broken link
    print '\n404: %s\n  -> %s\n' % (request.url, request.referrer)
    return render_template('error404.html'), 404


@app.errorhandler(500)
def internal_error(error=None):
    # TODO: Log the error
    return render_template('error500.html'), 500


# Run development server
if __name__ == '__main__':
    app.run(app.config['HOST'], app.config['PORT'], app.debug != False)
