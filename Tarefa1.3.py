#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from urlparse import urljoin
import helper

pages = helper.get_all_country_pages()
print(pages)	
