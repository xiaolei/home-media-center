from flask import Blueprint, g, request, render_template, abort, jsonify, current_app
from db import create_db, execute_sql
from services import MovieManager, AssetManager

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/rescan', methods = ['GET', 'POST'])
def rescan():
    movies_path = current_app.config['MOVIES_PATH']
    movie_file_exts = current_app.config['DEFAULT_MOVIE_FILE_EXTENSIONS']
    smb_share_path = current_app.config['SAMBA_SHARE_PATH']
    MovieManager().rescan(movies_path, smb_share_path, movie_file_exts)
    return jsonify(error='', data='ok')

@api.route('/create_db', methods = ['GET', 'POST'])
def init_db():
    result = dict(error='', data='ok')
    create_db()
    return jsonify(result)

@api.route('/movies')
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
