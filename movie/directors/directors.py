from flask import *
from werkzeug.security import check_password_hash

from movie.adapters import *
from movie.adapters.repo import *
from movie.adapters import repo
import sys

sys.path.append('../')
from movie.app import *

director_bp = Blueprint(
    'director_bp', __name__)


@director_bp.route('/directors', methods=['GET'])
def directors():
    user = repo.repo_instance.get_user(session.get("username"))
    return render_template('directors.html', user=user, actors=repo.repo_instance._directors)


@director_bp.route('/directordetailID%<directorname>', methods=['GET', 'POST'])
def director_detail(directorname):
    user = repo.repo_instance.get_user(session.get("username"))
    director = None
    for a in repo.repo_instance._directors:
        if a.director_full_name == directorname:
            director = a
    if request.method == 'GET':
        reviews = []
        for r in repo.repo_instance._director_review:
            if r.director == director:
                reviews.append(r)
        play_movies = filmed(director)
        return render_template('directorDetail.html', user=user, director=director, play_movies=play_movies,
                               reviews=reviews)
    elif request.method == 'POST':
        review_text = request.form.get('review')
        rating = int(request.form.get('rating'))
        review = DirectorReview(director, review_text, rating, user)
        repo.repo_instance.add_director_review(review)
        return redirect(url_for('director_bp.director_detail', directorname=directorname))


def filmed(director):
    play_movies = []
    for m in repo.repo_instance._movies:
        if m.director == director:
            play_movies.append(m)
    return play_movies
