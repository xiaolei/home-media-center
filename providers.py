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

    def get_value(self, raw_result, key, default_value=''):
        return raw_result[key] if raw_result and key and raw_result.has_key(key) else default_value

class OmdbApi(MovieInfoProviderBase):
    def transform(self, raw_result=dict()):
        result = dict()
        if raw_result.has_key('Error'):
            print(raw_result['Error'])
            return result
        result['name'] = self.get_value(raw_result, 'Title')
        result['storylines'] = self.get_value(raw_result, 'Plot')
        result['imdb_id'] = self.get_value(raw_result, 'imdbID')
        result['poster_url'] = self.get_value(raw_result, 'Poster')
        result['runtime'] = self.get_value(raw_result, 'Runtime').split(' ')[0]
        result['awards'] = self.get_value(raw_result, 'Awards')
        result['genre'] = self.get_value(raw_result, 'Genre')
        result['actors'] = self.get_value(raw_result, 'Actors')
        result['director'] = self.get_value(raw_result, 'Director')
        result['writers'] = self.get_value(raw_result, 'Writer')
        result['country'] = self.get_value(raw_result, 'Country')
        result['language'] = self.get_value(raw_result, 'Language')
        result['year'] = self.get_value(raw_result, 'Year')
        result['type'] = self.get_value(raw_result, 'Type')
        result['also_known_as'] = ''
        try:
            result['imdb_votes'] = int(self.get_value(raw_result, 'imdbVotes').replace(',',''))
            result['imdb_rating'] = float(self.get_value(raw_result, 'imdbRating'))
            result['imdb_metascore'] = float(self.get_value(raw_result, 'Metascore'))
        except Exception as ex:
            print(str(ex))
        return result


if __name__ == '__main__':
    url = 'http://www.omdbapi.com/?i=tt0371746'
    print(MovieInfoProvider().get(url))
