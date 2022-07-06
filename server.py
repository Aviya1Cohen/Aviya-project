"""Server for books app."""

from flask import Flask, render_template, flash, redirect, request, session
from model import connect_to_db, db, Favorite

import crud


app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route("/")
def homepage():
    """View homepage."""
    books = []
    english_level_by_book_id = {}
    if 'user_id' in session:
        (books, english_level_by_book_id) = crud.get_books()

    return render_template("homepage.html", books=books, english_level_by_book_id=english_level_by_book_id)


@app.route("/book/<book_id>")
def show_book(book_id):
    """Show details on a particular book."""

    book = crud.get_book_by_id(book_id)
    (user_rating, other_ratings) = crud.get_ratings_by_book_id(book_id, session['user_id'])

    return render_template("book_details.html", book=book, user_rating=user_rating, other_ratings=other_ratings, level_str=['Easy', 'Medium', 'Hard'])

@app.route("/favorites")
def favorite_books():
    """Show favorite books for user"""

    (books, english_level_by_book_id) = crud.get_favorite_books()

    return render_template("favorites.html", books=books, english_level_by_book_id=english_level_by_book_id)


@app.route("/book/<book_id>/rating", methods=["POST"])
def rate_book(book_id):
    """Rate a book"""

    english_level = request.form.get("english_level")
    review = request.form.get("review")

    rating = crud.create_rating(user_id=session['user_id'], book_id=book_id, english_level=english_level, review=review)
    db.session.add(rating)
    db.session.commit()

    return redirect("/book/" + book_id)

@app.route("/favorite/<book_id>", methods=["POST"])
def add_book_to_favorites(book_id):
    """Add a book to user's favorites"""

    favorite = crud.create_favorite(user_id=session['user_id'], book_id=book_id)
    db.session.add(favorite)
    db.session.commit()

    return redirect(request.referrer)

@app.route("/unfavorite/<favorite_id>", methods=["POST"])
def delete_book_favorite(favorite_id):
    """Remove specified fav"""

    Favorite.query.filter_by(favorite_id=favorite_id).delete()
    db.session.commit()

    return redirect(request.referrer)


@app.route("/signup")
def signup():
    """registration form"""
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def register_user():
    """Register"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("A user with the same email already exists.")
        return redirect('/signup')
    else:
        user = crud.create_user(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can now log in.")

        return redirect("/")
    
@app.route("/login")
def sigin():
    """loginh form"""
    return render_template("login.html" )

@app.route("/login", methods=["POST"])
def login():
    """Login"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user is None:
        flash("User not found!")
    elif user.password != password:
        flash("Wrong password!")
    else:
        session['username'] = user.first_name + ' ' + user.last_name
        session['user_id'] = user.user_id

    return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    """Logout"""

    session.clear()
    return redirect("/")

    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)