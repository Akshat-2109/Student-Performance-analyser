"""
predict.py
Loads trained model and predicts exam score for a student.
Feature engineering mirrors training pipeline exactly.
"""
import os
import pandas as pd
import joblib

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR  = os.path.join(BASE_DIR, 'models')

# Resolve the active model: prefer best-model JSON pointer, then fallback chain
def _resolve_model_path() -> str:
    import json
    comp_json = os.path.join(BASE_DIR, 'outputs', 'model_comparison.json')
    name_to_file = {
        'Linear Regression':  'trained_model_linear.pkl',
        'Gradient Boosting':  'trained_model_gradient.pkl',
        'Random Forest':      'trained_model_random.pkl',
        'Decision Tree':      'trained_model_decision.pkl',
    }
    # Try to read which model won
    if os.path.exists(comp_json):
        try:
            with open(comp_json) as f:
                data = json.load(f)
            best = data.get('best_model', '')
            fname = name_to_file.get(best)
            if fname:
                p = os.path.join(MODELS_DIR, fname)
                if os.path.exists(p):
                    return p
        except Exception:
            pass
    # Fallback chain — try each saved model in preference order
    for fname in ['trained_model_linear.pkl', 'trained_model_gradient.pkl',
                  'trained_model_random.pkl', 'trained_model_decision.pkl']:
        p = os.path.join(MODELS_DIR, fname)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(
        f"No trained model found in {MODELS_DIR}. Run train_model.py first."
    )

_model = None

def _load_model():
    global _model
    if _model is None:
        _model = joblib.load(_resolve_model_path())
    return _model


def map_categorical(submission, participation, extra_c, backlogs):
    sub_map = {'On time': 10, 'Late': 0, 'No Submission': -10}
    par_map = {'High': 10, 'Medium': 5, 'Low': 0}
    ext_map = {'Highly Active': 10, 'Active': 5, 'Inactive': 0}
    return (
        sub_map.get(submission, 0),
        par_map.get(participation, 0),
        ext_map.get(extra_c, 0),
        max(0, min(int(backlogs), 5))
    )


def compute_smart_features(df):
    df = df.copy()
    df['Hours_Studied_scaled']   = (df['Hours_Studied'] / 40 * 10).clip(0, 10).round(2)
    df['Attendance_scaled']      = (df['Attendance'] / 10).clip(0, 10).round(2)
    df['Previous_Scores_scaled'] = (df['Previous_Scores'] / 10).clip(0, 10).round(2)
    df['Backlogs_scaled']        = (df['Backlogs'] / 5 * 10).clip(0, 10).round(2)
    df['engagement_feature']     = ((df['Attendance_scaled'] + df['Participation']) / 2).round(2)
    df['risk_feature']           = (df['Backlogs_scaled'] - df['Previous_Scores_scaled']).round(2)
    df['balance_feature']        = ((df['Hours_Studied_scaled'] + df['Submission_Timeliness']) / 2).round(2)
    df['activeness_feature']     = ((df['Participation'] + df['Extra_C']) / 2).round(2)
    return df


FEATURE_COLS = [
    'Hours_Studied', 'Attendance', 'Previous_Scores', 'Test_Score',
    'Project_Marks', 'Submission_Timeliness', 'Participation',
    'Extra_C', 'Backlogs',
    'engagement_feature', 'risk_feature', 'balance_feature', 'activeness_feature'
]


def predict_exam_score(student_data: dict) -> float:
    sub_n, par_n, ext_n, bck_n = map_categorical(
        student_data.get('Submission_Timeliness', 'Late'),
        student_data.get('Participation', 'Medium'),
        student_data.get('Extra_C', 'Active'),
        student_data.get('Backlogs', 0)
    )
    row = pd.DataFrame([{
        'Hours_Studied':   max(5,  min(float(student_data.get('Hours_Studied', 20)),   40)),
        'Attendance':      max(0,  min(float(student_data.get('Attendance', 75)),      100)),
        'Submission_Timeliness': sub_n,
        'Participation':   par_n,
        'Extra_C':         ext_n,
        'Previous_Scores': max(40, min(float(student_data.get('Previous_Scores', 60)), 100)),
        'Test_Score':      max(10, min(float(student_data.get('Test_Score', 15)),       30)),
        'Project_Marks':   max(10, min(float(student_data.get('Project_Marks', 25)),   40)),
        'Backlogs':        bck_n,
    }])
    row  = compute_smart_features(row)
    pred = _load_model().predict(row[FEATURE_COLS])[0]
    return round(min(float(pred), 100), 2)


# if __name__ == '__main__':
#     sample = {
#         "Hours_Studied": 30, "Attendance": 85,
#         "Submission_Timeliness": "On time", "Participation": "High",
#         "Extra_C": "Active", "Previous_Scores": 75,
#         "Test_Score": 22, "Project_Marks": 33, "Backlogs": 1
#     }
#     print(f"Predicted score: {predict_exam_score(sample):.2f}")

# -----------------------------
# Step 4: Testing
# -----------------------------
if __name__ == "__main__":

    print("\n🔹 TEST CASE 1: TOP STUDENT")
    student1 = {
        "Hours_Studied": 40,
        "Attendance": 100,
        "Submission_Timeliness": "On time",
        "Participation": "High",
        "Extra_C": "Highly Active",
        "Previous_Scores": 100,
        "Test_Score": 30,
        "Project_Marks": 40,
        "Backlogs": 0
    }
    print(f"Predicted score: {predict_exam_score(student1):.2f}")


    print("\n🔹 TEST CASE 2: AVERAGE STUDENT")
    student2 = {
        "Hours_Studied": 20,
        "Attendance": 75,
        "Submission_Timeliness": "On time",
        "Participation": "Medium",
        "Extra_C": "Active",
        "Previous_Scores": 70,
        "Test_Score": 20,
        "Project_Marks": 25,
        "Backlogs": 1
    }
    print(f"Predicted score: {predict_exam_score(student2):.2f}")


    print("\n🔹 TEST CASE 3: POOR STUDENT")
    student3 = {
        "Hours_Studied": 5,
        "Attendance": 50,
        "Submission_Timeliness": "No Submission",
        "Participation": "Low",
        "Extra_C": "Inactive",
        "Previous_Scores": 40,
        "Test_Score": 10,
        "Project_Marks": 10,
        "Backlogs": 5
    }
    print(f"Predicted score: {predict_exam_score(student3):.2f}")
