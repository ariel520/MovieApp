import csv
import os
from datetime import date, datetime
from user.user import *
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash


class MemoryRepo:
    def __init__(self):
        self._users = list()
        self._movies = list()
        self._actors = list()
        self._reviews = list()
        self._genres = list()
        self._directors = list()
        self._actor_review=list()
        self._director_review=list()

    def add_user(self, user: User):
        self._users.append(user)
        print(self._users)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def add_review(self, review):
        self._reviews.append(review)

    def add_actor_review(self,review):
        self._actor_review.append(review)

    def add_director_review(self,review):
        self._director_review.append(review)

    def reset_profile(self, username, new_path):
        for i in range(len(self._users)):
            if self._users[i].username == username:
                self._users[i]._profile_pic = new_path

    def add_watch_movie(self, username, movie):
        for i in range(len(self._users)):
            if self._users[i].username == username:
                self._users[i].watch_movie(movie)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


repo_instance = None

# def load_users(repo):
#     users = dict()
#
#     for data_row in read_csv_file(os.path.join('users.csv')):
#         user = User(
#             username=data_row[1],
#             password=generate_password_hash(data_row[2])
#         )
#         repo.add_user(user)
#         users[data_row[0]] = user
#     return users
#
#
# def load_comments(data_path: str, repo: MemoryRepository, users):
#     for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
#         comment = make_comment(
#             comment_text=data_row[3],
#             user=users[data_row[1]],
#             article=repo.get_article(int(data_row[2])),
#             timestamp=datetime.fromisoformat(data_row[4])
#         )
#         repo.add_comment(comment)
#
#
# def populate(data_path: str, repo: MemoryRepository):
#     # Load articles and tags into the repository.
#     load_articles_and_tags(data_path, repo)
#
#     # Load users into the repository.
#     users = load_users(data_path, repo)
#
#     # Load comments into the repository.
#     load_comments(data_path, repo, users)
