# EduTrackX - AI-Powered Student Academic Dashboard

A comprehensive full-stack web application designed to help students track academic performance, predict results, plan study schedules, and receive AI-powered recommendations.

## Features

### Core Features
- **Student Authentication**: Secure JWT-based login and signup system
- **Subject & Marks Management**: Add, edit, and track subjects with marks entry (manual + OCR)
- **Assignment Tracking**: Manage assignments with deadlines, priorities, and progress tracking
- **Attendance Monitoring**: Track and visualize attendance for each subject
- **Study Time Logging**: Built-in Pomodoro timer for focused study sessions
- **Comprehensive Dashboard**: 
  - GPA/CGPA calculations
  - Subject-wise performance charts
  - Attendance graphs
  - Productivity statistics
  - Deadline reminders with progress bars

### AI-Powered Features
- **Grade Prediction**: ML model predicts future performance based on past marks
- **Weak Subject Detection**: Identifies subjects requiring more attention
- **Study Recommendations**: Generates personalized study plans and schedules
- **AI Study Mentor**: Interactive chatbot to answer academic questions
- **Performance Insights**: AI-generated insights on academic progress
- **OCR Marks Reader**: Extract marks from uploaded images/PDFs automatically
- **AI Timetable Planner**: Daily/weekly study schedule recommendations

### Additional Features
- **Gamification**: XP points, levels, streaks, and badges to motivate students
- **PDF Report Export**: Generate and download comprehensive report cards
- **Dark Mode**: Toggle between light and dark themes
- **Mobile Responsive**: Works seamlessly on all device sizes
- **Real-time Notifications**: Get alerts for upcoming deadlines

## Tech Stack

### Frontend
- **React 18** with Vite for fast development
- **Tailwind CSS** for modern, responsive UI
- **React Router** for navigation
- **Chart.js & Recharts** for data visualization
- **Axios** for API communication
- **Lucide React** for beautiful icons

### Backend
- **Python Flask** - RESTful API server
- **Flask-JWT-Extended** - Authentication
- **Flask-CORS** - Cross-origin resource sharing
- **JSON File Database** - Simple file-based data storage

### AI & ML
- **scikit-learn** - Machine learning models (Random Forest for grade prediction)
- **Pandas & NumPy** - Data processing
- **Tesseract OCR** - Text extraction from images
- **Custom AI helpers** - Study recommendations and chatbot

### Additional Tools
- **ReportLab** - PDF generation
- **Matplotlib & Seaborn** - Data visualization
- **Pillow** - Image processing

## Project Structure

```
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components (Dashboard, Subjects, etc.)
│   │   ├── context/        # React context (Auth)
│   │   ├── utils/          # Utility functions and API client
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Frontend dependencies
│   └── vite.config.js      # Vite configuration
│
├── backend/                 # Flask backend application
│   ├── app/
│   │   ├── routes/         # API route handlers
│   │   │   ├── auth.py     # Authentication routes
│   │   │   ├── subjects.py # Subject management
│   │   │   ├── assignments.py # Assignment tracking
│   │   │   ├── attendance.py  # Attendance management
│   │   │   ├── study.py    # Study session tracking
│   │   │   ├── ai.py       # AI features
│   │   │   ├── dashboard.py # Dashboard stats
│   │   │   └── export.py   # PDF export
│   │   ├── models/         # Data models
│   │   │   └── database.py # JSON file database
│   │   ├── utils/          # Utility modules
│   │   │   ├── ai_helpers.py    # AI/ML helpers
│   │   │   ├── ocr_helper.py    # OCR functionality
│   │   │   └── pdf_generator.py # PDF report generation
│   │   └── __init__.py     # App factory
│   ├── ml/                 # Machine learning models
│   │   ├── train_model.py  # Model training script
│   │   └── predict.py      # Prediction utilities
│   ├── run.py              # Flask app entry point
│   └── requirements.txt    # Python dependencies
│
├── docs/                    # Documentation (diagrams, reports)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 20+
- Tesseract OCR (for image processing)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Train the ML model (optional, already trained):
```bash
python ml/train_model.py
```

5. Run the Flask server:
```bash
python run.py
```

The backend will run on `http://localhost:5001`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5000`

