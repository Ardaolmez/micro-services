from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Define here for local use

class AdminItem(db.Model):
    __tablename__ = 'admin_item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Float, nullable=False)
    def __repr__(self):
        return f'<AdminItem {self.name}>'
