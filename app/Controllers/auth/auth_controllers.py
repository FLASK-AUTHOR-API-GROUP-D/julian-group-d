from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_401_UNAUTHORISED
import validators
from app.Models.author_model import Author
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from flask_jwt_extended import get_jwt_identity

#auth blueprint
auth= Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# blueprint refers to templates or structures that guide how code is organized
# authentication refers to the process of verifying the identity of a user or system 
# and is often used in the context of securing access to resources or services.
# validators is a library that provides a set of functions for validating various types of data, such as email addresses, URLs.

#register user
@auth.route('/register', methods=['POST'])
def register_author():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    type = data.get('author_type') if 'author_type' in data else 'author'
    password = data.get('password')
    biography = data.get('biography') if type == "author" else ''

#validating of incoming request
    if not first_name or not last_name or not contact or not email:# ensuring all fields are provided
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    if type == "author" and not biography:
        return jsonify({"error": "Enter your author biography"}), HTTP_400_BAD_REQUEST# biography is required for author type

    if not password or len(password) < 8: # ensuring password is provided and has a minimum length of 8 characters
        return jsonify({"error": "Password is too short"}), HTTP_400_BAD_REQUEST

    if not validators.email(email): ## validating email format using the validators library
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

    if Author.query.filter_by(email=email).first() is not None: # checking if email already exists in the database
        return jsonify({"error": "Email address is already in use"}), HTTP_409_CONFLICT

    if Author.query.filter_by(contact=contact).first() is not None:# checking if contact already exists in the database
        return jsonify({"error": "Contact address is already in use"}), HTTP_409_CONFLICT

    try:
        hashed_password = bcrypt.generate_password_hash(password) # hashing the password
# creating new author instance
        new_author = Author(
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            email=email,
            contact=contact,
            biography=biography
        )
        db.session.add(new_author)
        db.session.commit()
        # authorname
        authorname = new_author.get_full_name()

        return jsonify({
    "message": f"{authorname} has been created as an {new_author.author_type} successfully",
    "author": {
        # "id": new_author.id,
        "first_name": new_author.first_name,
        "last_name": new_author.last_name,
        "email": new_author.email,
        "contact": new_author.contact,
        "password": new_author.password,
        "biography": new_author.biography,
        "created_at": new_author.created_at,
        
    }
}), HTTP_201_CREATED


    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    

#login author
@auth.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    try:

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), HTTP_400_BAD_REQUEST 

        author = Author.query.filter_by(email=email).first()
        
        if author:
          is_correct_password = bcrypt.check_password_hash(author.password, password)  
          
          if is_correct_password:
            access_token = create_access_token(identity=str(author.id))
            reflesh_token = create_refresh_token(identity=str(author.id))

            return jsonify({
                'author': {
                  'id': author.id, 
                  'authorname':author.get_full_name(),
                  'email': author.email, 
                  'access_token': access_token,
                  'refresh_token': reflesh_token,

                  'type': author.author_type,
                  'biography': author.biography,
                 
                }, 
                'message': "You have successfully logged in into your account",
               
            }), HTTP_200_OK
          
          else:
            return jsonify({"message": "Invalid password"}), HTTP_401_UNAUTHORISED
        
        else:
         return jsonify({"message": "Invalid email address"}), HTTP_401_UNAUTHORISED   
    
    
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    


@auth.route("token/refresh",methods=["POST"])
@jwt_required(refresh=True)
def refresh():
   identity = str(get_jwt_identity())
   access_token = create_access_token(identity=identity)
   return jsonify({'access_token':access_token})



