"""Script to seed database."""

import os
# import csv
import random
import requests

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
book_id = 1
for _ in range(10):
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q=*&maxResults=40&key=AIzaSyAHaYSMCZBbwl5l6fdZt4yhHyWWujiMnSU')
    items = response.json()['items']
    for item in items:
        book = Book(
            book_id=book_id,
            title=item['volumeInfo']['title'],
            author=' - '.join(item['volumeInfo']['authors']) if 'authors' in item['volumeInfo'] else 'X', 
            description=item['volumeInfo']['description'] if 'description' in item['volumeInfo'] else 'X', 
            image=item['volumeInfo']['imageLinks']['thumbnail'],
            page_num=int(item['volumeInfo']['pageCount'] if 'pageCount' in item['volumeInfo'] else -1)
        )
        books.append(book)
        number_of_genres = random.choice([1, 2, 3])
        for i in range(number_of_genres):
            genre_id = random.choice(genres_ids)
            book_genres.append(BookGenre(genre_id=genre_id, book_id=book.book_id))

        book_id += 1
# with open('books.csv') as booksfile: 
#     reader = csv.DictReader(booksfile)
#     for row in reader:
#         try:
#             book = Book(
#                 book_id=row['bookID'],
#                 title=row['title'],
#                 author=row['authors'], 
#                 description=row['publisher'] + ' - ' + row['publication_date'],
#                 page_num=int(row['num_pages'])
#             )
#             books.append(book)
#             number_of_genres = random.choice([1, 2, 3])
#             for i in range(number_of_genres):
#                 genre_id = random.choice(genres_ids)
#                 book_genres.append(BookGenre(genre_id=genre_id, book_id=book.book_id))
#         except Exception:
#             print('## Error in row', row)
            
    
db.session.add_all(books)
db.session.add_all(book_genres)
db.session.commit()
