

from app.extensions import db
from datetime import datetime
class Company(db.Model):
       __tablename__= "companies"
       id = db.Column(db.Integer, primary_key=True)
       first_name = db.Column(db.String(20))
       last_name = db.Column(db.String(50), nullable=False)
       contact = db.Column(db.String(50), nullable=False, unique =True)
       email = db.Column(db.String(50), nullable=False, unique=True)
       pasword = db.Column(db.String(34), nullable=False)
       created_at = db.Column(db.DateTime, default =datetime.now())
       updated_at = db.Column(db.DateTime, onupdate= datetime.now())

       def __init__(self,id, name, origin, description, created_at, updated_at, email,contact):
            self.id =id
            self.name =name
            self.origin =origin
            self.description =description
            self.created_at =created_at
            self.update_at =updated_at
            self.email =email
            self.contact =contact
    
         # all models are all related
       def company_details(self, id, name, origin, description, created_at, updated_at, email, contact):
            return f"{self.name} {self.origin} {self.description} {self.created_at} {self.updated_at} {self.email} {self.contact}"