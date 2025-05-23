from app.extensions import db
from datetime import datetime
from app.extensions import db


class Author(db.Model):
    
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)  
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    contact = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    biography = db.Column(db.Text, nullable=True)
    author_type = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())

    def __init__(self, first_name, last_name, email, contact, password, biography=None):
        super(Author).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.password = password
        self.biography = biography
        self.type = type
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
        







