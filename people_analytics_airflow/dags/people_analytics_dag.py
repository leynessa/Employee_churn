from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression

def load_data():
    hr = pd.read_csv("/usr/local/airflow/include/WA_Fn-UseC_-HR-Employee-Attrition.csv")
    print(f"Loaded {len(hr)} rows")
    return hr.to_json()

def clean_data(**context):
    hr = pd.read_json(context["ti"].xcom_pull(task_ids="load_data"))
    hr = hr.drop(columns=["EmployeeCount", "StandardHours", "Over18", "EmployeeNumber"])
    hr["Attrition"] = (hr["Attrition"] == "Yes").astype(int)
    multi_cols = ["Department", "JobRole", "MaritalStatus",
                  "EducationField", "BusinessTravel"]
    hr = pd.get_dummies(hr, columns=multi_cols, drop_first=True)
    le = LabelEncoder()
    for col in hr.select_dtypes(include="object").columns:
        hr[col] = le.fit_transform(hr[col])
    print(f"Cleaned. Columns: {hr.shape[1]}")
    return hr.to_json()

def train_and_predict(**context):
    hr = pd.read_json(context["ti"].xcom_pull(task_ids="clean_data"))
    X = hr.drop(columns=["Attrition"])
    y = hr["Attrition"]
    scaler = StandardScaler()
    X_sc = scaler.fit_transform(X)
    lr = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    lr.fit(X_sc, y)
    hr["attrition_probability"] = lr.predict_proba(X_sc)[:, 1].round(3)
    hr["flight_risk"] = pd.cut(
        hr["attrition_probability"],
        bins=[0, 0.3, 0.6, 1.0],
        labels=["Low", "Medium", "High"]
    )
    print(hr["flight_risk"].value_counts())
    return hr.to_json()

def export_data(**context):
    hr = pd.read_json(context["ti"].xcom_pull(task_ids="train_and_predict"))
    hr.to_csv("/usr/local/airflow/include/hr_with_predictions.csv", index=False)
    print("Exported successfully")

with DAG(
    dag_id="people_analytics_pipeline",
    schedule="@weekly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["people_analytics"],
) as dag:

    t1 = PythonOperator(task_id="load_data",         python_callable=load_data)
    t2 = PythonOperator(task_id="clean_data",        python_callable=clean_data)
    t3 = PythonOperator(task_id="train_and_predict", python_callable=train_and_predict)
    t4 = PythonOperator(task_id="export_data",       python_callable=export_data)

    t1 >> t2 >> t3 >> t4

