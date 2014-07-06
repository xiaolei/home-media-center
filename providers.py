# -*- coding: utf-8 -*-

import sys
from urllib2 import Request, urlopen, URLError
from urlparse import urlparse
import json

class HttpClient(object):
    def get(self, url):
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

class MovieInfoProvider(object):
    factory = dict()
    def __init__(self):
        self.factory['www.omdbapi.com'] = OmdbApi()

    def register(self, name, provider_instance):
        if not name:
            raise Exception('name cannot be empty or None')
        if not isinstance(html_parser_instance, HtmlParserBase):
            raise Exception('provider_instance must be an instance of the sub class of MovieInfoProviderBase')
        if not self.factory.has_key(name):
            self.factory[name.lower()] = provider_instance

    def resolve_provider(self, url):
        if not url:
            raise Exception('url cannot be empty or None')
        link = urlparse(url)
        for key in self.factory.keys():
            if key in link.hostname.lower():
                return self.factory[key]
        return None

    def get(self, url):
        provider = self.resolve_provider(url)
        return provider.get(url) if provider != None else dict()

    def get_by_imdb_id(self, imdb_id):
        if not imdb_id:
            return dict()
        url = 'http://www.omdbapi.com/?i={0}'.format(imdb_id)
        return self.get(url)
        
      
class MovieInfoProviderBase(object):
    def get(self, url):
        response_json = HttpClient().get(url)['result']
        result = json.loads(response_json) if response_json else dict()
        return self.transform(result)

    def transform(self, raw_result=dict()):
        return raw_result

class OmdbApi(MovieInfoProviderBase):
    def transform(self, raw_result=dict()):
        result = dict()
        result['name'] = raw_result['Title']
        result['storylines'] = raw_result['Plot']
        result['imdb_id'] = raw_result['imdbID']
        result['poster_url'] = raw_result['Poster']
        result['runtime'] = raw_result['Runtime'].split(' ')[0]
        result['awards'] = raw_result['Awards']
        result['genre'] = raw_result['Genre']
        result['actors'] = raw_result['Actors']
        result['director'] = raw_result['Director']
        result['writers'] = raw_result['Writer']
        result['country'] = raw_result['Country']
        result['language'] = raw_result['Language']
        result['year'] = raw_result['Year']
        try:
            result['imdb_votes'] = int(raw_result['imdbVotes'].replace(',',''))
            result['imdb_rating'] = float(raw_result['imdbRating'])
            result['imdb_metascore'] = float(raw_result['Metascore'])
        except: pass
        return result


if __name__ == '__main__':
    url = 'http://www.omdbapi.com/?i=tt0371746'
    print(MovieInfoProvider().get(url))
