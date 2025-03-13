from flask import Flask
from app.extensions import db, migrate
from flask import Blueprint
from app.Controllers.auth.auth_controllers import auth_bp

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
books_bp = Blueprint('books', __name__, url_prefix='/api/v1/books')
company_bp = Blueprint('company', __name__, url_prefix='/api/v1/company')

# Define routes here...
@auth_bp.route('/register', methods=['POST'])
   #application factory function
def create_app(): 

     app = Flask(__name__)
     
     app.config.from_object('config.Config')

     db.init_app(app)
     migrate.init_app(app,db)
     #registering blueprints
     from app.Controllers.auth.auth_controllers import auth_bp
     from app.Controllers.books.books_controllers import books_bp
     from app.Controllers.company.company_controllers import company_bp

     #registering models
     from app.Models.user_model import User
     from app.Models.book_model import Book
     from app.Models.company_model import Company



     #registering blueprints
     app.register_blueprint(auth_bp)


     #index route
     @app.route('/')
     # the decorator must be on top
     def index():
                      
        return'Hello'
          
     return app