#🎓 EduPredict — Student Performance Predictive Analyzer

Python Flask Scikit-learn

EduPredict is a full-stack Machine Learning project that predicts student exam scores using a variety of machine learning models, including Linear Regression, Decision Tree, Random Forest, and Gradient Boosting. The project also features a live dashboard, REST API, and integrated cybersecurity layer.

#📁 Project Structure
EduPredict/
├── run.py                           ← Master launcher (run this!)
├── requirements.txt
├── README.md
│
├── data/
│   ├── Data.py                      ← Synthetic dataset generator
│   ├── misssing_data.py             ← Missing-value injector
│   ├── student_dataset.csv          ← Main dataset (30,000 students × 6 months)
│   ├── student_dataset_missing.csv  ← Dataset with injected missing values
│   ├── student_dataset_cleaned.csv  ← Post-preprocessing
│   ├── student_dataset_featured.csv ← ML-ready (encoded + engineered features)
│   └── students_summary.json        ← Pre-computed per-student profiles
│
├── models/
│   └── trained_model_linear.pkl     ← Best model (Linear Regression, R²=0.9309)
│   ├── trained_model_Gradient.pkl  ← Gradient Boosting 
│   ├── trained_model_random.pkl    ← Random Forest
│   ├── trained_model_decision.pkl  ← Decision Tree 
│
├── src/
│   ├── data_preprocessing.py        ← Cleans & imputes missing values
│   ├── feature_engineering.py       ← Encodes categoricals + engineered features
│   ├── train_model.py               ← Trains 4 models, saves best by R²
│   ├── evaluate_model.py            ← Metrics report + residual plots
│   ├── predict.py                   ← Single-student inference function
│   ├── analytics.py                 ← Dashboard data aggregations
│   ├── suggestion.py                ← Smart improvement-tip engine
│   └── security.py                  ← 🔐 Cybersecurity middleware
│
├── app/
│   ├── app.py                       ← Flask backend (8 REST endpoints)
│   └── static/index.html            ← Full SPA dashboard (6 tabs)
│
├── notebooks/
│   ├── EDA.ipynb                    ← Exploratory Data Analysis
│   └── model_training.ipynb         ← Model training notebook
│
└── outputs/
    ├── model_comparison.json        ← R², MAE, RMSE for all 4 models
    ├── audit.log                    ← Security event log (auto-generated)
    └── graphs/evaluation_plot.png   ← Actual vs Predicted + Residual plots
    
#🚀 Quick Start
1. Install dependencies
pip install -r requirements.txt
2. Launch everything
python run.py
3. Open browser → http://127.0.0.1:5000

Flags: --retrain to force re-training · --port 8080 to use a custom port

#🤖 ML Pipeline
Step	Script	Description
1	data/misssing_data.py	Injects missing values into raw dataset
2	src/data_preprocessing.py	Fills missing values per student
3	src/feature_engineering.py	Encodes categoricals + 4 composite features
4	src/train_model.py	Trains 4 models, saves best by R²
5	src/evaluate_model.py	Generates metrics + residual plots
6	src/predict.py	Exposes predict_exam_score() for the API

Engineered Features
Feature	Formula
engagement_feature	(Attendance_scaled + Participation) / 2
risk_feature	Backlogs_scaled − Previous_Scores_scaled
balance_feature	(Hours_Studied_scaled + Submission_Timeliness) / 2
activeness_feature	(Participation + Extra_C) / 2
Model Results (1,80,000 records · 70/30 split)
Model	R²	MAE	RMSE
⭐ Linear Regression	0.9309	2.5331	3.0947
Gradient Boosting	0.9532	2.1466	2.5463
Random Forest	0.8919	3.1352	3.8703
Decision Tree	0.7072	5.0844	6.3694
🏆 BEST MODEL

Gradient Boosting is the best performing model

R² Score : 0.9532
RMSE : 2.5463
MAE : 2.1466

#🌐 API Endpoints
Method	Route	Description
POST	/api/login	Authenticate → receive HMAC token
GET	/api/analytics	Aggregated dashboard statistics
POST	/api/predict	Predict exam score for a student
GET	/api/students	Paginated list (search / filter / sort)
GET	/api/student/<id>	Single student profile + monthly records
GET	/api/model-info	Model comparison results
GET	/api/security	Security event log & threat stats
GET	/api/health	Server health check

#🔐 Cybersecurity Features
Feature	Implementation
Rate Limiting	60 req/min per IP — returns HTTP 429 on breach
XSS Protection	Blocks <script>, onerror=, eval(), <iframe>
SQL Injection Guard	Blocks SELECT, UNION, DROP, --, # patterns
HMAC Token Auth	SHA-256 signed, Base64url encoded, 8-hour expiry
Audit Logging	All events logged to outputs/audit.log with IP + timestamp
Input Validation	Allowlist categoricals + numeric range clamping

Demo credentials:

teacher / teacher123
admin / admin2024
viewer / view123
📊 Dashboard Tabs
#	Tab	What's Inside
1	Dashboard	Stat cards, monthly trend, score distribution, grade doughnut, top 5
2	Predict Score	Sliders → ML prediction → score ring + breakdown + improvement tips
3	Students	30,000 students — search, filter by grade/risk, sort, paginate, profile modal
4	Analytics	Submission, extra-curricular, hours vs score, monthly area charts
5	ML Model	Model comparison bars, pipeline view, feature importance
6	Security	Live event feed, threat level, HMAC demo, XSS/rate-limit simulation

#🧰 Tech Stack
Backend: Python · Flask · Scikit-learn · Pandas · NumPy · Joblib · Faker · Matplotlib
Frontend: HTML · CSS · JavaScript · Chart.js
---

