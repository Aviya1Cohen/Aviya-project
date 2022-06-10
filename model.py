"""Models for books"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """ A user. """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    eng_level = db.Column(db.Integer)

    def __repr__(self):
        return f"<User user_id={self.user_id} first_name={self.first_name}>"


class Book(db.Model):
    """ A book. """

    __tablename__ = "books"

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    description = db.Column(db.String)
    page_num = db.Column(db.Integer)

    def __repr__(self):
        return f"<Book book_id={self.book_id} title={self.title}>"


class Genre(db.Model):
    """ Genre. """

    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_type = db.Column(db.String)

    def __repr__(self):
        return f"<Genre genre_id={self.genre_id} genre_type={self.genre_type}>"


class BookGenre(db.Model):
    """ A book genre. """

    __tablename__ = "book_genre"

    book_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.genre_id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))

    genre = db.relationship("Genre")
    book = db.relationship("Book")

    def __repr__(self):
        return f"<BookGenre book_genre_id={self.book_genre_id} genre_id={self.genre_id}>"


class Rating(db.Model):
    """ A book rating """

    __tablename__ = "rating"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    score = db.Column(db.Integer)
    review = db.Column(db.String)

    book = db.relationship("Book")
    user = db.relationship("User")

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} book_id={self.book_id}>"


class Favorite(db.Model):
    """ Favorite book for user """

    __tablename__ = "favorite"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    book = db.relationship("Book")
    user = db.relationship("User")

    def __repr__(self):
        return f"<Favorite favorite_id={self.favorite_id} book_id={self.book_id}>"

def connect_to_db(flask_app, db_uri="postgresql:///books", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")
    