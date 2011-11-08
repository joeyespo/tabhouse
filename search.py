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


def re_search(url):
    search_results = read_url(url)
    results = json.loads(search_results)
    data = results['responseData']
    hits = data['results']
    results = [hit['url'] for hit in hits]
    more_url = data['cursor']['moreResultsUrl']
    return results, more_url


def web_search(q, result_count = 4):
    # TODO: User IP, see http://code.google.com/apis/websearch/docs/
    # TODO: Use direct page parsing (from client?) and fall back to the API version
    next_url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % urlencode({'q': q})
    return re_search(next_url)[0]
    # TODO: Get all results
    results = []
    while len(results) < result_count:
        results_part, next_url = re_search(next_url)
        if not results_part:
            break
        results.append(results_part)    # TODO: min(result_count, a)
    return results


def search_song(q, result_count = 4):
    results = web_search(q + ' guitar tab', result_count)
    if not results:
        return None
    # TODO: load result pages and parse songs
    return results[0], '\n'.join(results), ''
