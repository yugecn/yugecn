import os, sys
sys.path.append(os.curdir)
from pelicanconf import *
SITEURL = os.environ.get("SITEURL", "https://yugecn.github.io")
RELATIVE_URLS = False
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"
DELETE_OUTPUT_DIRECTORY = True
SEARCH_ENABLED = True
from urllib.parse import urlparse
SEARCH_BASE = (urlparse(SITEURL).path.rstrip("/") or "") + "/"
