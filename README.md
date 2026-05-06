📘 EduPredict – Student Performance Prediction System
🚀 Overview

EduPredict is a machine learning-based web application designed to predict student performance based on various academic and behavioral factors such as study hours, attendance, participation, and previous scores.

The system uses multiple ML models, compares their performance, and selects the most accurate one to generate predictions. It also provides analytics and improvement suggestions.

🎯 Features
📊 Predict student exam scores using ML models
🤖 Multiple model comparison (Linear, Tree, RF, Gradient Boosting)
📈 Performance evaluation (MAE, RMSE, R²)
📉 Analytics dashboard for insights
💡 Suggestion system for performance improvement
🌐 Flask-based API backend
🧩 Modular and scalable architecture
🏗️ Project Structure
EduPredict/
│
├── app/                    # Flask backend
│   ├── app.py              # Main API routes
│   └── static/             # Frontend files
│
├── src/                    # Core ML pipeline
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── predict.py
│   ├── analytics.py
│   ├── suggestion.py
│   └── security.py
│
├── data/                   # Dataset files
│   ├── student_dataset.csv
│   ├── student_dataset_cleaned.csv
│   └── student_dataset_featured.csv
│
├── models/                 # Trained models (.pkl)
│
├── outputs/                # Results & logs
│
├── notebooks/              # EDA & experimentation
│
├── run.py                  # Entry point
└── README.md
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone <repo-url>
cd EduPredict
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run the application
python run.py
🌐 API Endpoints
Method	Endpoint	Description
POST	/api/login	User authentication
POST	/api/predict	Predict student score
GET	/api/analytics	Dashboard data
GET	/api/students	Student list
GET	/api/model-info	Model comparison
🤖 Machine Learning Models Used
Linear Regression
Decision Tree
Random Forest
Gradient Boosting (Best Performing)
📊 Evaluation Metrics
MAE (Mean Absolute Error)
RMSE (Root Mean Squared Error)
R² Score (Accuracy Measure)
🔄 Data Pipeline
Raw Data
   ↓
Data Preprocessing
   ↓
Feature Engineering
   ↓
Model Training
   ↓
Evaluation
   ↓
Prediction
🧠 How Prediction Works
User inputs student details
Data is preprocessed
Features are engineered
Best trained model is applied
Predicted score is returned
💡 Suggestions System

The system provides improvement suggestions based on:

Attendance
Study hours
Participation level
Submission behavior

(Currently rule-based)

📌 Future Improvements
🔄 Replace rule-based suggestions with ML-based recommendations
🗄️ Integrate database (MySQL / MongoDB)
🎨 Improve frontend UI
🔐 Enhance authentication & security
☁️ Deploy on cloud (AWS / Render)
🧑‍💻 Author

Developed as a Machine Learning Project for academic and practical implementation.

📜 License

This project is for educational purposes.