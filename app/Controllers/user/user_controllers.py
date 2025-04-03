from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_401_UNAUTHORISED
import validators
from app.Models.author_model import Author
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


#user blueprint
users= Blueprint('user', __name__, url_prefix='/api/v1/users')

# get all authors

@users.get('/authors')
def get_all_authorss():

  try:

        all_authors = Author.query.filter_by(author_type='author').all()
        
        authors_data = [] 

        for author in all_authors:
            author_info = {
                'id': author.id,
                'first_name':author.first_name,
                'last_name': author.last_name,
                'email': author.email,
                'authorname': author.authorname,
                'contact': author.contact,
                'biography': author.biography,
                'created_at': author.created_at,
                'companies': [],
                'books': []
            }

            if hasattr(author, 'books'):
               author_info['books'] = [{
                     'id': book.id,
                     'title':book.title,
                     'price_unit': book.price_unit,
                     'description': book.description,
                      'publication': book.publication,
                      'created_at': book.created_at,
                      'image': book.image} for book in author.books
                    ]
            
            if hasattr(author, 'companies'):
                author_info['companies'] = [{
                     'id': company.id,
                     'name':company.name,
                     'location': company.location,
                     'created_at': company.created_at} for company in author.companies
                    ]
                

            authors_data.append(author_info)


        return jsonify({
           "massage": "All authors retrieved successfully",
           'total': len(authors_data),
              "authors": authors_data
        }), HTTP_200_OK
    
  except Exception as e:
      return jsonify({
         "error": str(e)
         }), HTTP_500_INTERNAL_SERVER_ERROR
