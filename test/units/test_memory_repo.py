import pytest

from watchlist.watchlist import *
from adapters import repo
from user import *



test_repo = MemoryRepo()

def test_load_data():
    csv = MovieFileCSVReader('testMovies.csv')
    csv.read_csv_file()
    test_repo._movies = csv.dataset_of_movies
    test_repo._actors = csv.dataset_of_actors
    test_repo._genres = csv.dataset_of_genres
    test_repo._directors = csv.dataset_of_directors

    assert len(test_repo._movies) == 5


if __name__ == '__main__':
    pytest.main("-s test_memory_repo.py")
