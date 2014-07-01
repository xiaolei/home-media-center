﻿# -*- coding: utf-8 -*-

import sys
from urllib2 import Request, urlopen, URLError
from pyquery import PyQuery
from urlparse import urlparse

class WebCrawler(object):
    def execute(self, url):
        error = ''
        html = ''
        request = Request(url)
        try:
            response = urlopen(request)
        except URLError as e:
            error = 'sorry, error occurred. please try again later.'
            if hasattr(e, 'reason'):
                error = e.reason
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            html = response.read();
        return dict(error=error, result = html)

class HtmlParserFactory(object):
    factory = dict()
    def __init__(self):
        self.factory['douban'] = DoubanHtmlParser()
        self.factory['imdb'] = ImdbHtmlParser()

    def register(self, name, html_parser_instance):
        if not name:
            raise Exception('name cannot be empty or None')
        if not isinstance(html_parser_instance, HtmlParserBase):
            raise Exception('html_parser_instance must be an instance of the sub class of HtmlParserBase')
        if not self.factory.has_key(name):
            self.factory[name.lower()] = html_parser_instance

    def get_parser(self, url):
        if not url:
            raise Exception('url cannot be empty or None')
        link = urlparse(url)
        for key in self.factory.keys():
            if key in link.hostname.lower():
                return self.factory[key]
        return None
      
class HtmlParserBase(object):
    engine = None
    def load(self, url):
        self.engine = PyQuery(url=url)
        return self

    def select(self, selector):
        return self.engine(selector)

    def selectTitle(self):
        return ''

class DoubanHtmlParser(HtmlParserBase):
    def selectTitle(self):
        return self.select('title').text()

class ImdbHtmlParser(HtmlParserBase):
    def selectTitle(self):
        return self.select('title').text()


if __name__ == '__main__':
    url = 'https://www.douban.com'
    factory = HtmlParserFactory()
    parser = factory.get_parser(url)
    print(parser.load(url).selectTitle())