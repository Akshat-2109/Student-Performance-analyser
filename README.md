# 📘 EduPredict – Student Performance Prediction System

## 🚀 Overview
EduPredict is a machine learning-based web application designed to predict student performance based on various academic and behavioral factors such as study hours, attendance, participation, and previous scores.

The system uses multiple ML models, compares their performance, and selects the most accurate one to generate predictions. It also provides analytics and improvement suggestions.

---

## 🎯 Features

- 📊 Predict student exam scores using ML models  
- 🤖 Multiple model comparison  
- 📈 Performance evaluation (MAE, RMSE, R²)  
- 📉 Analytics dashboard  
- 💡 Suggestion system for improvement  
- 🌐 Flask-based backend API  
- 🧩 Modular project structure  

---

## 🏗️ Project Structure

```
Student-Performance-analyser/
│
├── app/                # Flask backend
├── src/                # Core ML logic
├── data/               # Dataset files
├── models/             # Trained models
├── outputs/            # Results & logs
├── notebooks/          # EDA & experiments
├── run.py              # Entry point
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```
git clone https://github.com/Akshat-2109/Student-Performance-analyser.git
cd Student-Performance-analyser
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Run the project
```
python run.py
```

---

## 🌐 API Endpoints

- POST `/api/login` → User authentication  
- POST `/api/predict` → Predict student score  
- GET `/api/analytics` → Dashboard data  
- GET `/api/students` → Student list  
- GET `/api/model-info` → Model comparison  

---

## 🤖 Machine Learning Models Used

- Linear Regression  
- Decision Tree  
- Random Forest  
- Gradient Boosting (Best Performing)  

---

## 📊 Evaluation Metrics

- MAE (Mean Absolute Error)  
- RMSE (Root Mean Squared Error)  
- R² Score  

---

## 🔄 Data Pipeline

```
Raw Data → Data Cleaning → Feature Engineering → Model Training → Evaluation → Prediction
```

---

## 🧠 How Prediction Works

1. User inputs student data  
2. Data is preprocessed  
3. Features are engineered  
4. Model predicts score  
5. Result is returned  

---

## 💡 Suggestion System

The system provides improvement suggestions based on:
- Study hours  
- Attendance  
- Participation  
- Submission behavior  

(Currently rule-based)

---

## 📌 Future Improvements

- Add database integration  
- Improve UI/UX  
- Deploy on cloud  
- Replace rule-based suggestions with ML  

---

## 🧑‍💻 Author

Akshat Jain

---

## 📜 License

This project is for educational purposes.
