class User:
    def __init__(self, username, password, email):
        self._username = username.strip().lower()
        self._password = password
        self._email = email
        self._profile_pic = 'static/img/user.jpg'
        self._watched_movies = []
        self._time_spent_watching_movies_minutes = 0
        if len(self._watched_movies) != 0:
            for movie in self._watched_movies:
                self._time_spent_watching_movies_minutes += movie.runtime_minutes
        self._reviews = []

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def email(self):
        return self._email

    @property
    def profile_pic(self):
        return self._profile_pic

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def time_spent_watching_movies_minutes(self):
        return self._time_spent_watching_movies_minutes

    @property
    def reviews(self):
        return self._reviews

    def __repr__(self):
        return "<User " + self.username + ">"

    def __eq__(self, other):
        if other!=None:
            return self.username == other.username
        else:
            return False

    def __lt__(self, other):
        return self.username < other.username

    def __hash__(self):
        return hash(self.username)

    def watch_movie(self, movie):
        self._watched_movies.append(movie)
        self._time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        self._reviews.append(review)