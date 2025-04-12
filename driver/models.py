from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Define here for local use

class DriverItem(db.Model):
    __tablename__ = 'driver_item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)
    def __repr__(self):
        return f'<DriverItem {self.name} - ${self.available}>'
