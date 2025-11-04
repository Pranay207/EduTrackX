from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.database import db
from app.utils.ai_helpers import predict_grade, get_weak_subjects, generate_study_plan, chat_with_mentor
from app.utils.ocr_helper import extract_marks_from_image
import os

bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@bp.route('/predict-grade', methods=['POST'])
@jwt_required()
def predict_student_grade():
    user_id = get_jwt_identity()
    data = request.json
    
    subject_id = data.get('subject_id')
    marks = db.find('marks', {'user_id': user_id, 'subject_id': subject_id})
    
    if len(marks) < 2:
        return jsonify({'error': 'Need at least 2 marks entries for prediction'}), 400
    
    prediction = predict_grade(marks)
    
    return jsonify({
        'predicted_grade': prediction['grade'],
        'predicted_percentage': prediction['percentage'],
        'confidence': prediction['confidence']
    }), 200

@bp.route('/weak-subjects', methods=['GET'])
@jwt_required()
def get_weak_subjects_api():
    user_id = get_jwt_identity()
    
    subjects = db.find('subjects', {'user_id': user_id})
    all_marks = db.find('marks', {'user_id': user_id})
    
    weak_subjects = get_weak_subjects(subjects, all_marks)
    
    return jsonify(weak_subjects), 200

@bp.route('/study-plan', methods=['POST'])
@jwt_required()
def generate_study_plan_api():
    user_id = get_jwt_identity()
    data = request.json
    
    subjects = db.find('subjects', {'user_id': user_id})
    marks = db.find('marks', {'user_id': user_id})
    assignments = db.find('assignments', {'user_id': user_id})
    
    study_plan = generate_study_plan(subjects, marks, assignments, data.get('days', 7))
    
    return jsonify(study_plan), 200

@bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    response = chat_with_mentor(question)
    
    return jsonify({'response': response}), 200

@bp.route('/ocr-marks', methods=['POST'])
@jwt_required()
def ocr_marks():
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    
    try:
        extracted_data = extract_marks_from_image(file_path)
        os.remove(file_path)
        
        return jsonify({
            'message': 'Marks extracted successfully',
            'data': extracted_data
        }), 200
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': str(e)}), 500

@bp.route('/insights', methods=['GET'])
@jwt_required()
def get_insights():
    user_id = get_jwt_identity()
    
    subjects = db.find('subjects', {'user_id': user_id})
    marks = db.find('marks', {'user_id': user_id})
    
    insights = []
    
    for subject in subjects:
        subject_marks = [m for m in marks if m['subject_id'] == subject['_id']]
        
        if len(subject_marks) >= 2:
            recent = subject_marks[-1]['percentage']
            previous = subject_marks[-2]['percentage']
            
            if recent > previous:
                insights.append(f"Great improvement in {subject['name']}! Keep it up!")
            elif recent < previous:
                insights.append(f"Your performance in {subject['name']} declined. Review the concepts.")
            else:
                insights.append(f"Steady performance in {subject['name']}.")
    
    if not insights:
        insights.append("Add more marks to get personalized insights!")
    
    return jsonify(insights), 200
