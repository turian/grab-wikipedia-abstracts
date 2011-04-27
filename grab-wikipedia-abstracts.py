#!/usr/bin/python

BASE_URL = "http://dumps.wikimedia.org/backup-index.html"

import sys
import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup, SoupStrainer
import os

def get_links(url):
    print >> sys.stderr, "Retrieving: %s" % url
    all_urls = []
    try:
        page = urllib2.urlopen(url)
        links = SoupStrainer('a')

        for link in BeautifulSoup(page, parseOnlyThese=links):
            if link.has_key('href'):
                all_urls.append(urlparse.urljoin(BASE_URL, link["href"]))
    except Exception, e:
        print >> sys.stderr, type(e), e
    return all_urls

for url in get_links(BASE_URL):
    for url2 in get_links("http://dumps.wikimedia.org/enwiki/20110405/"):
        if url2.find("abstract.xml") != -1:
            cmd = "wget --mirror %s" % url2
            print >> sys.stderr, cmd
            os.system(cmd)
