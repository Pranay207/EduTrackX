from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400
    
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    jwt = JWTManager(app)
    
    from app.routes import auth, subjects, assignments, attendance, study, ai, dashboard, export
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(subjects.bp)
    app.register_blueprint(assignments.bp)
    app.register_blueprint(attendance.bp)
    app.register_blueprint(study.bp)
    app.register_blueprint(ai.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(export.bp)
    
    return app
