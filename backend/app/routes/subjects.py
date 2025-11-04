from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.database import db

bp = Blueprint('subjects', __name__, url_prefix='/api/subjects')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_subjects():
    user_id = get_jwt_identity()
    subjects = db.find('subjects', {'user_id': user_id})
    return jsonify(subjects), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_subject():
    user_id = get_jwt_identity()
    data = request.json
    
    subject = {
        'user_id': user_id,
        'name': data.get('name'),
        'code': data.get('code'),
        'credits': data.get('credits', 3),
        'professor': data.get('professor', ''),
        'color': data.get('color', '#3B82F6')
    }
    
    created_subject = db.insert('subjects', subject)
    return jsonify(created_subject), 201

@bp.route('/<subject_id>', methods=['PUT'])
@jwt_required()
def update_subject(subject_id):
    user_id = get_jwt_identity()
    data = request.json
    
    subject = db.find_one('subjects', {'_id': subject_id, 'user_id': user_id})
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404
    
    db.update('subjects', {'_id': subject_id}, data)
    updated_subject = db.find_one('subjects', {'_id': subject_id})
    
    return jsonify(updated_subject), 200

@bp.route('/<subject_id>', methods=['DELETE'])
@jwt_required()
def delete_subject(subject_id):
    user_id = get_jwt_identity()
    
    deleted = db.delete('subjects', {'_id': subject_id, 'user_id': user_id})
    if deleted == 0:
        return jsonify({'error': 'Subject not found'}), 404
    
    db.delete('marks', {'subject_id': subject_id})
    
    return jsonify({'message': 'Subject deleted'}), 200

@bp.route('/<subject_id>/marks', methods=['GET'])
@jwt_required()
def get_subject_marks(subject_id):
    user_id = get_jwt_identity()
    marks = db.find('marks', {'user_id': user_id, 'subject_id': subject_id})
    return jsonify(marks), 200

@bp.route('/<subject_id>/marks', methods=['POST'])
@jwt_required()
def add_marks(subject_id):
    user_id = get_jwt_identity()
    data = request.json
    
    mark = {
        'user_id': user_id,
        'subject_id': subject_id,
        'exam_type': data.get('exam_type'),
        'marks_obtained': data.get('marks_obtained'),
        'total_marks': data.get('total_marks'),
        'date': data.get('date'),
        'percentage': (data.get('marks_obtained') / data.get('total_marks')) * 100
    }
    
    created_mark = db.insert('marks', mark)
    
    user = db.find_one('users', {'_id': user_id})
    new_xp = user.get('xp', 0) + 10
    db.update('users', {'_id': user_id}, {'xp': new_xp})
    
    return jsonify(created_mark), 201
