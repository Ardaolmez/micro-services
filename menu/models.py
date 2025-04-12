# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Define here for local use

class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<MenuItem {self.name} - ${self.price}>'
