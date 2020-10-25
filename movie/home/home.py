import flask
from flask import Blueprint
from movie.adapters import *
from movie.adapters.repo import *
from movie.adapters import repo
from movie.app import *

home_bp = Blueprint(
    'home_bp', __name__)

@home_bp.route('/')
def index():
    user = None
    username = session.get('username')
    for u in repo.repo_instance._users:
        if u.username == username:
            user = u
    return render_template('index.html', user=user)

