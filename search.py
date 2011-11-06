"""\
Search.py

Defines functions for searching for guitar tabs using Google.
"""

import json
from urllib import urlencode, urlopen


def read_url(url):
    response = urlopen(url)
    try:
        return response.read()
    finally:
        response.close()


def google_search(q, result_count = 4):
    # TODO: Use logging
    search_results = read_url('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % urlencode({'q': q}))
    results = json.loads(search_results)
    data = results['responseData']
    print 'Total results: %s' % data['cursor']['estimatedResultCount']
    hits = data['results']
    print 'Top %d hits:' % len(hits)
    text = ''
    results = []
    for h in hits:
        results.append(h['url'])
    print 'For more results, see %s' % data['cursor']['moreResultsUrl']
    # TODO: Get more URLs, up to result_count
    return results


def search_song(q, result_count = 4):
    results = google_search(q + ' guitar tab', result_count)
    if not results:
        return None
    # TODO: load result pages and parse songs
    return results[0], '\n'.join(results), ''
