from flask import Flask
from models import db, BookingItem
from routes import booking_routes
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    db_path = os.path.join(app.instance_path, 'booking.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        app.register_blueprint(booking_routes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5003)

