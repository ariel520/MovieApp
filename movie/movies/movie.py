from flask import *
from werkzeug.security import check_password_hash

from adapters import *
from adapters.repo import *
from adapters import repo
from movies.model import *
import sys

sys.path.append('../')
from app import *

movie_bp = Blueprint(
    'movie_bp', __name__)


@movie_bp.route('/movies<genre>', methods=['GET', 'POST'])
def movies(genre):
    user = None
    username=session.get('username')
    for u in repo.repo_instance._users:
        if u.username == username:
            user = u
    movies = repo.repo_instance._movies
    all_genre = repo.repo_instance._genres
    genre = genre
    if genre!='All':
        for g in all_genre:
            if g.genre_name==genre:
                genre=g
        movies=get_genre_movie(genre)
    return render_template('movies.html', user=user, movies=movies,all_genre=all_genre,genre=genre)

def get_genre_movie(genre):
    movie_list=[]
    for m in repo.repo_instance._movies:
        if genre in m.genres:
            movie_list.append(m)
    return movie_list



@movie_bp.route('/moviedetailID%<movietitle>', methods=['GET', 'POST'])
def movies_detail(movietitle):
    user = None
    username = session.get('username')
    for u in repo.repo_instance._users:
        if u.username == username:
            user = u
    movie = None
    for m in repo.repo_instance._movies:
        if m.title == movietitle:
            movie = m
    if request.method == 'GET':
        reviews=[]
        for r in repo.repo_instance._reviews:
            if r.movie==movie:
                reviews.append(r)
        return render_template('movieDetail.html', user=user, movie=movie,reviews=reviews)
    elif request.method == 'POST':
        username = session.get('username')
        user = None
        for u in repo.repo_instance._users:
            if u.username == username:
                user = u
        review_text = request.form.get('review')
        rating = int(request.form.get('rating'))
        review = Review(movie, review_text, rating, user)
        repo.repo_instance.add_review(review)
        return redirect(url_for('movie_bp.movies_detail',movietitle=movietitle))
