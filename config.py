import os
from common import get_local_ip

class DefaultConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'
    SESSION_COOKIE_SECURE = True
    DATABASE_URI = os.path.join(os.path.dirname(__file__), 'hmc.sqlite')
	# smb://[[[domain;]user[:password@]]server[/share[/path[/file]]]]
    SAMBA_SHARE_PATH = 'smb://{0}/hmc/movie'.format(get_local_ip())
    MOVIES_PATH = os.path.join(os.path.dirname(__file__), 'test-assets/movies')
    DEFAULT_MOVIE_FILE_EXTENSIONS = ('.mkv', '.rmvb', '.rm', '.mp4', '.avi')
	
class Production(DefaultConfig):
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.path.join(os.path.dirname(__file__), 'hmc.sqlite')
    MOVIES_PATH = os.path.join(os.path.dirname(__file__), 'test-assets/movies')
    DEFAULT_MOVIE_FILE_EXTENSIONS = ('.mkv', '.rmvb', '.rm', '.mp4', '.avi')

class Development(DefaultConfig):
    DEBUG = True
    MOVIES_PATH = '/media/elements_/public/movie'
    DEFAULT_MOVIE_FILE_EXTENSIONS = ('.mkv', '.rmvb', '.rm', '.mp4', '.avi')

class Testing(DefaultConfig):
    TESTING = True
    DATABASE_URI = os.path.join(os.path.dirname(__file__), 'hmc-test.sqlite')
    MOVIES_PATH = os.path.join(os.path.dirname(__file__), 'test-assets/movies')
    DEFAULT_MOVIE_FILE_EXTENSIONS = ('.txt', '.mkv', '.rmvb', '.rm', '.mp4', '.avi')
