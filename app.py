from flask import *

from movies.model import MovieFileCSVReader
from user import *
import config
from adapters.repo import *
from movies.movie import *
from actors.actors import *
from adapters import repo
from watchlist.watchlist import *
from directors.directors import *
from movies import movie, model
from user.__init__ import *


app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(user_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(actor_bp)
app.register_blueprint(watchlist_bp)
app.register_blueprint(director_bp)
repo.repo_instance = MemoryRepo()


@app.route('/')
def index():
    user = None
    username = session.get('username')
    for u in repo.repo_instance._users:
        if u.username == username:
            user = u
    return render_template('index.html', user=user)


def init_data():
    csv = MovieFileCSVReader('Data1000Movies.csv')
    csv.read_csv_file()
    repo.repo_instance._movies = csv.dataset_of_movies
    repo.repo_instance._actors = csv.dataset_of_actors
    repo.repo_instance._genres = csv.dataset_of_genres
    repo.repo_instance._directors = csv.dataset_of_directors


init_data()

if __name__ == '__main__':
    app.run()
