from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from app.models.database import db

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if not email or not password or not name:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if db.find_one('users', {'email': email}):
        return jsonify({'error': 'User already exists'}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    user = {
        'email': email,
        'password': hashed_password.decode('utf-8'),
        'name': name,
        'xp': 0,
        'level': 1,
        'streak': 0,
        'badges': []
    }
    
    created_user = db.insert('users', user)
    access_token = create_access_token(identity=created_user['_id'])
    
    return jsonify({
        'message': 'User created successfully',
        'token': access_token,
        'user': {
            '_id': created_user['_id'],
            'email': created_user['email'],
            'name': created_user['name'],
            'xp': created_user['xp'],
            'level': created_user['level'],
            'streak': created_user['streak']
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = db.find_one('users', {'email': email})
    
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user['_id'])
    
    return jsonify({
        'message': 'Login successful',
        'token': access_token,
        'user': {
            '_id': user['_id'],
            'email': user['email'],
            'name': user['name'],
            'xp': user.get('xp', 0),
            'level': user.get('level', 1),
            'streak': user.get('streak', 0)
        }
    }), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = db.find_one('users', {'_id': user_id})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        '_id': user['_id'],
        'email': user['email'],
        'name': user['name'],
        'xp': user.get('xp', 0),
        'level': user.get('level', 1),
        'streak': user.get('streak', 0),
        'badges': user.get('badges', [])
    }), 200
