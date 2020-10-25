from flask import *
from werkzeug.security import check_password_hash

from adapters import *
from adapters.repo import *
from adapters import repo
from movies.model import *
from movies import *
import sys

sys.path.append('../')
from app import *

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
    for i in range(len(user.watched_movies)):
        if user.watched_movies[i].title == movie_title:
            user._time_spent_watching_movies_minutes-=user.watched_movies[i].runtime_minutes
            del user.watched_movies[i]
    return redirect(url_for('watchlist_bp.watchlist'))
