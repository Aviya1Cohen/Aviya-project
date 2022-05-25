"""CRUD operations."""

from model import User, Book, Rating, connect_to_db


def create_user(first_name, last_name, email, password):
    """Create new user."""

    user = User(first_name=first_name, last_name=last_name, email=email, password=password)

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_books():
    """Return all books."""

    return Book.query.all()


def get_book_by_id(book_id):
    """Return a book by primary key."""

    return Book.query.get(book_id)


def create_rating(user, book, score, review):
    """Create and return a new rating"""

    rating = Rating(user=user, book=book, score=score, review=review)

    return rating



if __name__ == "__main__":
    from server import app

    connect_to_db(app)