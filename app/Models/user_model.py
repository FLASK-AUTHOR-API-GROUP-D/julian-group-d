from app.extensions import db
from datetime import datetime
from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    contact = db.Column(db.String(15), unique=True, nullable=False)
    user_type = db.Column(db.String(20), default='author')
    biography = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime. now())
    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime. now())

    def __init__(self,id, first_name,last_name ,email, pasword, contact, user_type, biography):
           self.id = id
           self.first_name =first_name
           self.last_name =last_name
           self.email =email
           self.pasword =pasword
           self.contact =contact
           self.user_type = user_type
           self.biography = biography
           
def get_full_name(self):
            return f"{self.first_name} {self.last_name}" 

user = User
