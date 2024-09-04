from flask import render_template
from app.catalog import main
from app import db
from app.catalog.models import Book, Publication


@main.route('/')
def get_book():
    books = Book.query.all()

    return render_template('home.html', books=books)