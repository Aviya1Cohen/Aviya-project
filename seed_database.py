"""Script to seed database."""

import os
import csv
import random

from model import connect_to_db, db, Book, BookGenre, Genre
from server import app

os.system("dropdb books")
os.system("createdb books")


connect_to_db(app)

db.create_all()

genres = ["Action and Adventure", "Classics", "Comic Book or Graphic Novel", "Detective and Mystery", "Fantasy", "Historical Fiction", "Horror", "Literary Fiction"]
db.session.add_all([Genre(genre_type=g) for g in genres])
db.session.commit()

genres_ids = range(1, len(genres) + 1) # [1, 2, ..., 8]
books = []
book_genres = []
with open('books.csv') as booksfile: 
    reader = csv.DictReader(booksfile)
    for row in reader:
        try:
            book = Book(
                book_id=row['bookID'],
                title=row['title'],
                author=row['authors'], 
                description=row['publisher'] + ' - ' + row['publication_date'],
                page_num=int(row['num_pages'])
            )
            books.append(book)
            number_of_genres = random.choice([1, 2, 3])
            for i in range(number_of_genres):
                genre_id = random.choice(genres_ids)
                book_genres.append(BookGenre(genre_id=genre_id, book_id=book.book_id))
        except Exception:
            print('## Error in row', row)
            
    
db.session.add_all(books)
db.session.add_all(book_genres)
db.session.commit()
