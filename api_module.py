from flask import Blueprint, g, request, render_template, abort, jsonify, current_app
from db import create_db, execute_sql, upgrade_db, get_db_version, has_db_update
from services import MovieManager, AssetManager

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/rescan', methods = ['GET', 'POST'])
def rescan():
    mode = request.args.get('mode')
    movies_path = current_app.config['MOVIES_PATH']
    movie_file_exts = current_app.config['DEFAULT_MOVIE_FILE_EXTENSIONS']
    movie_share_path = current_app.config['MOVIE_SHARE_PATH']
    MovieManager().rescan(movies_path, movie_share_path, movie_file_exts, True, mode=='force')
    return jsonify(error='', data='ok')

@api.route('/create_db', methods = ['GET', 'POST'])
def init_db():
    result = dict(error='', result='ok')
    create_db()
    return jsonify(result)

@api.route('/movies', methods = ['GET', 'POST'])
def all_movies():
    keywords = request.args.get('q')
    page_number = 0
    result = dict(error='', result=[])
    try:
        page_number = int(request.args.get('p'))
    except: pass
    if not keywords:
        result = MovieManager().get_all_movies(page_number=page_number)
    else:
        result = MovieManager().search(keywords, page_number=page_number)
    result['error'] = ''
    return jsonify(result)

@api.route('/get_db_version', methods = ['GET', 'POST'])
def get_database_version():
    result = dict(error='', result='Current database version is ' + str(get_db_version()))
    return jsonify(result)

@api.route('/upgrade_db', methods = ['GET', 'POST'])
def upgrade_database():
    result = dict(error='', result='No db update.')
    if not has_db_update():
        return jsonify(result)
    old_version = get_db_version()
    new_version = upgrade_db()
    result['result'] = 'Successfully upgraded database from version {0} to {1}.'.format(old_version, new_version)
    return jsonify(result)
