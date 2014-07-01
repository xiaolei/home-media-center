import os, fnmatch
from flask import current_app
from db import query_db

DEFAULT_PAGE_SIZE = 4

class AssetManager(object):
    def get_files(self, path, extensions=()):
        result = []
        smb_share_path = current_app.config['SAMBA_SHARE_PATH']
        length = len(path)
        if smb_share_path[-1:] != os.sep:
            smb_share_path = smb_share_path + os.sep
        for root, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if extensions and not (filename.lower().endswith(extensions)):
                    continue
                abs_file_name = os.path.join(root, filename)
                filename_with_path = abs_file_name.replace(path, '')
                if filename_with_path[0] == os.sep:
                    filename_with_path = smb_share_path + filename_with_path[1:]
                else:
                    filename_with_path = smb_share_path + filename_with_path
                filename_with_path = filename_with_path.replace('\\', '/')
                fileinfo = dict(url=filename_with_path, filename=abs_file_name)
                result.append(fileinfo)
        return result
        

class MovieManager(object):
    def get_all_movies(self, page_size=DEFAULT_PAGE_SIZE, page_number=0):
        if page_size <= 0:
            page_size = DEFAULT_PAGE_SIZE
        if page_number < 0:
            page_number = 0
        sql = "select * from movies where is_active = 'true' order by ratings desc limit {0} offset {1}".format(page_size, page_number*page_size)
        result = query_db(sql)
        return self.wrap_results(result, page_number, page_size, '')

    def search(self, keywords, page_size=DEFAULT_PAGE_SIZE, page_number=0):
        if page_size <= 0:
            page_size = DEFAULT_PAGE_SIZE
        if page_number < 0:
            page_number = 0
        result = []
        sql = "select * from movies where is_active = 'true' and name like ? or also_known_as like ? or plot_keywords like ? or tags like ? order by ratings desc limit {0} offset {1}".format(page_size, page_number*page_size)
        if keywords:
            result = query_db(sql, ['%' + keywords + '%', '%' + keywords + '%', '%' + keywords + '%', '%' + keywords + '%'])
        return self.wrap_results(result, page_number, page_size, keywords)

    def has_more_results(self, keywords, page_size=DEFAULT_PAGE_SIZE, page_number=0):
        sql = "select _id from movies where is_active = 'true' limit 1 offset {0}".format((page_number + 1)*page_size)
        args = []
        if keywords:
            sql = "select _id from movies where is_active = 'true' and name like ? limit 1 offset {0}".format((page_number + 1)*page_size)
            args=['%' + keywords + '%']
        result = query_db(query=sql, args=args, one=True)
        return True if result else False

    def wrap_results(self, result, page_number=0, page_size=DEFAULT_PAGE_SIZE, keywords=''):
        return dict(result=result, has_more = self.has_more_results(keywords, page_size, page_number), page_number=page_number, query=keywords)