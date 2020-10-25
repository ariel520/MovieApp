from flask import *
from werkzeug.security import check_password_hash

from movie.adapters import *
from movie.adapters.repo import *
from movie.adapters import repo
from movie.movies.model import *
from movie.movies import *
import sys

sys.path.append('../')
from movie.app import *

watchlist_bp = Blueprint(
    'watchlist_bp', __name__)


@watchlist_bp.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    user = repo.repo_instance.get_user(session.get("username"))
    watchlist = user.watched_movies
    return render_template('watchlist.html', user=user, watchlist=watchlist)


@watchlist_bp.route('/add_to_watchlist%<title>')
def add_to_watch_list(title):
    movie = None
    username = session.get('username')
    for m in repo.repo_instance._movies:
        if m.title == title:
            movie = m
    repo.repo_instance.add_watch_movie(username, movie)

    return redirect(url_for("movie_bp.movies", genre='All'))


@watchlist_bp.route('/add_to_watchlistreturndetail%<title>')
def add_to_watch_list_return_detail(title):
    movie = None
    username = session.get('username')
    for m in repo.repo_instance._movies:
        if m.title == title:
            movie = m
    repo.repo_instance.add_watch_movie(username, movie)

    return redirect(url_for("movie_bp.movies_detail", movietitle=title))


@watchlist_bp.route('/deletemoviefromlist<movie_title>')
def delete_movie_from_list(movie_title):
    user = repo.repo_instance.get_user(session.get("username"))
    for m in user.watched_movies:
        if m.title == movie_title:
            user.watched_movies.remove(m)
            user._time_spent_watching_movies_minutes -= m.runtime_minutes
    return redirect(url_for('watchlist_bp.watchlist'))