### Running Both Together

You can use the provided startup script:
```bash
chmod +x start.sh
./start.sh
```

Or run the workflow directly in Replit.

## Usage Guide

### Getting Started

1. **Sign Up / Login**: Create an account or login with existing credentials
2. **Add Subjects**: Navigate to "Subjects & Marks" and add your subjects
3. **Track Assignments**: Add assignments with deadlines in the "Assignments" section
4. **Mark Attendance**: Record your attendance daily
5. **Study with Pomodoro**: Use the Study Planner for focused study sessions
6. **Chat with AI**: Ask questions to the AI Study Assistant
7. **View Dashboard**: Monitor your overall performance and upcoming deadlines

### Key Workflows

**Adding Marks**:
1. Go to Subjects & Marks
2. Click on a subject
3. Add marks for different exams (midterm, final, quiz, etc.)
4. System automatically calculates percentages and GPA

**Using AI Features**:
- **Grade Prediction**: System predicts your final grade based on past performance
- **Weak Subjects**: View subjects that need more attention
- **Study Plan**: Get AI-generated weekly study schedules
- **OCR Upload**: Upload mark sheets to auto-extract marks

**Exporting Reports**:
1. Go to Profile
2. Click "Export Report Card"
3. PDF with all academic data will be downloaded

## API Documentation

### Authentication Endpoints

- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user details

### Subject Endpoints

- `GET /api/subjects` - Get all subjects
- `POST /api/subjects` - Create new subject
- `PUT /api/subjects/:id` - Update subject
- `DELETE /api/subjects/:id` - Delete subject
- `GET /api/subjects/:id/marks` - Get marks for subject
- `POST /api/subjects/:id/marks` - Add marks

### Dashboard Endpoints

- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/charts/performance` - Performance chart data
- `GET /api/dashboard/charts/attendance` - Attendance chart data

### AI Endpoints

- `POST /api/ai/predict-grade` - Predict student grade
- `GET /api/ai/weak-subjects` - Get weak subjects
- `POST /api/ai/study-plan` - Generate study plan
- `POST /api/ai/chat` - Chat with AI mentor
- `POST /api/ai/ocr-marks` - Extract marks from image
- `GET /api/ai/insights` - Get AI insights

## ML Model Details

The grade prediction model uses:
- **Algorithm**: Random Forest Regressor
- **Features**: 
  - Midterm 1 scores
  - Midterm 2 scores
  - Assignment grades
  - Attendance percentage
  - Quiz scores
- **Performance**: R² Score: 0.64, MSE: 28.03
- **Training Data**: 1000 synthetic student records

## Deployment

### Replit Deployment
This project is configured for easy deployment on Replit. Simply click the "Publish" button.

### Manual Deployment

1. Build the frontend:
```bash
cd frontend && npm run build
```

2. Use a production WSGI server for Flask:
```bash
cd backend && gunicorn -w 4 -b 0.0.0.0:5001 run:app
```

3. Serve frontend static files through a web server (nginx, apache)

## Environment Variables

### Backend (.env)
```
JWT_SECRET_KEY=your-secret-key
FLASK_ENV=development
PORT=5001
```

### Frontend
```
VITE_API_URL=http://localhost:5001/api
```

## Features in Development

- Email notifications for deadlines
- Integration with Google Calendar
- Advanced AI mentor with GPT integration
- Mobile app (React Native)
- Collaborative study groups
- Parent/teacher dashboard
- Advanced analytics and insights

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team

## Acknowledgments

- Built with modern web technologies
- Inspired by the need for better academic tracking tools
- AI-powered features to enhance student learning
- Gamification elements to increase engagement

---

**EduTrackX** - Empowering students to track, analyze, and improve their academic journey! 🚀📚
