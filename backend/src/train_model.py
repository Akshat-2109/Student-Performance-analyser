"""
train_model.py
Trains 4 ML models, compares them, saves the best by R2 score.
Run: python src/train_model.py
"""
import os, sys, json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEATURE_COLS = [
    'Hours_Studied', 'Attendance', 'Previous_Scores', 'Test_Score',
    'Project_Marks', 'Submission_Timeliness', 'Participation',
    'Extra_C', 'Backlogs',
    'engagement_feature', 'risk_feature', 'balance_feature', 'activeness_feature'
]


def train():
    featured_path = os.path.join(BASE_DIR, 'data', 'student_dataset_featured.csv')
    if not os.path.exists(featured_path):
        print("Featured dataset not found. Running feature engineering first...")
        sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
        from feature_engineering import feature_engineering
        raw = os.path.join(BASE_DIR, 'data', 'student_dataset.csv')
        feature_engineering(raw, featured_path)

    df = pd.read_csv(featured_path)
    print(f"Featured data loaded: {df.shape}")

    X = df[FEATURE_COLS]
    y = df['Exam_Score']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)
    print(f"Train: {len(X_train)}   Test: {len(X_test)}")

    models = {
        "Linear Regression":  LinearRegression(),
        "Decision Tree":      DecisionTreeRegressor(random_state=42),
        "Random Forest":      RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "Gradient Boosting":  GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42),
    }

    results = []
    trained = {}
    for name, mdl in models.items():
        mdl.fit(X_train, y_train)
        # ✅ Clip predictions to 0-100 (same as evaluate_model.py)
        pred = np.clip(mdl.predict(X_test), 0, 100)
        mae  = round(float(mean_absolute_error(y_test, pred)), 4)
        rmse = round(float(mean_squared_error(y_test, pred) ** 0.5), 4)
        r2   = round(float(r2_score(y_test, pred)), 4)
        results.append({"model": name, "MAE": mae, "RMSE": rmse, "R2": r2})
        trained[name] = mdl
        print(f"  {name:25s}  MAE={mae}  RMSE={rmse}  R2={r2}")

    results_df = pd.DataFrame(results).sort_values('R2', ascending=False)

    best_name = results_df.iloc[0]['model']
    best_mdl  = trained[best_name]

    # Save every model to its own dedicated file
    name_to_file = {
        'Linear Regression': 'trained_model_linear.pkl',
        'Decision Tree':     'trained_model_decision.pkl',
        'Random Forest':     'trained_model_random.pkl',
        'Gradient Boosting': 'trained_model_gradient.pkl',
    }
    for mname, mdl in trained.items():
        fname = name_to_file.get(mname)
        if fname:
            joblib.dump(mdl, os.path.join(BASE_DIR, 'models', fname))
            print(f"  Saved {mname} → models/{fname}")

    print(f"\nBest model: '{best_name}' (R²={results_df.iloc[0]['R2']})")

    out_json = os.path.join(BASE_DIR, 'outputs', 'model_comparison.json')
    with open(out_json, 'w') as f:
        json.dump({"best_model": best_name, "results": results_df.to_dict(orient='records')}, f, indent=2)
    print(f"Model comparison saved to {out_json}")
    return best_name, results


if __name__ == '__main__':
    train()
