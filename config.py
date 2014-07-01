import os

class DefaultConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'
    SESSION_COOKIE_SECURE = True
    DATABASE_URI = os.path.join(os.path.dirname(__file__), 'hmc.sqlite')
	# smb://[[[domain;]user[:password@]]server[/share[/path[/file]]]]
    SAMBA_SHARE_PATH = 'smb://192.168.1.104/hmc'
    MOVIES_PATH = 'D:/v-lexia/labs/python-projects/hmc'
    DEFAULT_MOVIE_FILE_EXTENSIONS = ('.html', '.mkv', '.rmvb', '.rm', '.mp4', '.avi')
	
class Production(DefaultConfig):
    DATABASE_URI = os.path.join(os.path.dirname(__file__), 'hmc.sqlite')

class Development(DefaultConfig):
    DEBUG = True

class Testing(DefaultConfig):
    TESTING = True