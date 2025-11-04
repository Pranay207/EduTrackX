from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.database import db
from datetime import datetime, timedelta

bp = Blueprint('study', __name__, url_prefix='/api/study')

@bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_study_sessions():
    user_id = get_jwt_identity()
    sessions = db.find('study_sessions', {'user_id': user_id})
    return jsonify(sessions), 200

@bp.route('/sessions', methods=['POST'])
@jwt_required()
def create_study_session():
    user_id = get_jwt_identity()
    data = request.json
    
    session = {
        'user_id': user_id,
        'subject_id': data.get('subject_id'),
        'duration': data.get('duration'),
        'date': data.get('date', datetime.now().isoformat()),
        'type': data.get('type', 'pomodoro')
    }
    
    created_session = db.insert('study_sessions', session)
    
    user = db.find_one('users', {'_id': user_id})
    new_xp = user.get('xp', 0) + (data.get('duration', 25) // 5)
    db.update('users', {'_id': user_id}, {'xp': new_xp})
    
    return jsonify(created_session), 201

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_study_stats():
    user_id = get_jwt_identity()
    sessions = db.find('study_sessions', {'user_id': user_id})
    
    total_time = sum(s.get('duration', 0) for s in sessions)
    
    today = datetime.now().date().isoformat()
    today_sessions = [s for s in sessions if s.get('date', '').startswith(today)]
    today_time = sum(s.get('duration', 0) for s in today_sessions)
    
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    week_sessions = [s for s in sessions if s.get('date', '') >= week_ago]
    
    return jsonify({
        'total_time': total_time,
        'total_sessions': len(sessions),
        'today_time': today_time,
        'today_sessions': len(today_sessions),
        'week_sessions': len(week_sessions)
    }), 200
