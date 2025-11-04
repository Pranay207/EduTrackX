# EduTrackX Demo Script

This guide walks you through demonstrating all features of EduTrackX.

## Demo Flow (10-15 minutes)

### 1. Introduction (1 minute)
"EduTrackX is an AI-powered academic dashboard that helps students track their performance, predict grades, and optimize their study schedules. Let me show you how it works."

### 2. Authentication (30 seconds)
1. Open the application
2. Click "Sign Up"
3. Create a demo account:
   - Name: Demo Student
   - Email: demo@edutrackx.com
   - Password: demo123
4. Successfully log in

### 3. Dashboard Overview (1 minute)
"This is the main dashboard where students see everything at a glance."

Point out:
- Total subjects counter
- Average performance percentage
- Current CGPA
- Pending assignments
- Attendance percentage
- Total study time
- XP points and level (gamification)
- Performance charts
- Attendance visualization
- Upcoming deadlines

### 4. Adding Subjects (2 minutes)
1. Navigate to "Subjects & Marks"
2. Click "Add Subject"
3. Add first subject:
   - Name: Data Structures
   - Code: CS201
   - Credits: 4
   - Professor: Dr. Smith
   - Color: Blue
4. Add more subjects quickly:
   - Database Systems (CS301)
   - Web Development (CS302)
   - Mathematics (MATH201)

### 5. Adding Marks (2 minutes)
1. Click on "Data Structures" subject
2. Add marks:
   - Exam Type: Midterm 1
   - Marks Obtained: 85
   - Total Marks: 100
3. Add more marks for variety:
   - Midterm 2: 88/100
   - Quiz 1: 45/50
4. Show how XP increases with each entry
5. Return to dashboard to see updated charts

### 6. Assignments Management (2 minutes)
1. Navigate to "Assignments"
2. Click "Add Assignment"
3. Create assignment:
   - Subject: Data Structures
   - Title: Implement Binary Search Tree
   - Description: Create BST with insert, delete, search
   - Deadline: [Tomorrow's date]
   - Priority: High
4. Add another assignment:
   - Subject: Database Systems
   - Title: Design ER Diagram for Library System
   - Deadline: [Next week]
   - Priority: Medium
5. Show how to mark assignments as complete (checkbox)
6. Demonstrate priority badges and deadline tracking

### 7. Attendance Tracking (1 minute)
1. Navigate to "Attendance"
2. Mark attendance for today:
   - Subject: Data Structures
   - Date: Today
   - Status: Present
3. Add a few more records with mix of present/absent
4. Return to dashboard to see attendance chart update

### 8. Study Planner with Pomodoro (2 minutes)
1. Navigate to "Study Planner"
2. Explain Pomodoro Technique:
   - 25 minutes focused study
   - 5-minute break
3. Select subject: Web Development
4. Click "Start" to begin timer
5. Show timer countdown
6. Explain that completion adds XP and tracks study time
7. (Optional: Let it run briefly, then reset)

### 9. AI Features (3 minutes)

**AI Study Assistant:**
1. Navigate to "AI Assistant"
2. Ask questions:
   - "How should I study for exams?"
   - "What is time management?"
   - "How to prepare for exams?"
3. Show AI responses

**AI Insights:**
1. Return to Dashboard
2. Point out AI-generated insights (if available):
   - Performance improvement notifications
   - Weak subject warnings
   - Study recommendations

**Grade Prediction (Demo in backend):**
- Explain: "The system uses Machine Learning to predict your final grades"
- Show: Based on Midterm 1, Midterm 2, attendance, the AI predicts final exam performance
- Model: Random Forest with 64% accuracy

**Weak Subject Detection:**
- System automatically identifies subjects with low performance
- Provides targeted study recommendations

### 10. Gamification Features (1 minute)
Point out gamification elements:
- XP points earned for:
  - Adding marks (+10 XP)
  - Completing assignments (+25 XP)
  - Study sessions (based on duration)
- Level system (increases with XP)
- Streak counter (consecutive days of activity)
- Profile badges (future feature)

### 11. Profile & Export (1 minute)
1. Navigate to "Profile"
2. Show user information:
   - Name and email
   - Current level
   - Total XP
   - Streak days
3. Click "Export Report Card (PDF)"
4. PDF downloads with:
   - Student information
   - All subjects with performance
   - Attendance statistics
   - Overall GPA/CGPA

### 12. Dark Mode (30 seconds)
1. Click moon icon in sidebar
2. Toggle to dark mode
3. Show how entire UI adapts
4. Toggle back to light mode

## Advanced Features to Mention

### OCR Marks Upload (Not in basic demo)
"Students can upload photos of their mark sheets, and the system automatically extracts marks using OCR technology."

### Study Plan Generation
"The AI can generate personalized weekly study plans based on:
- Weak subjects
- Upcoming deadlines
- Past performance
- Available study time"

### Real-time Notifications
"Students receive notifications for:
- Upcoming assignment deadlines
- Low attendance warnings
- Performance alerts"

## Technical Highlights

### For Technical Audience:
1. **Full-Stack Architecture**:
   - React + Vite frontend
   - Flask Python backend
   - RESTful API design

2. **AI/ML Integration**:
   - Random Forest for grade prediction
   - Tesseract OCR for mark extraction
   - Custom recommendation engine

3. **Modern UI/UX**:
   - Tailwind CSS for styling
   - Chart.js for visualizations
   - Responsive design
   - Dark mode support

4. **Security**:
   - JWT authentication
   - Password hashing with bcrypt
   - CORS protection

## Common Questions & Answers

**Q: Can multiple students use this?**
A: Yes! Each student has their own account with isolated data.

**Q: Does it work offline?**
A: Currently requires internet. PWA offline support is planned.

**Q: Can teachers/parents access this?**
A: Currently student-only. Parent dashboard is in development.

**Q: What about mobile apps?**
A: The web app is fully responsive. Native mobile apps are planned.

**Q: Is the data secure?**
A: Yes, passwords are hashed, and authentication uses JWT tokens.

**Q: Can I integrate with Google Calendar?**
A: This is a planned feature for future releases.

## Conclusion

"EduTrackX combines traditional academic tracking with modern AI to help students:
- Stay organized with assignments and deadlines
- Track their academic progress visually
- Get personalized study recommendations
- Predict and improve their performance
- Stay motivated through gamification

All in one beautiful, easy-to-use dashboard."

## Quick Reset for Multiple Demos

To reset the demo:
1. Logout
2. Create new account with different email
3. Or manually delete `database.json` in backend folder

## Troubleshooting

- **Charts not showing**: Add more data (subjects, marks, attendance)
- **Backend not responding**: Check that Flask server is running on port 5001
- **Frontend not loading**: Ensure Vite dev server is on port 5000
- **Dark mode not persisting**: It's stored in localStorage per browser

---

**Demo Duration**: 10-15 minutes
**Preparation Time**: 2 minutes
**Best For**: Students, educators, investors, or technical reviewers
