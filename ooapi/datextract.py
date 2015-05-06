'''

Try to find the date from an URL

We have 2 approaches:

 - Do it ourselves. This uses python's dateutil.parser, wrapped
   in some custom code to pull date-like strings out of the full
   text of the page
 - Use IBM's Alchemy API. This possibly works better, but the
   tier is limited to 1000 requests per day. We could get more
   at a cost of .35 cents per URL
'''


from dateutil import parser
import re
import requests
from django.conf import settings


def date_from_html(html):
    '''
    Try to find dates within a text
    dateutil.parser is moderately good at interpreting dates
    but relatively bad at finding them amid all the clutter
    so we go thorough looking forw
    '''
    pass
    html_lower = html.lower()
    for pattern in anchors():
        match = re.search(pattern, html_lower)
        if not match:
            continue
        start = max(0, match.start()-7)
        context = html[start:match.end()+7]
        try:
            return parser.parse(context, fuzzy=True)
        except ValueError:
            continue
        

def date_from_url_internal(url):
    # just for testing
    import six
    html = str(six.moves.urllib.request.urlopen(url).read())
    return date_from_html(html)

def date_from_url_alchemy(article_url):
    api_url = 'http://access.alchemyapi.com/calls/url/URLGetPubDate'
    params = {
        'url': article_url,
        'apikey': settings.ALCHEMY_API_KEY,
        'outputMode': 'json'}
    response = requests.get(api_url, params=params)
    js = response.json()
    rawdate = js['publicationDate']['date']
    if not rawdate:
        return None
    return parser.parse(rawdate)

def anchors():
    '''
    try to find par
    '''
    month = "(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
    numbers = '\d{1,6}'
    whitespace = '\W{0,5}'
    patterns = (
        # 27 january 2015, 27 jan 2015
        ''.join([numbers,whitespace,month,whitespace,numbers]),
        # july 27, 2015
        ''.join([month,whitespace,numbers,whitespace,numbers]),
        # jan 2015
        ''.join([month,whitespace,numbers]),
        # 2015-01-27
        '\d{4}-\d{1,2}-\d{1,2}',
        # 1/27/2015
        '\d{1,2}/\d{1,2}/\d{1,4}',
        # the whole string (and let dateutil work out the rest)
        '.*',
        # 27 jan
        '\d+\W*%s' % month,
        # 2015
        '\d{4}',
    )
    return patterns

