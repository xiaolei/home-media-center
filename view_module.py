import os
from flask import Flask, Blueprint, current_app, request, make_response, render_template, url_for, send_from_directory
from core import cached, templated
from services import MovieManager, AssetManager

view = Blueprint('view', __name__, template_folder='templates')

@view.route('/favicon.ico')
@cached(60*60*24)
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@view.route('/')
@templated('home.html')
def home(): pass

@view.route('/admin')
@templated('admin.html')
def admin(): pass