from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.database import db

bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_attendance():
    user_id = get_jwt_identity()
    attendance = db.find('attendance', {'user_id': user_id})
    return jsonify(attendance), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def mark_attendance():
    user_id = get_jwt_identity()
    data = request.json
    
    attendance_record = {
        'user_id': user_id,
        'subject_id': data.get('subject_id'),
        'date': data.get('date'),
        'status': data.get('status')
    }
    
    existing = db.find_one('attendance', {
        'user_id': user_id,
        'subject_id': data.get('subject_id'),
        'date': data.get('date')
    })
    
    if existing:
        db.update('attendance', {'_id': existing['_id']}, {'status': data.get('status')})
        updated_record = db.find_one('attendance', {'_id': existing['_id']})
        return jsonify(updated_record), 200
    
    created_record = db.insert('attendance', attendance_record)
    return jsonify(created_record), 201

@bp.route('/stats/<subject_id>', methods=['GET'])
@jwt_required()
def get_attendance_stats(subject_id):
    user_id = get_jwt_identity()
    records = db.find('attendance', {'user_id': user_id, 'subject_id': subject_id})
    
    total = len(records)
    present = len([r for r in records if r['status'] == 'present'])
    
    percentage = (present / total * 100) if total > 0 else 0
    
    return jsonify({
        'total': total,
        'present': present,
        'absent': total - present,
        'percentage': round(percentage, 2)
    }), 200
