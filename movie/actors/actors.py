from flask import *
from werkzeug.security import check_password_hash

from movie.adapters import *
from movie.adapters.repo import *
from movie.adapters import repo
import sys

sys.path.append('../')
from movie.app import *

actor_bp = Blueprint(
    'actor_bp', __name__)


@actor_bp.route('/actors', methods=['GET'])
def actors():
    user = repo.repo_instance.get_user(session.get("username"))
    return render_template('actors.html', user=user, actors=repo.repo_instance._actors)


@actor_bp.route('/actordetailID%<actortitle>', methods=['GET', 'POST'])
def actor_detail(actortitle):
    user = repo.repo_instance.get_user(session.get("username"))
    actor = None
    for a in repo.repo_instance._actors:
        if a.actor_full_name == actortitle:
            actor = a
    play_movies = play(actor)
    if request.method == 'GET':
        reviews = []
        for r in repo.repo_instance._actor_review:
            if r.actor == actor:
                reviews.append(r)
        return render_template('actorDetails.html', user=user, actor=actor, play_movies=play_movies,reviews=reviews)
    elif request.method == 'POST':
        review_text = request.form.get('review')
        rating = int(request.form.get('rating'))
        review = ActorReview(actor, review_text, rating, user)
        repo.repo_instance.add_actor_review(review)
        return redirect(url_for('actor_bp.actor_detail',actortitle=actortitle))


def play(actor):
    play_movies = []
    for m in repo.repo_instance._movies:
        if actor in m.actors:
            play_movies.append(m)
    return play_movies
