
from app.extensions import db
from datetime import datetime

class Book(db.Model):
    
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    title = db.Column(db.String(100))
    price = db.Column(db.Float)
    no_of_pages = db.Column(db.Integer)
    price_unit = db.Column(db.String(10))
    email = db.Column(db.String(50))
    contact = db.Column(db.String(20))
    location = db.Column(db.String(50))
    publication_date = db.Column(db.Date)

    def __init__(self, id, name, title, price,  no_of_pages, price_unit, email, contact, location):
        self.id = id
        self.name = name
        self.title = title
        self.price = price
        self.no_of_pages = no_of_pages
        self.price_unit = price_unit
        self.email = email
        self.contact = contact
        self.location = location


    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"
    


    