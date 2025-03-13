from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
import validators
from app.Controllers.auth import User
from app.Models.user_model import User
from app.extensions import db, bcrypt

#auth blueprint
auth_bp= Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# blueprint refers to templates or structures that guide how code is organized

#register user
@auth_bp.route('/register', methods=['POST'])
def regester_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('type', '')
    biography = data.get('biography', '') if user_type == "author" else ''
#validating of incoming request
    if not first_name or not last_name or not contact or not email:
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    if user_type == "author" and not biography:
        return jsonify({"error": "Enter your author biography"}), HTTP_400_BAD_REQUEST

    if not password or len(password) < 9:
        return jsonify({"error": "Password must be at least 9 characters long"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email address is already in use"}), HTTP_409_CONFLICT

    if User.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error": "Contact address is already in use"}), HTTP_409_CONFLICT

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            email=email,
            contact=contact,
            biography=biography
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": f"User '{new_user.first_name} {new_user.last_name}' has been created successfully",
            "user": {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "contact": new_user.contact,
                "biography": new_user.biography,
                "created_at": new_user.created_at,
                "updated_at": new_user.updated_at
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
