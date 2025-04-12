from flask_sqlalchemy import SQLAlchemy

# initialize db
db = SQLAlchemy()

class BookingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.Text, nullable=False)  # store as JSON string
    total = db.Column(db.Float, nullable=False)
    driver_name = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f'<BookingItem {self.items} - ${self.driver_name} - ${self.total}>'

    def as_dict(self):
        return {
            "id": self.id,
            "items": json.loads(self.items),
            "total": self.total,
            "driver_name": self.driver_name
        }
