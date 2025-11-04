import joblib
import numpy as np
import os

class GradePredictor:
    def __init__(self, model_path='ml/grade_prediction_model.pkl'):
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            print(f"Model not found at {model_path}. Please train the model first.")
            self.model = None
    
    def predict(self, midterm1, midterm2, assignments, attendance_pct, quizzes):
        if self.model is None:
            return None
        
        features = np.array([[midterm1, midterm2, assignments, attendance_pct, quizzes]])
        prediction = self.model.predict(features)[0]
        
        return {
            'predicted_score': round(prediction, 2),
            'grade': self._score_to_grade(prediction)
        }
    
    def _score_to_grade(self, score):
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'

if __name__ == '__main__':
    predictor = GradePredictor()
    
    if predictor.model:
        example_prediction = predictor.predict(
            midterm1=85,
            midterm2=88,
            assignments=90,
            attendance_pct=95,
            quizzes=87
        )
        print("\nExample Prediction:")
        print(f"Input: Midterm1=85, Midterm2=88, Assignments=90, Attendance=95%, Quizzes=87")
        print(f"Predicted Final Score: {example_prediction['predicted_score']}")
        print(f"Predicted Grade: {example_prediction['grade']}")
