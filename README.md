# EduPredict — Student Performance Analyser

A full-stack machine learning dashboard that predicts student exam scores, flags at-risk students, and surfaces cohort-wide analytics from 180,000+ student records. Includes a built-in security layer with rate limiting, input sanitization, HMAC token authentication, and audit logging.

## Features

- Exam score prediction using the best of four trained ML models
- Cohort-wide analytics: grade distribution, monthly trends, hours-vs-score correlation
- Searchable, filterable, paginated student directory
- Individual student detail view with monthly performance records
- Security dashboard: rate limiting, audit log, HMAC-signed token demo login
- Model comparison view across Linear Regression, Gradient Boosting, Random Forest, and Decision Tree

## Tech Stack

- **Backend:** Python, Flask, Flask-CORS, scikit-learn, pandas, joblib, gunicorn
- **Frontend:** HTML, CSS, vanilla JavaScript (single-page dashboard, no build step)
- **Models:** Linear Regression, Gradient Boosting, Random Forest, Decision Tree — best model auto-selected
- **Hosting:** Render (backend API) + Vercel (frontend)

## Project Structure

```
EduPredict/
├── backend/
│   ├── run.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── render.yaml
│   ├── app/
│   │   └── app.py
│   ├── src/
│   │   ├── predict.py
│   │   ├── analytics.py
│   │   ├── suggestion.py
│   │   ├── security.py
│   │   ├── data_preprocessing.py
│   │   ├── feature_engineering.py
│   │   ├── train_model.py
│   │   └── evaluate_model.py
│   ├── models/
│   ├── data/
│   └── outputs/
│
└── frontend/
    ├── index.html
    ├── config.js
    └── vercel.json
```

## Local Development

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
Runs at `http://127.0.0.1:5000`.

### Frontend
Set the backend URL in `frontend/config.js`:
```js
window.API_BASE_URL = "http://127.0.0.1:5000";
```
Serve `frontend/` with any static server (e.g. VS Code Live Server) and open it in the browser.

## Deployment

### Backend (Render)
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn run:app --bind 0.0.0.0:$PORT`
- Environment variable: `FRONTEND_ORIGIN` set to the deployed frontend URL

### Frontend (Vercel)
- Root Directory: `frontend`
- Framework Preset: Other
- `frontend/config.js` updated with the deployed backend URL

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/login` | Demo login, returns HMAC token |
| GET | `/api/analytics` | Dashboard-wide statistics |
| POST | `/api/predict` | Predict exam score from student inputs |
| GET | `/api/students` | Paginated, searchable, sortable student list |
| GET | `/api/student/<id>` | Single student detail with monthly records |
| GET | `/api/model-info` | Model comparison results |
| GET | `/api/security` | Security and audit event log |
| GET | `/api/health` | Health check |

## License

Private project.
