from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/bookMeets')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
books = db.books
users = db.users


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
        'author': request.form.get('author'),
        'image': request.form.get('image'),
        'description' : request.form.get('description')
    }
    book_id = books.insert_one(book).inserted_id
    
    # print(request.form.to_dict())
    return redirect(url_for('book_show', book_id = book_id))

@app.route('/books/<book_id>')
def book_show(book_id):
    """Show a single book."""
    book = books.find_one({'_id' : ObjectId(book_id)})
    book_users = users.find({'book_id': ObjectId(book_id)})
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
        'author' : request.form.get('author'),
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

@app.route('/books/<book_id>/adduser', methods=['GET'])
def user_new(book_id):
    """Add a new user."""
    
        #print(user)
    #return redirect(url_for('book_show', book_id=request.form.get('book_id')))
    return render_template('user_new.html', book_id=book_id)

@app.route('/books/<book_id>/adduser', methods=['POST'])
def user_submit(book_id):
    """Submit a new user."""
    user = {
       'name': request.form.get('name'),
       'contact' : request.form.get('contact'),
       'book_id': ObjectId(book_id),
    }
    user_id = users.insert_one(user).inserted_id
    # print(request.form.to_dict())
    return redirect(url_for('all_users', book_id=book_id))


@app.route('/books/<book_id>/seeuser', methods=['GET','POST'])
def all_users(book_id):
    """Show all users."""
    return render_template('user_index.html', users=users.find({'book_id': ObjectId(book_id)}))




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

