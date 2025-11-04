import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    
    data = {
        'midterm1': np.random.randint(40, 100, n_samples),
        'midterm2': np.random.randint(40, 100, n_samples),
        'assignments': np.random.randint(50, 100, n_samples),
        'attendance_pct': np.random.randint(60, 100, n_samples),
        'quizzes': np.random.randint(40, 100, n_samples),
    }
    
    data['final_exam'] = (
        data['midterm1'] * 0.25 +
        data['midterm2'] * 0.25 +
        data['assignments'] * 0.20 +
        data['attendance_pct'] * 0.10 +
        data['quizzes'] * 0.20 +
        np.random.normal(0, 5, n_samples)
    )
    
    data['final_exam'] = np.clip(data['final_exam'], 0, 100)
    
    df = pd.DataFrame(data)
    return df

def train_grade_prediction_model():
    print("Generating synthetic training data...")
    df = generate_synthetic_data(1000)
    
    df.to_csv('ml/training_data.csv', index=False)
    print(f"Training data saved to ml/training_data.csv")
    
    X = df[['midterm1', 'midterm2', 'assignments', 'attendance_pct', 'quizzes']]
    y = df['final_exam']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\nTraining Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R² Score: {r2:.4f}")
    
    model_path = 'ml/grade_prediction_model.pkl'
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")
    
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    return model

if __name__ == '__main__':
    os.makedirs('ml', exist_ok=True)
    model = train_grade_prediction_model()
    print("\nModel training completed successfully!")
