"""\
Search.py

Defines functions for searching for guitar tabs using Google.
"""

import json
from urlparse import urlparse
from urllib import urlencode, urlopen
from flask import current_app
from guitar import Song


def read_url_unicode(url):
    response = urlopen(url)
    content_type = response.headers.get('content-type', '')
    try:
        content = response.read()
    finally:
        response.close()
    index = content_type.find('charset=')
    encoding = content_type[index + 8:] if index >= 0 else None
    content = unicode(content, encoding, errors='replace') if encoding else unicode(content, errors='replace')
    return content


def re_search(url):
    data = json.loads(read_url_unicode(url))
    responseData = data[u'responseData']
    if not responseData:
        responseStatus, responseDetails = data[u'responseStatus'], data[u'responseDetails']
        if responseStatus:
            # TODO: Log errors
            print '  *** Error: search responded with %s: %s' % (responseStatus, responseDetails)
        return [], ''
    current_domain = current_app.config.get('DOMAIN', 'localhost')
    any_other_domain = lambda url: not (current_domain in url and urlparse(url).netloc.endswith(current_domain))
    urls = [hit['url'] for hit in responseData['results'] if any_other_domain(hit['url'])]
    return urls, responseData['cursor']['moreResultsUrl']


def web_search(q, result_count=4):
    # TODO: Provide the client IP address for more results, see http://code.google.com/apis/websearch/docs/
    # TODO: Use direct page parsing (from client?) and fall back to the API version
    urls, next_url = re_search('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % urlencode({'q': q}))
    # TODO: Get all results, up to result_count
    return urls[:result_count]


def search_song(q, result_count=4, show_source=False):
    print
    urls = web_search(q + ' guitar tab', result_count)
    if not urls:
        return '', '', ''
    print 'Checking for song:'
    for url in urls:
        print '  - Checking:', url
        try:
            content = read_url_unicode(url)
        except Exception, ex:
            # TODO: Log errors
            print '  *** Error fetching %s: %s' % (url, ex)
            continue
        for text in get_pre_text(content):
            song, errors = Song.parse(text)
            if not song.staffs:
                continue
            print '    Found song!'
            # TODO: Log errors
            if len(errors) > 0:
                print '\n'.join(['  *** Error while parsing song: ' + message for message in errors])
            song_text = str(song)
            song_source = text if show_source or len(song_text.split('\n')) < 20 else ''
            return url, song_text, song_source
    return '', '', ''


# TODO: Clean this up
def get_pre_text(html):
    html_insensitive = html.lower()
    def between(s, beginswith='', endswith='', start=0, end=None):
        end = end or len(s)
        i = s.find(beginswith, start, end) if beginswith else 0
        if i == -1:
            return -1, -1
        i += len(beginswith)
        j = s.find(endswith, i, end) if endswith else len(s)
        return i, j
    preList = []
    j = 0
    while True:
        i, j = between(html_insensitive, '<pre>', '</pre>', j)
        if j == -1:
            break
        preList.append(html[i:j].replace('<br>', '\n').replace('<BR>', '\n'))
        j += 6          # => len('</pre>')
    return preList


def get_best_song(songs):
    # TODO: Use a better heuristic than the minimum error count which has the longest staff
    if len(songs) == 0:
        return None
    maxerrors = 0
    for song in songs:
        maxerrors = min(len(song.Errors), maxerrors)
    size = 0
    index = 0
    for i in range(len(songs)):
        song = songs[i]
        if song.Errors > maxerrors:
            continue
        cursize = len(song.Staffs)
        if cursize >= size:
            size = cursize
            index = i
    return songs[index]
