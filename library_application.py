from flask import Flask, render_template, request

app = Flask(__name__)

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def display(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}"

class EBook(Book):
    def __init__(self, title, author, isbn, file_format):
        super().__init__(title, author, isbn)
        self.file_format = file_format

    def display(self):
        base_info = super().display()
        return f"{base_info}, Format: {self.file_format}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_books(self):
        return [book.display() for book in self.books]

    def search_by_title(self, title):
        matching_books = [book for book in self.books if book.title == title]
        return [book.display() for book in matching_books]

    def delete_book(self, title):
        deleted_book = None
        for i, book in enumerate(self.books):
            if book.title == title:
                deleted_book = self.books.pop(i)
                break
        return deleted_book

library = Library()

@app.route('/')
def home():
    return render_template('library_app.html', books=library.display_books())

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    fileformat = request.form.get('ff_add')

    new_book = EBook(title, author, isbn, fileformat)
    library.add_book(new_book)

    return render_template('library.html', books=library.display_books(), added_book=new_book.display())

@app.route('/search_book', methods=['POST'])
def search_book():
    title = request.form.get('title')
    found_books = library.search_by_title(title)

    return render_template('library.html', books=found_books)

@app.route('/delete_book', methods=['POST'])
def delete_book():
    title = request.form.get('title')
    deleted_book = library.delete_book(title)

    if deleted_book:
        deleted_book_info = deleted_book.display()
    else:
        deleted_book_info = f"Book with title '{title}' not found."
    return render_template('library.html', books=library.display_books(), deleted_book=deleted_book_info)

if __name__ == '__main__':
    app.run(debug=True)
