import os
from flask import Flask, Blueprint, current_app, request, make_response, render_template, url_for, send_from_directory
from core import cached, templated
from services import MovieManager, AssetManager

movie_view = Blueprint('movies', __name__, template_folder='templates')

@movie_view.route('/')
# @cached(60)
@templated('movies.html')
def home():
    keywords = request.args.get('q')
    page_number = 0
    movies = dict()
    try:
        page_number = int(request.args.get('p'))
    except: pass
    if not page_number:
        page_number = 0
    if not keywords:
        movies = MovieManager().get_all_movies(page_number=page_number)
    else:
        movies = MovieManager().search(keywords=keywords, page_number=page_number)
    return dict(movies=movies)