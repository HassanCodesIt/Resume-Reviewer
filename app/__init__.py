import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, '..', 'uploads')

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app 