"""CRUD operations."""
from sqlalchemy import and_
from sqlalchemy.sql import func
from model import User, Book, Rating, Favorite, connect_to_db, db
from flask import session


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

def get_english_level_by_book_id():
    """engish level"""
    level_to_str={0: 'Easy', 1: 'Medium', 2: 'Hard'}
    english_level_by_book_id = {}
    for (book_id, avg_eng_level) in db.session.query(Rating.book_id, func.avg(Rating.english_level).label('average_english_level')).group_by(Rating.book_id).all():
        english_level_by_book_id[book_id] = level_to_str[int(avg_eng_level)]

    return english_level_by_book_id

def get_books():
    """Return all books."""

    books = db.session.query(Book.book_id, Book.title, Book.author, Favorite.favorite_id).join(Favorite, and_(Book.book_id == Favorite.book_id, Favorite.user_id == session['user_id']), isouter=True).limit(500).all()
    english_level_by_book_id = get_english_level_by_book_id()
    
    return (books, english_level_by_book_id)

def get_favorite_books():
    """Return all books."""

    books = db.session.query(Favorite.book_id, Favorite.favorite_id, Book.author, Book.title).join(Book, and_(Book.book_id == Favorite.book_id, Favorite.user_id == session['user_id']), isouter=False).limit(500).all()
    english_level_by_book_id = get_english_level_by_book_id()
    
    return (books, english_level_by_book_id)

def get_book_by_id(book_id):
    """Return a book by primary key."""

    return Book.query.get(book_id)


def create_rating(user_id, book_id, english_level, review):
    """Create and return a new rating"""

    rating = Rating(user_id=user_id, book_id=book_id, english_level=english_level, review=review)

    return rating


def get_ratings_by_book_id(book_id, user_id):
    """Return a book by primary key."""
    user_rating = Rating.query.filter(Rating.book_id == book_id, Rating.user_id == user_id).first()
    other_ratings = Rating.query.filter(Rating.book_id == book_id, Rating.user_id != user_id).all()

    return (user_rating, other_ratings)


def create_favorite(user_id, book_id):
    """Create a favorite for the given book/user"""

    favorite = Favorite(user_id=user_id, book_id=book_id)

    return favorite




if __name__ == "__main__":
    from server import app

    connect_to_db(app)