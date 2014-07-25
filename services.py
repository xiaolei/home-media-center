import os, os.path, fnmatch, json, urllib
from db import query_db, execute_sql
from providers import MovieInfoProvider

DEFAULT_PAGE_SIZE = 16
FILE_NAME_NOT_SCAN = '.notscan'

class AssetManager(object):
    def refine_folder_names(self, path, replace_rules=[[' ', '_'], ['[', ''], [']', ''], ['(', ''], [')', '']]):
        if not path or not replace_rules or not os.path.isdir(path): pass
        for dirname in os.listdir(path):
            new_dirname = dirname
            for rule in replace_rules:
                if len(rule) == 2 and rule[0] in dirname:
                    new_dirname = new_dirname.replace(rule[0], rule[1])
            if new_dirname != dirname:
                os.rename(os.path.join(path, dirname), os.path.join(path, new_dirname))
                
    def get_files(self, path, movie_share_path, extensions=(), skip_if_notscan_file_exists = True):
        result = []
        length = len(path)
        if movie_share_path[-1:] != '/':
            movie_share_path = movie_share_path + '/'
        for root, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if extensions and not (filename.lower().endswith(extensions)):
                    continue
                abs_file_name = os.path.join(root, filename)

                # Ignor the files if there is a file which name is '.notscan' in the parent folder 
                notscan_file_name = os.path.join(os.path.dirname(abs_file_name), FILE_NAME_NOT_SCAN)
                if skip_if_notscan_file_exists and os.path.isfile(notscan_file_name):
                    continue
                (name, ext) = os.path.splitext(abs_file_name)
                # Try to load the json format movie information from the file with the same file name but extension is .json
                json_file_name = name + '.json'
                json_file_info = dict()
                if os.path.isfile(json_file_name):
                    with open(json_file_name) as f:
                        json_text = f.read()
                        if json_text:
                            json_file_info = json.loads(json_text)
                filename_with_path = abs_file_name.replace(path, '')
                if filename_with_path[0] == os.sep:
                    filename_with_path = movie_share_path + filename_with_path[1:]
                else:
                    filename_with_path = movie_share_path + filename_with_path
                filename_with_path = filename_with_path.replace('\\', '/')
                fileinfo = dict(url=filename_with_path, filename=abs_file_name, info=json_file_info)
                result.append(fileinfo)
        return result
        

class MovieManager(object):
    def rescan(self, movies_path, movie_share_path, movie_file_exts, refine_folder_names = True, force_rescan_all = False):
        result = 0
        if force_rescan_all:
            sql = 'delete from movies;'
            execute_sql(sql)
        else:
            self.remove_all_missing_files_in_db()
        assetManager = AssetManager();
        if refine_folder_names:
            assetManager.refine_folder_names(movies_path)
        files = assetManager.get_files(movies_path, movie_share_path, movie_file_exts, False if force_rescan_all else True)
        for file in files:
            movie = dict()
            filename = file['filename']
            url = file['url']
            movie['name'] = os.path.basename(filename)
            (r, ext) = os.path.splitext(filename)
            poster_filename = r + '.jpg'
            
            if file['info'].has_key('imdb_id'):
                imdb_id = file['info']['imdb_id']
                movie = MovieInfoProvider().get_by_imdb_id(imdb_id)
                if not movie:
                    continue
                # Download poster image to local with the same name as the movie file name.
                if movie.has_key('poster_url'):
                    self.download_poster_file(movie['poster_url'], poster_filename)
                    
            movie['url'] = url
            movie['file_name'] = filename
            movie['poster_url'] = url[:-4] + '.jpg'

            sql = u'insert into movies({0}) values({1});'.format(', '.join(movie.keys()), ('?,'*len(movie.values()))[:-1])
            execute_sql(sql, movie.values())
            result = result + 1
            
            # Create a '.notscan' file to indicates that this file already be scanned. Next time, it will be ignored
            self.create_notscan_file(os.path.dirname(filename))
        return result

    def download_poster_file(self, poster_url, save_to_filename):
        if not poster_url or not save_to_filename or os.path.isfile(save_to_filename):
            pass
        try:
            urllib.urlretrieve(poster_url, save_to_filename)
        except Exception as ex:
            print(str(ex))

    def create_notscan_file(self, folder_path):
        if not folder_path: pass
        notscan_file_name = os.path.join(folder_path, FILE_NAME_NOT_SCAN)
        if not os.path.isfile(notscan_file_name):
            with open(notscan_file_name, 'w'): pass

    def get_all_movies(self, page_size=DEFAULT_PAGE_SIZE, page_number=0):
        if page_size <= 0:
            page_size = DEFAULT_PAGE_SIZE
        if page_number < 0:
            page_number = 0
        sql = u"select * from movies where is_active = 'true' order by ratings desc limit {0} offset {1}".format(page_size, page_number*page_size)
        result = query_db(sql)
        return self.wrap_results(result, page_number, page_size, '')

    def remove_all_missing_files_in_db(self):
        removed_count = 0
        sql = 'delete from movies where _id = ?'
        while True:
            query = self.get_all_movies(20, 0)
            if len(query['result']) == 0:
                break
            movies = query['result']
            for movie in movies:
                file_name = movie['file_name']
                file_id = movie['_id']
                if not os.path.isfile(file_name):
                    execute_sql(sql, [file_id])
                    removed_count = removed_count + 1
        return removed_count

    def get_total_count(self):
        sql = u"select count(_id) as mcount from movies where is_active = 'true'"
        result = query_db(query=sql, one=True)
        return int(result['mcount']) if result else 0

    def search(self, keywords, page_size=DEFAULT_PAGE_SIZE, page_number=0):
        if page_size <= 0:
            page_size = DEFAULT_PAGE_SIZE
        if page_number < 0:
            page_number = 0
        result = []
        sql = u"select * from movies where is_active = 'true' and name like ? or also_known_as like ? or plot_keywords like ? or tags like ? order by ratings desc limit {0} offset {1}".format(page_size, page_number*page_size)
        if keywords:
            result = query_db(sql, ['%' + keywords + '%', '%' + keywords + '%', '%' + keywords + '%', '%' + keywords + '%'])
        return self.wrap_results(result, page_number, page_size, keywords)

    def has_more_results(self, keywords, page_size=DEFAULT_PAGE_SIZE, page_number=0):
        sql = u"select _id from movies where is_active = 'true' limit 1 offset {0}".format((page_number + 1)*page_size)
        args = []
        if keywords:
            sql = u"select _id from movies where is_active = 'true' and name like ? limit 1 offset {0}".format((page_number + 1)*page_size)
            args=['%' + keywords + '%']
        result = query_db(query=sql, args=args, one=True)
        return True if result else False

    def wrap_results(self, result, page_number=0, page_size=DEFAULT_PAGE_SIZE, keywords=''):
        return dict(result=result, has_more = self.has_more_results(keywords, page_size, page_number), page_number=page_number, query=keywords)
