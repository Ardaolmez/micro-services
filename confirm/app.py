# confirm_service/app.py
from flask import Flask
from routes import confirm_routes

app = Flask(__name__)
app.register_blueprint(confirm_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
