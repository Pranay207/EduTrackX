from flask import Blueprint, send_file, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.database import db
from app.utils.pdf_generator import generate_report_card
import os

bp = Blueprint('export', __name__, url_prefix='/api/export')

@bp.route('/report-card', methods=['GET'])
@jwt_required()
def export_report_card():
    user_id = get_jwt_identity()
    
    user = db.find_one('users', {'_id': user_id})
    subjects = db.find('subjects', {'user_id': user_id})
    marks = db.find('marks', {'user_id': user_id})
    attendance = db.find('attendance', {'user_id': user_id})
    
    pdf_path = generate_report_card(user, subjects, marks, attendance)
    
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name='report_card.pdf')
    else:
        return jsonify({'error': 'Failed to generate report card'}), 500
