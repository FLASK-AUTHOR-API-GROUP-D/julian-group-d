from flask import Blueprint, request, jsonify
from app.Models.book_model import Book
from app import db

def some_function():
    from app.Controllers.books import books_controllers 

books_bp = Blueprint('books', __name__, url_prefix='/api/v1/books')

@books_bp.route('/register', methods=['POST'])

# 1. Create a new book
def create_book():
    data = request.get_json()
    title = data.get('title')
    author_id = data.get('author_id')
    genre = data.get('genre')

    new_book = Book(title=title, author_id=author_id, genre=genre)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book created successfully'}), 201

# 2. Read all books
@books_bp.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200

# 3. Update a book
@books_bp.route('/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    book.title = data.get('title', book.title)
    book.genre = data.get('genre', book.genre)
    db.session.commit()

    return jsonify({'message': 'Book updated successfully'}), 200

# 4. Delete a book
@books_bp.route('/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully'}), 200
