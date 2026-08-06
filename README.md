# EduPredict — Student Performance Analyser

A full-stack ML dashboard that predicts exam scores, flags at-risk students,
and surfaces cohort-wide analytics from 180k+ student records — with a
security layer (rate limiting, input sanitization, HMAC token auth, audit
logging) built in.

**Live architecture:** Flask API backend (deployed on **Render**) + a static
HTML/CSS/JS dashboard (deployed on **Vercel**) that talks to it over a JSON API.

---

## Project Structure

```
EduPredict/
├── backend/                       # Flask API + ML — deploy this on Render
│   ├── run.py                      # Entry point: builds features/model if missing, then launches Flask
│   ├── requirements.txt
│   ├── Procfile                    # web: gunicorn run:app --bind 0.0.0.0:$PORT
│   ├── render.yaml                 # Render blueprint (optional one-click deploy)
│   │
│   ├── app/
│   │   └── app.py                  # Flask app + all /api/* routes (API-only now)
│   │
│   ├── src/
│   │   ├── predict.py               # Loads best trained model, runs predictions
│   │   ├── analytics.py             # Cohort-wide analytics (grade dist, trends, etc.)
│   │   ├── suggestion.py            # Generates improvement tips per prediction
│   │   ├── security.py              # Rate limiting, input validation, HMAC tokens, audit log
│   │   ├── data_preprocessing.py
│   │   ├── feature_engineering.py
│   │   ├── train_model.py           # Trains Linear/Gradient Boosting/Random Forest/Decision Tree
│   │   └── evaluate_model.py
│   │
│   ├── models/                     # trained_model_*.pkl (4 models)
│   ├── data/                       # student_dataset*.csv, students_summary.json
│   └── outputs/                    # model_comparison.json, audit.log, graphs/
│
├── frontend/                      # Static dashboard — deploy this on Vercel
│   ├── index.html                  # Single-file dashboard (charts, predictor, student table)
│   ├── config.js                   # Sets window.API_BASE_URL (backend URL)
│   └── vercel.json
│
└── README.md
```

---

## How it works

- **Prediction:** `src/predict.py` loads whichever model won during training
  (per `outputs/model_comparison.json`), from Linear Regression, Gradient
  Boosting, Random Forest, or Decision Tree — all four are shipped in
  `models/`.
- **Security layer:** `src/security.py` rate-limits API calls, sanitizes
  input against XSS/SQL-injection patterns, validates ranges on every
  `/api/predict` field, and logs every request to `outputs/audit.log`.
  `/api/login` issues a demo HMAC-SHA256 token (`teacher`/`admin`/`viewer`
  demo accounts) — this is a stateless token, not a cookie, so no
  cross-origin cookie configuration is needed.
- **Analytics:** `src/analytics.py` computes grade distribution, monthly
  trends, and hours-vs-score correlations directly from the 180k-row CSV
  using vectorized pandas.

---

## Local Setup (VS Code)

Backend and frontend run as two separate processes locally, same as in production.

### 1. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python run.py
```
Runs at **http://127.0.0.1:5000**. Visiting it in a browser should show:
```json
{"status": "ok", "service": "EduPredict backend"}
```

### 2. Frontend
In `frontend/config.js`, point it at your local backend:
```js
window.API_BASE_URL = "http://127.0.0.1:5000";
```
Then open `frontend/index.html` with the VS Code **Live Server** extension
(right-click → *Open with Live Server*), or:
```bash
cd frontend
python -m http.server 5500
```
Open **http://127.0.0.1:5500** — the dashboard, predictor, and student table
should all load live data from your local backend.

**Remember:** before deploying, change `config.js` back to your live Render URL.

> This app uses stateless token-based login (not cookies), so — unlike
> cookie-based apps — you do **not** need to worry about `localhost` vs
> `127.0.0.1` matching between frontend and backend here.

### Retraining the model (optional)
```bash
cd backend
python run.py --retrain
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/login` | Demo login → HMAC token (`teacher`/`teacher123`, `admin`/`admin2024`, `viewer`/`view123`) |
| GET | `/api/analytics` | Dashboard-wide stats (grade distribution, trends) |
| POST | `/api/predict` | Predict exam score from student inputs |
| GET | `/api/students` | Paginated/searchable/sortable student list |
| GET | `/api/student/<id>` | Single student detail + monthly records |
| GET | `/api/model-info` | Model comparison results (accuracy of all 4 models) |
| GET | `/api/security` | Security/audit event log |
| GET | `/api/health` | Health check |

---

## Deployment

### Backend → Render

1. Push this repo to GitHub (keep `backend/` and `frontend/` as top-level folders).
2. On Render: **New → Web Service** → connect the repo.
3. **Root Directory:** `backend`
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `gunicorn run:app --bind 0.0.0.0:$PORT` (auto-detected from `Procfile`, or use `render.yaml` for one-click)
6. Deploy → note the public URL, e.g. `https://edupredict-backend.onrender.com`

### Frontend → Vercel

1. Update `frontend/config.js`:
   ```js
   window.API_BASE_URL = "https://edupredict-backend.onrender.com";
   ```
   Commit and push.
2. On Vercel: **Add New → Project** → import the same repo.
3. **Root Directory:** `frontend`
4. **Framework Preset:** Other (no build step needed)
5. **Project Name** must be lowercase (letters, digits, `.`, `_`, `-` only) —
   if Vercel auto-fills an uppercase name, lowercase it before creating.
6. Deploy → note the public URL, e.g. `https://edupredict.vercel.app`

### Connect them (CORS)

On Render, open the backend service → **Environment** → add:
- **Key:** `FRONTEND_ORIGIN`
- **Value:** `https://edupredict.vercel.app` (your actual Vercel URL)

Save — Render redeploys automatically. (This app uses token-based auth, not
cookies, so `FRONTEND_ORIGIN=*` also works if you'd rather skip this step —
but restricting it to your exact frontend URL is better practice.)

> Render's free tier sleeps after 15 min of inactivity — the first request
> after that can take 30-50 seconds to wake up.

### Test
Open your Vercel URL — the dashboard should load analytics, and the predictor
and student table should both work end-to-end against the live backend.

---

## Restructure notes (what changed and why)

- Split the original single Flask app into an independently deployable
  **`backend/`** (Flask JSON API) and **`frontend/`** (static HTML/JS),
  so each can be deployed on the platform best suited for it (Render / Vercel).
- `app/app.py` no longer serves `static/index.html` — it's now a pure JSON
  API, with `FRONTEND_ORIGIN` driving CORS instead of a hardcoded `'*'`.
- `app/static/index.html` → `frontend/index.html`. The file already had a
  configurable `const API = ''` prefix used by every fetch call — only
  change needed was pointing it at `window.API_BASE_URL` from a new
  `frontend/config.js`, so the backend URL is a single editable setting.
- Added `Procfile` and `render.yaml` (`gunicorn run:app`), matching the
  gunicorn-aware comments already present in `run.py`.

**Nothing about how predictions, analytics, or security logic work
changed** — same models, same routes, same responses. Only file locations
and deployment plumbing.

---

## Tech Stack

- **Backend:** Python, Flask, Flask-CORS, scikit-learn, pandas, joblib, gunicorn
- **Frontend:** HTML/CSS/vanilla JS single-page dashboard (no build step required)
- **Models:** Linear Regression, Gradient Boosting, Random Forest, Decision Tree — best one auto-selected
- **Hosting:** Render (backend API) + Vercel (frontend static site)
