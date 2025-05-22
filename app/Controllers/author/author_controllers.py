from flask import Blueprint, request, jsonify
from app.extensions import db
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_401_UNAUTHORISED
import validators
from app.Models.author_model import Author
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

# Author blueprint
author = Blueprint('author', __name__, url_prefix='/api/v1/authors')

# Get all authors
@author.route('/', methods=['GET'])
def get_all_authors():
    try:
        all_authors = Author.query.all()  
        authors_data = []

        for author in all_authors:
            author_info = {
                'id': author.id,
                'first_name': author.first_name,
                'last_name': author.last_name,
                'email': author.email,
                'authorname': author.authorname,
                'contact': author.contact,
                'biography': author.biography,
                'created_at': author.created_at,
                'companies': [],  # Assuming companies will be populated later
                'books': []      # Assuming books will be populated later
            }
            authors_data.append(author_info)

        return jsonify({
            "message": "All authors retrieved successfully",  
            'total': len(authors_data),
            "authors": authors_data
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR

 # Get author by ID
@author.get('/<int:id>', methods=['GET'])
@jwt_required()
def get_author_by_id(id):

    try:

        author = Author.query.filter_by(id=id).first()
        
        books = []
        companies = []



        if hasattr(author, 'books'):
                books = [{
                    'id': book.id,
                    'title': book.title,
                    'price': book.price,
                    'no_of_pages': book.no_of_pages,
                    'price_unit': book.price_unit,
                    'publication_date': book.publication_date
                } for book in author.books]

        if hasattr(author, 'companies'):
                companies = [{
                    'id': company.id,
                    'name': company.name,
                    'origin': company.origin,
                    'description': company.description
                } for company in author.companies]


                return jsonify({
                     "message": "Author details retrieved successfully",
                    "author":{
                        'id': author.id,
                        'first_name': author.first_name,
                        'last_name': author.last_name,
                        'email': author.email,
                        'authorname': author.authorname,
                        'contact': author.contact,
                        'biography': author.biography,
                        'created_at': author.created_at,
                        'companies': companies,
                        'books': books
                    }
                     
                }), HTTP_200_OK
        
    except Exception as e:
        return jsonify({
                "error": str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
    
    # Update author details
@author.put('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_author_details(id):
     

     try:
          current_author = get_jwt_identity()
          logged_in_user = Author.query.filter_by(id=id).first()
          #get author by id
          author = Author.query.filter_by(id=id).first()
          if not author:
                 return jsonify({
                        "message": "Author not found"
                 }), HTTP_400_BAD_REQUEST
          
          elif logged_in_user.user_type != 'admin' and author.id != current_author:
                    return jsonify({
                            "message": "You are not authorized to update this author details"
                    }), HTTP_401_UNAUTHORISED
          
          else:
               # store request data

               name = request.get_json.get('name', author.name)
               email = request.get_json.get('email', author.email)
               contact = request.get_json.get('contact', author.contact)
              
               if contact != author.contact and Author.query.filter_by(contact).first():
                    return jsonify({
                        "message": "Contact number already exists"
                    }), HTTP_409_CONFLICT
               

          author.name = name
          author.email = email
          author.contact = contact

          db.session.commit()

        
          return jsonify({
                    "message": f"{name} has been updated successfully",
                    "author": {
                        "id": author.id,
                        "first_name": author.first_name,
                        "last_name": author.last_name,
                        "email": author.email,
                        "contact": author.contact,
                        "biography": author.biography,
                        "created_at": author.created_at
                    
                    }
                })
     except Exception as e:
          return jsonify({
                "error": str(e)
          }), HTTP_500_INTERNAL_SERVER_ERROR
     



# Delete author
@author.delete('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_author(id):
    try:
        current_author = get_jwt_identity()
        logged_in_user = Author.query.filter_by(id=id).first()
        #get author by id
        author = Author.query.filter_by(id=id).first()
        if not author:
            return jsonify({
                "message": "Author not found"
            }), HTTP_400_BAD_REQUEST
        
        elif logged_in_user.user_type != 'admin' and author.id != current_author:
            return jsonify({
                "message": "You are not authorized to delete this author"
            }), HTTP_401_UNAUTHORISED
        
        else:
            db.session.delete(author)
            db.session.commit()

            return jsonify({
                "message": f"{author.first_name} has been deleted successfully"
            }), HTTP_200_OK
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
          
                  
     


