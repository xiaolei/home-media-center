import os
from flask import Flask, g, Blueprint, render_template, jsonify
from core import cached, templated, request_wants_json
from api_module import api
from view_module import view

app = Flask(__name__)
app.config.from_object('config.Development')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(view)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=error), 404

@app.errorhandler(403)
def page_not_found(error):
    return render_template('error.html', error=error), 403

@app.errorhandler(500)
def page_not_found(error):
    return render_template('error.html', error=error), 500

@app.errorhandler(Exception)
def catch_all_exception(error):
    if request_wants_json():
        return jsonify(dict(error=error, data=[]))
    else:
        raise

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()