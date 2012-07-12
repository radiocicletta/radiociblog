#!/bin/env python2.6
# the ubermaster social feeds collectr

from httplib import HTTPConnection



try:
    conn = HTTPConnection("api.discogs.com", 80)
    conn.request("GET", query)
    response = conn.getresponse()
    if response.status == 200:
        lastquery = query
        laststatus = 200
        results = json.loads(response.read())
        logging.debug(results)
        lastdata = results["results"]
        if len(lastdata):
            logging.debug("%s results found" % len(lastdata))
            genres = lastdata[0]["genre"]
            tags = lastdata[0]["style"]
        else:
            tags = []
            genres = []
except Exception as e:
    logging.error(e)
    tags = []
    genres = []
