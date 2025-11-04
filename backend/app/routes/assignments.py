from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.database import db
from datetime import datetime

bp = Blueprint('assignments', __name__, url_prefix='/api/assignments')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_assignments():
    user_id = get_jwt_identity()
    assignments = db.find('assignments', {'user_id': user_id})
    
    for assignment in assignments:
        if assignment['deadline']:
            deadline = datetime.fromisoformat(assignment['deadline'].replace('Z', '+00:00'))
            assignment['is_overdue'] = deadline < datetime.now()
    
    return jsonify(assignments), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_assignment():
    user_id = get_jwt_identity()
    data = request.json
    
    assignment = {
        'user_id': user_id,
        'subject_id': data.get('subject_id'),
        'title': data.get('title'),
        'description': data.get('description', ''),
        'deadline': data.get('deadline'),
        'priority': data.get('priority', 'medium'),
        'status': data.get('status', 'pending'),
        'progress': data.get('progress', 0)
    }
    
    created_assignment = db.insert('assignments', assignment)
    return jsonify(created_assignment), 201

@bp.route('/<assignment_id>', methods=['PUT'])
@jwt_required()
def update_assignment(assignment_id):
    user_id = get_jwt_identity()
    data = request.json
    
    assignment = db.find_one('assignments', {'_id': assignment_id, 'user_id': user_id})
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    db.update('assignments', {'_id': assignment_id}, data)
    
    if data.get('status') == 'completed':
        user = db.find_one('users', {'_id': user_id})
        new_xp = user.get('xp', 0) + 25
        db.update('users', {'_id': user_id}, {'xp': new_xp})
    
    updated_assignment = db.find_one('assignments', {'_id': assignment_id})
    return jsonify(updated_assignment), 200

@bp.route('/<assignment_id>', methods=['DELETE'])
@jwt_required()
def delete_assignment(assignment_id):
    user_id = get_jwt_identity()
    
    deleted = db.delete('assignments', {'_id': assignment_id, 'user_id': user_id})
    if deleted == 0:
        return jsonify({'error': 'Assignment not found'}), 404
    
    return jsonify({'message': 'Assignment deleted'}), 200
