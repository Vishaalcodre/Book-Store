from flask import render_template, flash,  redirect, url_for, request
from app.catalog import main
from app import db
from app.catalog.models import Book, Publication
from flask_login import login_required
from .forms import EditForm, CreateForm



@main.route('/')
def display_books():
    books = Book.query.all()

    return render_template('home.html', books=books)

@main.route('/display/publisher/<int:publisher_id>')
def display_publisher(publisher_id):
    publisher = Publication.query.filter_by(id=publisher_id).first()

    publisher_books = Book.query.filter_by(pub_id = publisher_id).all()

    return render_template('publisher.html', publisher=publisher, publisher_books=publisher_books)

@main.route('/book/delete/<book_id>', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)

    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully')
        return redirect(url_for('main.display_books'))
    
    return  render_template('delete_book.html', book=book, book_id=book_id)

@main.route('/edit/book/<book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get(book_id)
    form = EditForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.format =  form.format.data
        book.num_pages = form.num_pages.data
        db.session.add(book)
        db.session.commit()
        flash("Book edited successfully")
        return redirect(url_for('main.display_books'))
    
    return render_template('edit_book.html', form=form)

@main.route('/create/book/<pub_id>', methods=['GET', 'POST'])
@login_required
def  create_book(pub_id):
    form = CreateForm()
    form.pub_id.data = pub_id

    if form.validate_on_submit():
        book = Book(
            title=form.title.data, 
            author=form.author.data,
            book_format=form.format.data,
            num_pages=form.num_pages.data,
            avg_rating=form.avg_rating.data,
            image=form.img_url.data,
            pub_id=form.pub_id.data
            )
        
        # Check if the image already exists in the database
        existing_book = Book.query.filter_by(image=form.img_url).first()
        if existing_book:
            flash('Book with this image already exists')
            return redirect(url_for('main.create_book'))
        
        db.session.add(book)
        db.session.commit()
        flash("Book Created Successfully")
        return(redirect(url_for('main.display_publisher',  publisher_id=pub_id)))

    
    return render_template('create_book.html', form=form,  pub_id=pub_id)



