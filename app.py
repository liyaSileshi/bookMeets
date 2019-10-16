from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/bookMeets')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
books = db.books


app = Flask(__name__)


@app.route('/')
def book_index():
    """Show all books."""
    return render_template('book_index.html', books=books.find())

@app.route('/books/new')
def book_new():
    """Add new book."""
    return render_template('book_new.html', book = {}, title = 'Add book')
            
@app.route('/books', methods=['POST'])
def book_submit():
    """Submit a new book."""
    book = {
        'type': request.form.get('type'),
        'name' : request.form.get('name'),
        'image': request.form.get('image'),
        'description' : request.form.get('description')
    }
    book_id = books.insert_one(book).inserted_id
    #lipsticks.insert_one(lipstick)
    # print(request.form.to_dict())
    return redirect(url_for('book_show', book_id = book_id))

@app.route('/books/<book_id>')
def book_show(book_id):
    """Show a single book."""
    book = books.find_one({'_id' : ObjectId(book_id)})
    return render_template('book_show.html', book= book)

@app.route('/books/<book_id>/edit')
def book_edit(book_id):
    """Show the edit form for a book."""
    book = books.find_one({'_id': ObjectId(book_id)})
    return render_template('book_edit.html', book=book, tilte = 'Edit Book')

@app.route('/books/<book_id>', methods=['POST'])
def book_update(book_id):
    """Submit an edited book."""
    updated_book = {
         'type': request.form.get('type'),
        'name' : request.form.get('name'),
        'image': request.form.get('image'),
        'description' : request.form.get('description')
    }
    books.update_one(
        {'_id': ObjectId(book_id)},
        {'$set': updated_book})
    return redirect(url_for('book_show', book_id=book_id))

@app.route('/books/<book_id>/delete', methods=['POST'])
def book_delete(book_id):
    """Delete one book."""
    books.delete_one({'_id': ObjectId(book_id)})
    return redirect(url_for('book_index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

