from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.database import db
from datetime import datetime, timedelta

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    user_id = get_jwt_identity()
    
    subjects = db.find('subjects', {'user_id': user_id})
    marks = db.find('marks', {'user_id': user_id})
    assignments = db.find('assignments', {'user_id': user_id})
    attendance_records = db.find('attendance', {'user_id': user_id})
    study_sessions = db.find('study_sessions', {'user_id': user_id})
    user = db.find_one('users', {'_id': user_id})
    
    total_subjects = len(subjects)
    
    if marks:
        total_percentage = sum(m['percentage'] for m in marks)
        average_percentage = total_percentage / len(marks)
        gpa = (average_percentage / 100) * 10
        cgpa = gpa
    else:
        average_percentage = 0
        gpa = 0
        cgpa = 0
    
    pending_assignments = len([a for a in assignments if a['status'] != 'completed'])
    completed_assignments = len([a for a in assignments if a['status'] == 'completed'])
    
    if attendance_records:
        present = len([a for a in attendance_records if a['status'] == 'present'])
        attendance_percentage = (present / len(attendance_records)) * 100
    else:
        attendance_percentage = 0
    
    total_study_time = sum(s.get('duration', 0) for s in study_sessions)
    
    today = datetime.now().date().isoformat()
    today_sessions = [s for s in study_sessions if s.get('date', '').startswith(today)]
    today_study_time = sum(s.get('duration', 0) for s in today_sessions)
    
    upcoming_deadlines = []
    for assignment in assignments:
        if assignment['status'] != 'completed' and assignment.get('deadline'):
            deadline = datetime.fromisoformat(assignment['deadline'].replace('Z', '+00:00'))
            if deadline > datetime.now():
                subject = db.find_one('subjects', {'_id': assignment['subject_id']})
                upcoming_deadlines.append({
                    'assignment': assignment['title'],
                    'subject': subject['name'] if subject else 'Unknown',
                    'deadline': assignment['deadline'],
                    'priority': assignment.get('priority', 'medium')
                })
    
    upcoming_deadlines.sort(key=lambda x: x['deadline'])
    upcoming_deadlines = upcoming_deadlines[:5]
    
    return jsonify({
        'total_subjects': total_subjects,
        'average_percentage': round(average_percentage, 2),
        'gpa': round(gpa, 2),
        'cgpa': round(cgpa, 2),
        'pending_assignments': pending_assignments,
        'completed_assignments': completed_assignments,
        'attendance_percentage': round(attendance_percentage, 2),
        'total_study_time': total_study_time,
        'today_study_time': today_study_time,
        'upcoming_deadlines': upcoming_deadlines,
        'xp': user.get('xp', 0),
        'level': user.get('level', 1),
        'streak': user.get('streak', 0)
    }), 200

@bp.route('/charts/performance', methods=['GET'])
@jwt_required()
def get_performance_chart():
    user_id = get_jwt_identity()
    
    subjects = db.find('subjects', {'user_id': user_id})
    marks = db.find('marks', {'user_id': user_id})
    
    chart_data = []
    for subject in subjects:
        subject_marks = [m for m in marks if m['subject_id'] == subject['_id']]
        if subject_marks:
            avg = sum(m['percentage'] for m in subject_marks) / len(subject_marks)
            chart_data.append({
                'subject': subject['name'],
                'average': round(avg, 2)
            })
    
    return jsonify(chart_data), 200

@bp.route('/charts/attendance', methods=['GET'])
@jwt_required()
def get_attendance_chart():
    user_id = get_jwt_identity()
    
    subjects = db.find('subjects', {'user_id': user_id})
    attendance = db.find('attendance', {'user_id': user_id})
    
    chart_data = []
    for subject in subjects:
        subject_attendance = [a for a in attendance if a['subject_id'] == subject['_id']]
        if subject_attendance:
            present = len([a for a in subject_attendance if a['status'] == 'present'])
            percentage = (present / len(subject_attendance)) * 100
            chart_data.append({
                'subject': subject['name'],
                'percentage': round(percentage, 2)
            })
    
    return jsonify(chart_data), 200
