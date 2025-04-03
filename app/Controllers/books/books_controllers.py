from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_401_UNAUTHORISED
import validators
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.Models.book_model import Book
# Books blueprint
books = Blueprint('books', __name__, url_prefix='/api/v1/books')

# Getting all books in the database
@books.get('/')
def get_all_books():
    try:
        
        all_books = Book.query.all()
        
        books_data = [] 

        # Loop through all books and extract relevant information
        # loop is used to iterate over the list of books and extract the relevant information for each book
        for book in all_books:
            book_info = {
               'id': book.id,
                'name': book.name,
                'title': book.title,
                'price': book.price,
                'no_of_pages': book.no_of_pages,
                'price_unit': book.price_unit,
                'email': book.email,
                'contact': book.contact,
                'location': book.location,
                'publication_date': book.publication_date
            }
            books_data.append(book_info)

        return jsonify({
            "message": "All books retrieved successfully",  
            "books": books_data
        }), HTTP_200_OK

    except Exception as e:
        # Return an error response in case of failure
        return jsonify({
            "error": str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
