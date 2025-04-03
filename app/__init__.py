from flask import Flask
from app.extensions import db, migrate, jwt
from flask import Blueprint
from app.Controllers.auth.auth_controllers import auth
from app.Controllers.books.books_controllers import books
from app.Controllers.user.user_controllers import users



   #application factory function
def create_app(): 

     app = Flask(__name__)
     
     app.config.from_object('config.Config')

     db.init_app(app)
    # migrate.init_app(app, db)

     from flask_migrate import Migrate

     migrate = Migrate(app, db)
     jwt.init_app(app)


     #registering models
     from app.Models.author_model import Author
     from app.Models.book_model import Book
     from app.Models.company_model import Company



     #registering blueprints
     app.register_blueprint(auth)
     app.register_blueprint(books)
     app.register_blueprint(users)


     #index route
     @app.route('/')
     # the decorator must be on top
     def index():
                      
        return'Hello'
          
     return app





