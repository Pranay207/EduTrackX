from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

def generate_report_card(user, subjects, marks, attendance):
    os.makedirs('reports', exist_ok=True)
    filename = f'reports/report_card_{user["_id"]}.pdf'
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1E40AF'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1E40AF'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    title = Paragraph("EduTrackX - Student Report Card", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    student_info = [
        ['Student Name:', user['name']],
        ['Email:', user['email']],
        ['Generated On:', datetime.now().strftime('%B %d, %Y')],
        ['Level:', f"Level {user.get('level', 1)}"],
        ['XP Points:', str(user.get('xp', 0))]
    ]
    
    info_table = Table(student_info, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    subject_heading = Paragraph("Academic Performance", heading_style)
    elements.append(subject_heading)
    
    subject_data = [['Subject', 'Average Marks', 'Attendance', 'Grade']]
    
    total_percentage = 0
    subject_count = 0
    
    for subject in subjects:
        subject_marks = [m for m in marks if m['subject_id'] == subject['_id']]
        subject_attendance = [a for a in attendance if a['subject_id'] == subject['_id']]
        
        if subject_marks:
            avg = sum(m['percentage'] for m in subject_marks) / len(subject_marks)
            total_percentage += avg
            subject_count += 1
        else:
            avg = 0
        
        if subject_attendance:
            present = len([a for a in subject_attendance if a['status'] == 'present'])
            attendance_pct = (present / len(subject_attendance)) * 100
        else:
            attendance_pct = 0
        
        grade = 'A+' if avg >= 90 else 'A' if avg >= 80 else 'B' if avg >= 70 else 'C' if avg >= 60 else 'D' if avg >= 50 else 'F'
        
        subject_data.append([
            subject['name'],
            f"{avg:.2f}%",
            f"{attendance_pct:.2f}%",
            grade
        ])
    
    subject_table = Table(subject_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
    subject_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    elements.append(subject_table)
    elements.append(Spacer(1, 0.3*inch))
    
    if subject_count > 0:
        overall_avg = total_percentage / subject_count
        gpa = (overall_avg / 100) * 10
        
        summary_data = [
            ['Overall Average:', f"{overall_avg:.2f}%"],
            ['GPA:', f"{gpa:.2f}/10"],
            ['CGPA:', f"{gpa:.2f}/10"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 12),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1E40AF')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(summary_table)
    
    elements.append(Spacer(1, 0.5*inch))
    
    footer = Paragraph(
        "This is an auto-generated report from EduTrackX Academic Dashboard System",
        styles['Normal']
    )
    footer.alignment = TA_CENTER
    elements.append(footer)
    
    doc.build(elements)
    
    return filename
