import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import joblib
import os

def predict_grade(marks_history):
    if len(marks_history) < 2:
        return {
            'grade': 'N/A',
            'percentage': 0,
            'confidence': 0
        }
    
    X = np.array([[i] for i in range(len(marks_history))])
    y = np.array([m['percentage'] for m in marks_history])
    
    model = LinearRegression()
    model.fit(X, y)
    
    next_index = len(marks_history)
    predicted_percentage = model.predict([[next_index]])[0]
    
    predicted_percentage = max(0, min(100, predicted_percentage))
    
    if predicted_percentage >= 90:
        grade = 'A+'
    elif predicted_percentage >= 80:
        grade = 'A'
    elif predicted_percentage >= 70:
        grade = 'B'
    elif predicted_percentage >= 60:
        grade = 'C'
    elif predicted_percentage >= 50:
        grade = 'D'
    else:
        grade = 'F'
    
    confidence = min(len(marks_history) * 15, 95)
    
    return {
        'grade': grade,
        'percentage': round(predicted_percentage, 2),
        'confidence': confidence
    }

def get_weak_subjects(subjects, all_marks):
    weak_subjects = []
    
    for subject in subjects:
        subject_marks = [m for m in all_marks if m['subject_id'] == subject['_id']]
        
        if subject_marks:
            avg_percentage = sum(m['percentage'] for m in subject_marks) / len(subject_marks)
            
            if avg_percentage < 60:
                weak_subjects.append({
                    'subject_id': subject['_id'],
                    'subject_name': subject['name'],
                    'average_percentage': round(avg_percentage, 2),
                    'recommendation': 'Focus on this subject. Review past topics and practice more.'
                })
    
    weak_subjects.sort(key=lambda x: x['average_percentage'])
    
    return weak_subjects

def generate_study_plan(subjects, marks, assignments, days=7):
    plan = {}
    
    weak_subjects_list = get_weak_subjects(subjects, marks)
    pending_assignments = [a for a in assignments if a['status'] != 'completed']
    
    weak_subject_ids = [ws['subject_id'] for ws in weak_subjects_list[:3]]
    
    subjects_to_study = []
    for subject in subjects:
        if subject['_id'] in weak_subject_ids:
            subjects_to_study.append({
                'subject': subject['name'],
                'priority': 'high',
                'reason': 'Weak performance'
            })
    
    for assignment in pending_assignments[:3]:
        subject = next((s for s in subjects if s['_id'] == assignment['subject_id']), None)
        if subject:
            deadline = datetime.fromisoformat(assignment['deadline'].replace('Z', '+00:00')) if assignment.get('deadline') else None
            if deadline and deadline < datetime.now() + timedelta(days=days):
                subjects_to_study.append({
                    'subject': subject['name'],
                    'priority': 'urgent',
                    'reason': f"Assignment: {assignment['title']} due soon",
                    'deadline': assignment['deadline']
                })
    
    for i in range(days):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        daily_tasks = []
        
        if i < len(subjects_to_study):
            daily_tasks.append(subjects_to_study[i])
        
        if len(subjects) > 0:
            regular_subject = subjects[i % len(subjects)]
            daily_tasks.append({
                'subject': regular_subject['name'],
                'priority': 'medium',
                'reason': 'Regular revision',
                'duration': '25 minutes (1 Pomodoro)'
            })
        
        plan[date] = daily_tasks
    
    return plan

def chat_with_mentor(question):
    responses = {
        'what is python': 'Python is a high-level programming language known for its simplicity and readability. It is widely used in web development, data science, machine learning, and automation.',
        'how to study': 'Effective study techniques include: 1) Use the Pomodoro technique (25 min study, 5 min break), 2) Practice active recall, 3) Teach concepts to others, 4) Make summary notes, 5) Take regular breaks.',
        'time management': 'Good time management tips: 1) Prioritize tasks using Eisenhower Matrix, 2) Set specific goals, 3) Use time blocking, 4) Avoid multitasking, 5) Track your study hours.',
        'exam preparation': 'For effective exam preparation: 1) Start early, 2) Create a study schedule, 3) Practice with past papers, 4) Form study groups, 5) Get enough sleep before exams.',
        'motivation': 'Stay motivated by: 1) Setting clear goals, 2) Rewarding yourself for achievements, 3) Visualizing success, 4) Breaking tasks into smaller steps, 5) Finding a study buddy.',
    }
    
    question_lower = question.lower()
    
    for key, response in responses.items():
        if key in question_lower:
            return response
    
    return "I'm here to help you with your studies! You can ask me about study techniques, time management, specific subjects, or exam preparation. What would you like to know?"
